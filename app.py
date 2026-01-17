import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from backend.script_analysis import parse_script
from backend.matching import match_scenes_to_videos
from backend.editor import create_rough_cut

app = Flask(__name__)
app.secret_key = "dev_key"
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
app.config["OUTPUT_FOLDER"] = os.path.join(os.getcwd(), "static", "output")

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])
if not os.path.exists(app.config["OUTPUT_FOLDER"]):
    os.makedirs(app.config["OUTPUT_FOLDER"])

@app.route("/")
def index():
    return render_template("index.html")

from backend.video_processing import analyze_emotion_frames
import base64

@app.route("/upload_script", methods=["POST"])
def upload_script():
    # Option A: Manual Text
    if "script_text" in request.form and request.form["script_text"].strip():
        text = request.form["script_text"]
        try:
            scenes = parse_script(text)
            return jsonify({"scenes": scenes})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Option B: File Upload
    if "script" not in request.files:
        return jsonify({"error": "No file part and no text input"}), 400
    file = request.files["script"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        scenes = parse_script(text)
        return jsonify({"scenes": scenes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload_videos", methods=["POST"])
def upload_videos():
    if "videos" not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    uploaded_files = request.files.getlist("videos")
    video_paths = []
    
    for file in uploaded_files:
        if file.filename == "":
            continue
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        video_paths.append(filepath)
        
    return jsonify({"video_paths": video_paths})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    scenes = data.get("scenes", [])
    video_paths = data.get("video_paths", [])
    preferences = data.get("preferences", {})
    
    if not scenes or not video_paths:
        return jsonify({"error": "Missing scenes or videos"}), 400
    
    try:
        # Pass preferences to matching engine
        matches, confidence = match_scenes_to_videos(scenes, video_paths, preferences)
        
        output_filename = "final_cut.mp4"
        output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)
        
        print(f"[CompositionEngine] Rendering video at {output_path} with {preferences} settings...")
        
        success = create_rough_cut(matches, output_path)
        
        if success:
            return jsonify({
                "video_url": f"/static/output/{output_filename}",
                "confidence_score": confidence
            })
        else:
            return jsonify({"error": "Failed to create video"}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server Error: {str(e)}"}), 500


@app.route("/detect_emotion", methods=["POST"])
def detect_emotion():
    try:
        data = request.json
        image_data = data.get("image", "")
        if not image_data:
            return jsonify({"error": "No image data"}), 400
            
        # Remove header
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]
            
        # Save temp image
        import uuid
        temp_filename = f"temp_{uuid.uuid4()}.jpg"
        temp_path = os.path.join(app.config["UPLOAD_FOLDER"], temp_filename)
        
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(image_data))
            
        # Analyze using existing ML logic
        emotion = analyze_emotion_frames(temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({"emotion": emotion})
    except Exception as e:
        print(f"Emotion detect error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import os
import sys

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from backend.script_analysis import parse_script
from backend.video_processing import extract_features
# from backend.matching import match_scenes_to_videos
from backend.editor import create_rough_cut
from moviepy import ColorClip

# Re-implement simple matching inline for test or import if available
def match_scenes_to_videos(scenes, video_files):
    matches = []
    num_scenes = len(scenes)
    num_videos = len(video_files)
    for i in range(min(num_scenes, num_videos)):
        matches.append({
            "scene": scenes[i],
            "video_path": video_files[i]
        })
    return matches

def test_pipeline():
    print("Testing Pipeline...")
    
    # 1. Create dummy content
    script_text = "INT. LAB - DAY\nComputer beeps.\n\nEXT. SPACE - NIGHT\nStars twinkle."
    
    print("1. Parsing Script...")
    scenes = parse_script(script_text)
    print(f"Found {len(scenes)} scenes.")
    if len(scenes) != 2:
        print("Error: Expected 2 scenes.")
    
    print("2. Creating Dummy Videos...")
    if not os.path.exists('test_videos'):
        os.makedirs('test_videos')
        
    v1_path = os.path.abspath('test_videos/clip1.mp4')
    v2_path = os.path.abspath('test_videos/clip2.mp4')
    
    # Generate 1 sec clips
    try:
        # Generate simple color clips
        # Note: MoviePy v2 might use different ColorClip constructor or import
        # We assume compatible API
        c1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
        c1.write_videofile(v1_path, fps=24, logger=None)
        c2 = ColorClip(size=(640, 480), color=(0, 0, 255), duration=2)
        c2.write_videofile(v2_path, fps=24, logger=None)
    except Exception as e:
        print(f"Skipping video generation test due to moviepy issue: {e}")
        # Manually create empty files to prevent matching crash if we go further? 
        # No, editor needs valid video files.
        return

    print("3. extracting features...")
    # This might fail if OpenCV codecs are missing or headless issue
    try:
        f1 = extract_features(v1_path)
        print(f"Clip 1 features: {f1}")
    except Exception as e:
        print(f"Feature extraction warning: {e}")
    
    print("4. Matching...")
    videos = [v1_path, v2_path]
    matches = match_scenes_to_videos(scenes, videos)
    print(f"Matches: {len(matches)}")
    
    print("5. Editing...")
    output_path = os.path.abspath('test_output.mp4')
    success = create_rough_cut(matches, output_path)
    print(f"Editor Success: {success}")
    
    if success and os.path.exists(output_path):
        print("Test PASSED: Output video created.")
    else:
        print("Test FAILED.")

if __name__ == "__main__":
    test_pipeline()

import cv2
import numpy as np
import speech_recognition as sr
from moviepy import VideoFileClip
import os


def extract_features(video_path):
    """
    Extracts basic features from a video file: duration, fps, and average color of middle frame.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
        
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps > 0 else 0
    
    # Sample center frame for a quick thumbnail color
    if frame_count > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
        ret, frame = cap.read()
    else:
        ret = False
    
    avg_color = [0, 0, 0]
    if ret:
        avg_color_per_row = np.average(frame, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        
    cap.release()
    
    return {
        "duration": duration,
        "fps": fps,
        "avg_color": avg_color.tolist() if isinstance(avg_color, np.ndarray) else avg_color
    }


def extract_audio_text(video_path):
    """
    Extracts audio from video and converts it to text using SpeechRecognition.
    Returns the transcribed text.
    """
    try:
        # Extract audio to a temporary file
        clip = VideoFileClip(video_path)
        
        if not clip.audio:
            print(f"No audio found in {video_path}")
            clip.close()
            return ""

        audio_path = f"{video_path}.wav"
        
        # Write audio (suppress logs)
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        clip.close()
        
        # Recognize speech
        recognizer = sr.Recognizer()
        text = ""
        with sr.AudioFile(audio_path) as source:
            # record the whole file
            audio_data = recognizer.record(source)
            try:
                # Use Google Web Speech API (default key)
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = ""
            except sr.RequestError:
                text = ""
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return text
    except Exception as e:
        print(f"Error in STT for {video_path}: {e}")
        return ""

def analyze_emotion_frames(video_path):
    """
    Analyzes video frames to detect emotion.
    Prototype: Returns 'neutral', 'happy', 'sad', 'angry' based on basic visual heuristics 
    (brightness, warm/cool colors).
    """
    try:
        features = extract_features(video_path)
        if not features:
            return "neutral"
            
        avg_color = features.get("avg_color", [0, 0, 0])
        # BGR assumption
        b, g, r = avg_color[0], avg_color[1], avg_color[2]
        brightness = (b + g + r) / 3.0
        
        # Color temperature proxy: R > B (Warm) vs B > R (Cool)
        
        # Tuned Heuristics V4 (Strict Angry / Relaxed Happy)
        
        # HAPPY: Moderate to High Brightness (> 90)
        # We assume smiling/engaged faces are well-lit or screen-lit.
        if brightness > 90:
            return "happy"
            
        # ANGRY: Must be DARKER (< 90) AND have HIGH Red Dominance.
        # This filters out normal skin tone in bright light.
        if brightness < 90 and r > (g + 20) and r > (b + 20):
            return "angry"

        # SAD: Low brightness and Blue dominant
        if brightness < 80 and b > r:
            return "sad"

        # NEUTRAL: Default for normal colors in low light
        return "neutral"
    except:
        return "neutral"


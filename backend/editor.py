from moviepy import VideoFileClip, concatenate_videoclips
import os
import imageio_ffmpeg

# Explicitly set ffmpeg path for moviepy to avoid detection issues
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

def create_rough_cut(matches, output_path):
    """
    Creates a rough cut video from a list of matches.
    matches: List of dictionaries containing 'video_path'
    output_path: Path to save the output video
    """
    clips = []
    final_clip = None
    
    try:
        for match in matches:
            video_path = match.get('video_path')
            start = match.get('start')
            end = match.get('end')
            
            if video_path and os.path.exists(video_path):
                # Load clip
                try:
                    clip = VideoFileClip(video_path)
                    
                    # Apply subclip if start/end are present
                    if start is not None and end is not None:
                        # Ensure we don't go past the video duration
                        if start < clip.duration:
                            actual_end = min(end, clip.duration)
                            # Create a subclip - using subclipped for MoviePy 2.x
                            clip = clip.subclipped(start, actual_end)
                        else:
                            print(f"Warning: Start time {start} is beyond video duration {clip.duration}")
                            clip.close()
                            continue
                    
                    # RESIZE LOGIC: Enforce 360p (Height=360) for MAXIMUM SPEED
                    # This is "Draft Mode" quality
                    try:
                        clip = clip.resized(height=360)
                    except Exception as resize_err:
                        print(f"Warning: Resize failed: {resize_err}. Using original size.")
                        
                    clips.append(clip)
                except Exception as e:
                    print(f"Error loading clip {video_path}: {e}")
            else:
                print(f"Warning: Video path not found or None: {video_path}")
        
        if clips:
            # Method='compose' is generally safer for mixed formats
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # FINAL POLISH OPTIMIZATION:
            # - preset='ultrafast'
            # - bitrate='300k': Very low bitrate for speed
            # - fps=20: Reduced framerate to save 20% processing time
            final_clip.write_videofile(
                output_path, 
                codec='libx264', 
                audio_codec='aac', 
                fps=20, 
                preset='ultrafast',
                bitrate='300k',
                audio_bitrate='64k',
                threads=4
            )
            return True
        else:
            print("No clips to concatenate")
            return False
            
    except Exception as e:
        print(f"Error creating rough cut: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Close clips to release resources
        try:
            for clip in clips:
                clip.close()
            if final_clip:
                final_clip.close()
        except:
            pass

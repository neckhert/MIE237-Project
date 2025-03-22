import os
import moviepy.editor as mp

def extract_audio_from_videos(video_dir, audio_dir):
    # Create the audio directory if it doesn't exist
    os.makedirs(audio_dir, exist_ok=True)
    
    # Iterate over all files in the video directory
    for filename in os.listdir(video_dir):
        if filename.lower().endswith(('.mp4')):
            video_path = os.path.join(video_dir, filename)
            audio_path = os.path.join(audio_dir, os.path.splitext(filename)[0] + ".mp3")
            
            # Load video and extract audio
            try:
                video = mp.VideoFileClip(video_path)
                video.audio.write_audiofile(audio_path)
                print(f"Extracted audio: {audio_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    video_directory = "videos"  # Change to your source directory
    audio_directory = "audio"    # Change to your target directory
    extract_audio_from_videos(video_directory, audio_directory)

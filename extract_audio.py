import os
import subprocess


def extract_audio_from_videos(video_dir, audio_dir):
    # Create the audio directory if it doesn't exist
    os.makedirs(audio_dir, exist_ok=True)

    # Iterate over all files in the video directory
    for filename in os.listdir(video_dir):
        if filename.lower().endswith(('.mp4')):
            video_path = os.path.join(video_dir, filename)
            audio_path = os.path.join(
                audio_dir, os.path.splitext(filename)[0] + ".mp3")

            # Use ffmpeg to extract audio
            try:
                subprocess.run(
                    ["ffmpeg", "-i", video_path, "-q:a",
                        "0", "-map", "a", audio_path],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Extracted audio: {audio_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e.stderr.decode()}")


if __name__ == "__main__":
    # Change to your source directory
    video_directory = "tkinter-voting-app/src/data/videos"
    # Change to your target directory
    audio_directory = "tkinter-voting-app/src/data/audios"
    extract_audio_from_videos(video_directory, audio_directory)

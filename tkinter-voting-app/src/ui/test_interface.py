import customtkinter as ctk
from ffpyplayer.player import MediaPlayer
import os
import random
from tkinter import messagebox
import cv2
from data.csv_handler import write_voting_data
import numpy as np
from itertools import product
import time  # Import the time module


class TestInterface(ctk.CTkFrame):
    def __init__(self, parent, user_id, switch_to_main_menu):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.switch_to_main_menu = switch_to_main_menu

        # Initialize media player attributes
        self.media_player = None
        self.audio_player = None

        # Timer attributes
        self.start_time = 0
        self.end_time = 0

        # Define video and audio pools
        self.video_pool = [
            {"person": "LeBron", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/LebronReal.mp4"},
            {"person": "LeBron", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/LebronFake.mp4"},
            {"person": "Will Smith", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/WillsmithReal.mp4"},
            {"person": "Will Smith", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/WillSmithFake.mp4"},
            {"person": "Snoop Dogg", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/SnoopDogReal.mp4"},
            {"person": "Snoop Dogg", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/SnoopDogFake.mp4"},
            {"person": "MrBeast", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/MrBeastreal.mp4"},
            {"person": "MrBeast", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/MrBeastFake.mp4"},
            {"person": "Justin Bieber", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/JustinBieberReal.mp4"},
            {"person": "Justin Bieber", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/JustinBieberFake.mp4"},
            {"person": "Bill Gates", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/BillGatesReal.mp4"},
            {"person": "Bill Gates", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/BillGatesFake.mp4"},
            {"person": "Caitlin Clark", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/CaitlinClarkReal.mp4"},
            {"person": "Caitlin Clark", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/CaitlinClarkFake.mp4"},
            {"person": "Kim K", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/KimKardashianReal.mp4"},
            {"person": "Kim K", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/KimKardashianFake.mp4"},
            {"person": "Jordan", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/MichaelJordanReal.mp4"},
            {"person": "Jordan", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/MichaelJordanFake.mp4"},
            {"person": "Oprah", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/OprahWinfreyReal.mp4"},
            {"person": "Oprah", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/videos/OprahWinfreyFake.mp4"}
        ]

        self.audio_pool = [
            {"person": "LeBron", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/LebronReal.mp3"},
            {"person": "LeBron", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/LebronFake.mp3"},
            {"person": "Will Smith", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/WillsmithReal.mp3"},
            {"person": "Will Smith", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/WillSmithFake.mp3"},
            {"person": "Snoop Dogg", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/SnoopDogReal.mp3"},
            {"person": "Snoop Dogg", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/SnoopDogFake.mp3"},
            {"person": "MrBeast", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/MrBeastreal.mp3"},
            {"person": "MrBeast", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/MrBeastFake.mp3"},
            {"person": "Justin Bieber", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/JustinBieberReal.mp3"},
            {"person": "Justin Bieber", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/JustinBieberFake.mp3"},
            {"person": "Bill Gates", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/BillGatesReal.mp3"},
            {"person": "Bill Gates", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/BillGatesFake.mp3"},
            {"person": "Caitlin Clark", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/CaitlinClarkReal.mp3"},
            {"person": "Caitlin Clark", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/CaitlinClarkFake.mp3"},
            {"person": "Kim K", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/KimKardashianReal.mp3"},
            {"person": "Kim K", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/KimKardashianFake.mp3"},
            {"person": "Jordan", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/MichaelJordanReal.mp3"},
            {"person": "Jordan", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/MichaelJordanFake.mp3"},
            {"person": "Oprah", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/OprahWinfreyReal.mp3"},
            {"person": "Oprah", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "AI",
             "video_path": "tkinter-voting-app/src/data/audios/OprahWinfreyFake.mp3"}
        ]

        # Filter and shuffle pools to ensure 5 real and 5 fake items
        self.video_pool, self.audio_pool = self.get_balanced_pool(
            self.video_pool, self.audio_pool)

        self.current_pool = self.video_pool
        self.current_round = 0

        # # Start the timer
        self.start_time = time.time()

        # Display the first voting round
        self.display_voting_round()

    def get_balanced_pool(self, video_pool, audio_pool):
        """Ensure that there are exactly 5 videos and 5 audios, with 5 real and 5 fake media in total, and each person is used only once."""
        # Separate real and fake items
        real_videos = [item for item in video_pool if item["kind"] == "real"]
        fake_videos = [item for item in video_pool if item["kind"] == "fake"]
        real_audios = [item for item in audio_pool if item["kind"] == "real"]
        fake_audios = [item for item in audio_pool if item["kind"] == "fake"]

        # Shuffle lists to randomize selections
        random.shuffle(real_videos)
        random.shuffle(fake_videos)
        random.shuffle(real_audios)
        random.shuffle(fake_audios)

        # Track used people
        used_people = set()

        # Select videos
        thing = random.randint(0, 1)
        if thing == 0:
            balanced_videos = []
            i = 0
            j = 0
            while len(balanced_videos) < 5:
                real = real_videos[i]
                fake = fake = fake_videos[j]
                while real['person'] in used_people and i < 9:
                    i += 1
                    real = real_videos[i]
                balanced_videos.append(real)
                used_people.add(real["person"])
                while fake['person'] in used_people and j < 9:
                    j += 1
                    fake = fake_videos[j]
                if len(balanced_videos) < 5:
                    balanced_videos.append(fake)
                    used_people.add(fake["person"])
                i += 1
                j += 1

            # Select audios
            balanced_audios = []
            i = 0
            j = 0
            fake = fake_audios[j]
            real = real_audios[i]
            while len(balanced_audios) < 5:
                while fake['person'] in used_people and j < 9:
                    j += 1
                    fake = fake_audios[j]
                balanced_audios.append(fake)
                used_people.add(fake["person"])
                while real['person'] in used_people and i < 9:
                    i += 1
                    real = real_audios[i]
                if len(balanced_audios) < 5:
                    balanced_audios.append(real)
                    used_people.add(real["person"])
                i += 1
                j += 1
        else:
            balanced_videos = []
            i = 0
            j = 0
            real = real_videos[j]
            fake = fake_videos[i]

            while len(balanced_videos) < 5:
                while fake['person'] in used_people and i < 9:
                    i += 1
                    fake = fake_videos[i]
                balanced_videos.append(fake)
                used_people.add(fake["person"])
                while real['person'] in used_people and j < 9:
                    j += 1
                    real = real_videos[j]
                if len(balanced_videos) < 5:
                    balanced_videos.append(real)
                    used_people.add(real["person"])
                i += 1
                j += 1

            # Select audios
            balanced_audios = []
            i = 0
            j = 0
            fake = fake_audios[i]
            real = real_audios[j]
            while len(balanced_audios) < 5:
                while real['person'] in used_people and j < 9:
                    j += 1
                    real = real_audios[j]
                balanced_audios.append(real)
                used_people.add(real["person"])
                while fake['person'] in used_people and i < 9:
                    i += 1
                    fake = fake_audios[i]
                if len(balanced_audios) < 5:
                    balanced_audios.append(fake)
                    used_people.add(fake["person"])
                i += 1
                j += 1

        # Ensure we have exactly 5 real and 5 fake media
        real_count = sum(1 for item in balanced_videos +
                         balanced_audios if item["kind"] == "real")
        fake_count = sum(1 for item in balanced_videos +
                         balanced_audios if item["kind"] == "fake")

        if real_count != 5 or fake_count != 5:
            raise ValueError(
                "Unable to balance the pool with 5 real and 5 fake media.")

        # Shuffle again to ensure order randomness
        random.shuffle(balanced_videos)
        random.shuffle(balanced_audios)

        return balanced_videos, balanced_audios

    def display_voting_round(self):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Check if all rounds are completed
        if self.current_round >= len(self.current_pool):
            if self.current_pool == self.video_pool:
                self.show_transition_window()
                return
            else:
                self.switch_to_thank_you()
                return

        # Get the current data
        current_data = self.current_pool[self.current_round]
        option1, option2 = current_data["options"]

        # Display the round number and data type
        ctk.CTkLabel(self, text=f"Round {self.current_round + 1}",
                     font=("Arial", 16)).pack(pady=10)

        # Play the video or audio for the current round
        media_path = current_data["video_path"]
        # use the video play fucntion since the audio one doesnt work
        self.play_video(media_path)

        # Display the voting options
        ctk.CTkButton(self, text=option1,
                      command=lambda: self.record_vote(option1),
                      width=200, height=50, font=ctk.CTkFont(size=16)).pack(pady=10)

        ctk.CTkButton(self, text=option2,
                      command=lambda: self.record_vote(option2),
                      width=200, height=50, font=ctk.CTkFont(size=16)).pack(pady=10)

    def play_video(self, video_path):
        """Play the video."""
        # Stop any previous video playback
        self.stop_video()

        # Debug: Check if the video file exists
        if not os.path.exists(video_path):
            messagebox.showerror(
                "Error", f"Video file not found: {video_path}")
            return

        # Create a MediaPlayer instance
        try:
            self.media_player = MediaPlayer(video_path)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to initialize MediaPlayer: {e}")
            return

        # Retrieve the video's frame rate
        frame_rate = self.media_player.get_metadata().get(
            'frame_rate', 30)  # Default to 30 fps if not available
        if isinstance(frame_rate, tuple):  # Handle frame rate as a tuple (numerator, denominator)
            if frame_rate[1] == 0:  # Avoid division by zero
                self.frame_rate = 30  # Default to 30 fps
            else:
                self.frame_rate = frame_rate[0] / frame_rate[1]
        else:
            self.frame_rate = frame_rate

        # Start video playback
        self.update_video_frame()

    def stop_video(self):
        if self.media_player:
            self.media_player.close_player()
            self.media_player = None

    def record_vote(self, vote):
        """Record the user's vote."""
        current_data = self.current_pool[self.current_round]
        ground_truth = current_data["ground_truth"]

        write_voting_data("user_votes.csv", self.user_id,
                          current_data["video_path"], vote, ground_truth)

        self.current_round += 1
        self.display_voting_round()

    def show_transition_window(self):
        """Display a transition window between video and audio tests."""
        for widget in self.winfo_children():
            widget.destroy()

        self.stop_video()

        ctk.CTkLabel(self, text="You have completed the video test.\nYou will now be test with 5 different audio clips.\nAs with the videos, please wait until the audio finishes playing before voting.",
                     font=("Arial", 16), justify="center").pack(pady=20)
        ctk.CTkLabel(self, text="Headphone use is recomended.",
                     font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self, text="Start Audio Test",
                      command=self.start_audio_test,
                      width=200, height=50, font=ctk.CTkFont(size=16)).pack(pady=20)

    def start_audio_test(self):
        """Switch to the audio pool and start the audio test."""
        self.stop_video()
        self.current_pool = self.audio_pool
        self.current_round = 0
        self.display_voting_round()

    def switch_to_thank_you(self):
        """Display the thank-you screen."""
        for widget in self.winfo_children():
            widget.destroy()

        # Stop the timer
        self.end_time = time.time()

        # Calculate elapsed time
        elapsed_time = self.end_time - self.start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)

        # Write elapsed time to a file
        self.write_elapsed_time_to_file(elapsed_minutes, elapsed_seconds)

        # Display the thank-you message
        ctk.CTkLabel(self, text=f"Thank you for participating!\nYou completed the test in {elapsed_minutes} minutes and {elapsed_seconds} seconds.",
                     font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self, text="Return to Main Menu",
                      command=self.switch_to_main_menu,
                      width=200, height=50, font=ctk.CTkFont(size=16)).pack(pady=10)

    def write_elapsed_time_to_file(self, minutes, seconds):
        """Write the elapsed time to a CSV file."""
        import csv
        file_path = "elapsed_time.csv"  # File to store elapsed times
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write the header if the file is new
            if not file_exists:
                writer.writerow(["User ID", "Elapsed Time (Minutes)", "Elapsed Time (Seconds)"])
            # Write the elapsed time for the current user
            writer.writerow([self.user_id, minutes, seconds])

    def update_video_frame(self):
        if self.media_player:
            # Get the next frame from the MediaPlayer
            frame, val = self.media_player.get_frame()

            # Debug: Check the frame and value
            print(f"Frame: {frame}, Value: {val}")

            if frame is not None:
                img, t = frame
                # Convert the frame to a format suitable for OpenCV
                try:
                    # Convert bytearray to NumPy array with the correct shape
                    img_array = np.frombuffer(
                        img.to_bytearray()[0], dtype=np.uint8)
                    img_array = img_array.reshape((img.get_size()[1], img.get_size()[
                                                0], 3))  # Height, Width, Channels
                    # Convert BGR to RGB for correct coloring
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                    # Display the frame in an OpenCV window
                    cv2.imshow("Video Playback", img_array)
                    # Use the default playback rate based on the frame rate
                    delay = int(1000 / self.frame_rate)
                    cv2.waitKey(delay)
                except Exception as e:
                    print(f"Error processing frame: {e}")
                    return

            # Check if playback is finished
            if val == 'eof':
                print("End of video playback.")
                self.stop_video()
                cv2.destroyAllWindows()  # Close the OpenCV window
                return

            # Schedule the next frame update
            self.after(10, self.update_video_frame)
            
def run_test_interface():
    root = ctk.CTk()
    root.title("Voting App")
    root.geometry("800x600")

    user_id = ctk.StringVar()
    ctk.CTkEntry(root, textvariable=user_id).pack(pady=5)
    ctk.CTkButton(root, text="Start Test", command=lambda: start_test(
        root, user_id.get()),
        width=200, height=50, font=ctk.CTkFont(size=16)).pack(pady=20)
    root.mainloop()


def start_test(root, user_id):
    if not user_id:
        ctk.CTkMessagebox.show_warning(
            "Input Error", "Please enter your User ID/Name.")
        return

    def switch_to_main_menu():
        for widget in root.winfo_children():
            widget.destroy()
        ctk.CTkLabel(root, text="Main Menu (Placeholder)",
                     font=("Arial", 16)).pack(pady=20)

    app = TestInterface(root, user_id, switch_to_main_menu)

    random.seed(42)
    random.shuffle(app.video_pool)

    app.pack()
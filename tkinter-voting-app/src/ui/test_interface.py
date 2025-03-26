import customtkinter as ctk
from ffpyplayer.player import MediaPlayer
import os
import random
import threading
import time
from data.csv_handler import write_voting_data
import cv2
import numpy as np


class TestInterface(ctk.CTkFrame):
    def __init__(self, parent, user_id, switch_to_main_menu):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.switch_to_main_menu = switch_to_main_menu

        # Initialize media player attributes
        self.media_player = None
        self.audio_player = None

        # Define video and audio pools
        self.video_pool = [
            {"person": "LeBron", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/lebron_real.mp4"},
            {"person": "LeBron", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/lebron_fake.mp4"},
            {"person": "Will Smith", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/WillsmithReal.mp4"},
            {"person": "Will Smith", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/WillSmithFake.mp4"},
            {"person": "Snoop Dogg", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/SnoopDogReal.mp4"},
            {"person": "Snoop Dogg", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/SnoopDogFake.mp4"},
            {"person": "MrBeast", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/MrBeastreal.mp4"},
            {"person": "MrBeast", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/MrBeastFake.mp4"},
            {"person": "Justin Bieber", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/JustinBieberReal.mp4"},
            {"person": "Justin Bieber", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/JustinBieberFake.mp4"},
            {"person": "Bill Gates", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/videos/BillGatesReal.mp4"},
            {"person": "Bill Gates", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/videos/BillGatesFake.mp4"}
        ]

        self.audio_pool = [
            {"person": "LeBron", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/LebronReal.mp3"},
            {"person": "LeBron", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/LebronFake.mp3"},
            {"person": "Will Smith", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/WillsmithReal.mp3"},
            {"person": "Will Smith", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/WillSmithFake.mp3"},
            {"person": "Snoop Dogg", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/SnoopDogReal.mp3"},
            {"person": "Snoop Dogg", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/SnoopDogFake.mp3"},
            {"person": "MrBeast", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/MrBeastreal.mp3"},
            {"person": "MrBeast", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/MrBeastFake.mp3"},
            {"person": "Justin Bieber", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/JustinBieberReal.mp3"},
            {"person": "Justin Bieber", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/JustinBieberFake.mp3"},
            {"person": "Bill Gates", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/BillGatesReal.mp3"},
            {"person": "Bill Gates", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/BillGatesFake.mp3"},
            {"person": "Caitlin Clark", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/CaitlinClarkReal.mp3"},
            {"person": "Caitlin Clark", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/CaitlinClarkFake.mp3"},
            {"person": "Kim K", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/KimKardashianReal.mp3"},
            {"person": "Kim K", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/KimKardashianFake.mp3"},
            {"person": "Jordan", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/MichaelJordanReal.mp3"},
            {"person": "Jordan", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/MichaelJordanFake.mp3"},
            {"person": "Oprah", "kind": "real", "options": ("Real", "AI"), "ground_truth": "Real",
             "video_path": "tkinter-voting-app/src/data/audios/OprahWinfreyReal.mp3"},
            {"person": "Oprah", "kind": "fake", "options": ("Real", "AI"), "ground_truth": "Fake",
             "video_path": "tkinter-voting-app/src/data/audios/OprahWinfreyFake.mp3"}
        ]

        # Filter and shuffle pools
        self.video_pool = self.filter_pool(self.video_pool)
        random.shuffle(self.video_pool)
        self.video_pool = self.video_pool[:5]

        self.audio_pool = self.filter_pool(self.audio_pool)
        random.shuffle(self.audio_pool)
        self.audio_pool = self.audio_pool[:5]

        self.current_pool = self.video_pool
        self.current_round = 0

        # Display the first voting round
        self.display_voting_round()

    def filter_pool(self, pool):
        """Filter the pool to include only one dataset (real or fake) per person."""
        filtered_pool = []
        seen_people = set()

        for item in pool:
            person = item["person"]
            if person not in seen_people:
                person_items = [v for v in pool if v["person"] == person]
                selected_item = random.choice(person_items)
                filtered_pool.append(selected_item)
                seen_people.add(person)

        return filtered_pool

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
                      command=lambda: self.record_vote(option1)).pack(pady=10)
        ctk.CTkButton(self, text=option2,
                      command=lambda: self.record_vote(option2)).pack(pady=10)

    def play_video(self, video_path):
        """Play the video."""
        self.stop_video()

        if not os.path.exists(video_path):
            ctk.CTkMessagebox.show_error(
                "Error", f"Video file not found: {video_path}")
            return

        try:
            self.media_player = MediaPlayer(video_path)
        except Exception as e:
            ctk.CTkMessagebox.show_error(
                "Error", f"Failed to initialize MediaPlayer: {e}")
            return

        self.update_video_frame()

    def play_audio(self, audio_path, person_name):
        """Play the audio."""
        self.stop_audio()

        # Display the person's name
        ctk.CTkLabel(self, text=f"Person: {person_name}", font=(
            "Arial", 16)).pack(pady=10)

        if not os.path.exists(audio_path):
            ctk.CTkMessagebox.show_error(
                "Error", f"Audio file not found: {audio_path}")
            return

        def audio_thread():
            try:
                self.audio_player = MediaPlayer(audio_path)
                while True:
                    audio_pos = self.audio_player.get_pts()
                    if audio_pos < 0:
                        break
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error playing audio: {e}")
                ctk.CTkMessagebox.show_error(
                    "Error", f"Failed to play audio: {e}")
            finally:
                self.stop_audio()

        threading.Thread(target=audio_thread, daemon=True).start()

    def stop_video(self):
        if self.media_player:
            self.media_player.close_player()
            self.media_player = None

    def stop_audio(self):
        if hasattr(self, "audio_player") and self.audio_player:
            self.audio_player.close_player()
            self.audio_player = None

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

        ctk.CTkLabel(self, text="You have completed the video test.\nGet ready for the audio test!",
                     font=("Arial", 16), justify="center").pack(pady=20)
        ctk.CTkButton(self, text="Start Audio Test",
                      command=self.start_audio_test).pack(pady=20)

    def start_audio_test(self):
        """Switch to the audio pool and start the audio test."""
        self.current_pool = self.audio_pool
        self.current_round = 0
        self.display_voting_round()

    def switch_to_thank_you(self):
        """Display the thank-you screen."""
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="Thank you for participating!",
                     font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self, text="Return to Main Menu",
                      command=self.switch_to_main_menu).pack(pady=10)

    def update_video_frame(self):
        """Update the video frame during playback."""
        if self.media_player:
            # Get the next frame from the MediaPlayer
            frame, val = self.media_player.get_frame()

            if val == 'eof':  # End of file
                print("End of video playback.")
                self.stop_video()
                return

            if frame is not None:
                img, t = frame
                try:
                    # Convert the frame to a format suitable for OpenCV
                    img_array = np.frombuffer(
                        img.to_bytearray()[0], dtype=np.uint8)
                    img_array = img_array.reshape((img.get_size()[1], img.get_size()[
                                                  0], 3))  # Height, Width, Channels
                    img_array = cv2.cvtColor(
                        img_array, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

                    # Display the frame using OpenCV
                    cv2.imshow("Video Playback", img_array)
                    cv2.waitKey(1)  # Wait for 1ms to display the frame
                except Exception as e:
                    print(f"Error processing frame: {e}")
                    self.stop_video()

            # Schedule the next frame update
            self.after(30, self.update_video_frame)


def run_test_interface():
    root = ctk.CTk()
    root.title("Voting App")
    root.geometry("800x600")

    user_id = ctk.StringVar()
    ctk.CTkEntry(root, textvariable=user_id).pack(pady=5)
    ctk.CTkButton(root, text="Start Test", command=lambda: start_test(
        root, user_id.get())).pack(pady=20)
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

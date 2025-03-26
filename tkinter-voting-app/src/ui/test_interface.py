from tkinter import Frame, Button, Label, Entry, StringVar, Tk, messagebox, ttk
import pygame
from data.csv_handler import write_voting_data
from ffpyplayer.player import MediaPlayer
import os  # For debugging file paths
import numpy as np  # Import NumPy for array conversion
import cv2  # Import OpenCV for video playback
import random  # Import random for shuffling
import threading  # Import threading for audio playback
import time  # Import time for sleep


class TestInterface(Frame):
    def __init__(self, parent, user_id, switch_to_main_menu):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.switch_to_main_menu = switch_to_main_menu

        # Define a list of videos with their metadata
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

        # Filter the video pool to include only one video per person
        self.video_pool = self.filter_pool(self.video_pool)

        # Shuffle the video pool for random order
        random.shuffle(self.video_pool)
        self.video_pool = self.video_pool[:5]

        # Do the same with the audio pool
        self.audio_pool = self.filter_pool(self.audio_pool)
        random.shuffle(self.audio_pool)
        self.audio_pool = self.audio_pool[:5]

        self.current_pool = self.video_pool
        self.current_round = 0
        self.video_label = None  # Label to display video frames
        self.video_capture = None  # OpenCV video capture object
        self.play_rate = 25  # Default play rate in milliseconds

        pygame.mixer.init()  # Initialize the pygame mixer for audio
        self.audio_channel = None  # To manage audio playback
        self.media_player = None  # MediaPlayer instance for video and audio

        # Display the first voting round
        self.display_voting_round()

    def filter_pool(self, pool):
        """Filter the pool to include only one dataset (real or fake) per person."""
        filtered_pool = []
        seen_people = set()

        for video in pool:
            person = video["person"]
            if person not in seen_people:
                # Randomly select either "real" or "fake" for this person
                person_videos = [
                    v for v in pool if v["person"] == person]
                selected_video = random.choice(person_videos)
                filtered_pool.append(selected_video)
                seen_people.add(person)

        return filtered_pool

    def display_voting_round(self):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Check if all rounds are completed
        if self.current_round >= len(self.current_pool):
            if self.current_pool == self.video_pool:
                # Show the transition window before switching to the audio pool
                self.show_transition_window()
                return
            else:
                # If both pools are completed, show the thank-you screen
                self.switch_to_thank_you()
                return

        # Get the current data
        current_data = self.current_pool[self.current_round]
        option1, option2 = current_data["options"]


        # Display the round number and data type
        Label(self, text=f"Round {self.current_round + 1}",
              font=("Arial", 16)).pack(pady=10)

        # Play the video or audio for the current round
        media_path = current_data["video_path"]
        self.play_video(media_path)

        # Display the voting options
        Button(self, text=option1, command=lambda: self.record_vote(
            option1)).pack(pady=10)
        Button(self, text=option2, command=lambda: self.record_vote(
            option2)).pack(pady=10)

    def play_video(self, video_path):
        """Play the video."""
        self.stop_video()

        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

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

        # Retrieve the video's metadata
        video_metadata = self.media_player.get_metadata()
        if video_metadata:
            frame_rate = video_metadata.get(
                'frame_rate', 30)  # Default to 30 fps
            # Handle frame rate as a tuple (numerator, denominator)
            if isinstance(frame_rate, tuple):
                if frame_rate[1] != 0:  # Avoid division by zero
                    self.frame_rate = frame_rate[0] / frame_rate[1]
                else:
                    self.frame_rate = 30
            else:
                self.frame_rate = frame_rate

        # Start video playback
        self.update_video_frame()

    def play_audio(self, audio_path, person_name):
        """Play the audio using ffpyplayer."""
        self.stop_audio()

        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Display the person's name
        Label(self, text=f"Person: {person_name}", font=("Arial", 16)).pack(pady=10)

        if not os.path.exists(audio_path):
            messagebox.showerror("Error", f"Audio file not found: {audio_path}")
            return

        def audio_thread():
            try:
                self.audio_player = MediaPlayer(audio_path)
                while True:
                    audio_pos = self.audio_player.get_pts()
                    if audio_pos < 0:  # Playback finished
                        break
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error playing audio: {e}")
                messagebox.showerror("Error", f"Failed to play audio: {e}")
            finally:
                self.stop_audio()

        threading.Thread(target=audio_thread, daemon=True).start()

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

    def stop_video(self):
        if self.media_player:
            self.media_player.close_player()
            self.media_player = None
        cv2.destroyAllWindows()  # Ensure the OpenCV window is closed

    def stop_audio(self):
        """Stop the audio playback."""
        if hasattr(self, "audio_player") and self.audio_player:
            self.audio_player.close_player()
            self.audio_player = None

    def record_vote(self, vote):
        # Save the vote to the CSV file
        current_data = self.video_pool[self.current_round]
        ground_truth = current_data["ground_truth"]

        write_voting_data("user_votes.csv", self.user_id,
                          current_data["video_path"], vote, ground_truth)

        # Move to the next round
        self.current_round += 1
        self.display_voting_round()

    def switch_to_thank_you(self):
        # Clear the current frame and display the thank-you message
        self.stop_video()
        for widget in self.parent.winfo_children():
            widget.destroy()
        Label(self.parent, text="Thank you for participating!",
              font=("Arial", 16)).pack(pady=20)
        Button(self.parent, text="Return to Main Menu",
               command=self.switch_to_main_menu).pack(pady=10)

    def show_transition_window(self):
        """Display a transition window between video and audio tests."""
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Display the transition message
        Label(self, text="You have completed the video test.\nGet ready for the audio test!",
              font=("Arial", 16), justify="center").pack(pady=20)

        # Add a button to proceed to the audio test
        Button(self, text="Start Audio Test", font=("Arial", 12),
               command=self.start_audio_test).pack(pady=20)

    def start_audio_test(self):
        """Switch to the audio pool and start the audio test."""
        self.current_pool = self.audio_pool
        self.current_round = 0
        self.display_voting_round()

    # TODO: switch between video and audio
    # TODO: consent form


def run_test_interface():
    root = Tk()
    root.title("Voting App")
    root.geometry("800x600")

    user_id = StringVar()
    Entry(root, textvariable=user_id).pack(pady=5)
    Button(root, text="Start Test", command=lambda: start_test(
        root, user_id.get())).pack(pady=20)
    root.mainloop()


def start_test(root, user_id):
    if not user_id:
        messagebox.showwarning(
            "Input Error", "Please enter your User ID/Name.")
        return

    # Define a dummy switch_to_main_menu function for testing
    def switch_to_main_menu():
        for widget in root.winfo_children():
            widget.destroy()
        Label(root, text="Main Menu (Placeholder)",
              font=("Arial", 16)).pack(pady=20)

    # Create a new TestInterface instance
    app = TestInterface(root, user_id, switch_to_main_menu)

    # TODO: RANDOM ORDER?
    # Seed the random number generator with the current system time
    random.seed(42)  # Ensures a different seed is used each time
    random.shuffle(app.video_pool)  # Randomize the video order

    app.pack()

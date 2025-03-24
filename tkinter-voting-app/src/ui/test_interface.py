from tkinter import Frame, Button, Label, Entry, StringVar, Tk, messagebox
import pygame
from data.csv_handler import write_voting_data
from ffpyplayer.player import MediaPlayer
import os  # For debugging file paths
import numpy as np  # Import NumPy for array conversion
import cv2  # Import OpenCV for video playback
import random  # Import random for shuffling


class TestInterface(Frame):
    def __init__(self, parent, user_id, switch_to_main_menu):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.switch_to_main_menu = switch_to_main_menu

        # Define voting rounds with ground truths
        self.voting_data = [
            {"options": ("Option 1", "Option 2"), "ground_truth": "Ai"},
            {"options": ("Red", "Blue"), "ground_truth": "Real"},
            # Add more entries as needed
        ]

        self.current_round = 0
        self.video_label = None  # Label to display video frames
        self.video_capture = None  # OpenCV video capture object
        self.play_rate = 25  # Default play rate in milliseconds

        pygame.mixer.init()  # Initialize the pygame mixer for audio
        self.audio_channel = None  # To manage audio playback
        self.media_player = None  # MediaPlayer instance for video and audio

        # Display the first voting round
        self.display_voting_round()

    def display_voting_round(self):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Check if all rounds are completed
        if self.current_round >= len(self.voting_data):
            self.switch_to_thank_you()
            return

        # Get the current voting data
        current_data = self.voting_data[self.current_round]
        option1, option2 = current_data["options"]

        # Display the voting options
        Label(self, text=f"Round {self.current_round + 1}",
              font=("Arial", 16)).pack(pady=20)

        # Play the video for the current round
        video_path = f"tkinter-voting-app/src/data/video_{self.current_round + 1}.mp4"
        self.play_video(video_path)

        Button(self, text=option1, command=lambda: self.record_vote(
            option1)).pack(pady=10)
        Button(self, text=option2, command=lambda: self.record_vote(
            option2)).pack(pady=10)

    def play_video(self, video_path):
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

    def record_vote(self, vote):
        # Save the vote to the CSV file
        current_data = self.voting_data[self.current_round]
        ground_truth = current_data["ground_truth"]

        write_voting_data("user_votes.csv", self.user_id,
                          f"tkinter-voting-app/src/data/video_{self.current_round + 1}", vote, ground_truth)

        # Move to the next round
        self.current_round += 1
        self.display_voting_round()

    def switch_to_thank_you(self):
        # Clear the current frame and display the thank-you message
        for widget in self.parent.winfo_children():
            widget.destroy()
        Label(self.parent, text="Thank you for participating!",
              font=("Arial", 16)).pack(pady=20)
        Button(self.parent, text="Return to Main Menu",
               command=self.switch_to_main_menu).pack(pady=10)


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
    random.seed()  # Ensures a different seed is used each time
    random.shuffle(app.voting_data)  # Randomize the video order
    print("Voting data has been randomized:",
          app.voting_data)  # Log the randomized data

    app.pack()

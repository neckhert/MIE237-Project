import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
import os
from tkVideoPlayer import TkinterVideo  # You'll need to install this: pip install tkVideoPlayer

class ExperimentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Experiment")
        self.root.geometry("800x600")
        
        # Sample video list and ground truth (replace with your actual videos and truths)
        self.videos = [
            {"path": "video1.mp4", "ground_truth": "positive"},
            {"path": "video2.mp4", "ground_truth": "negative"},
            # Add more videos here (total 10)
        ]
        self.current_video = 0
        
        # Data storage
        self.results = pd.DataFrame(columns=["video", "ground_truth", "user_response"])
        
        # Start with welcome screen
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_window()
        
        # Welcome text
        welcome_text = tk.Label(self.root, text="Welcome to the Video Experiment", font=("Arial", 16))
        welcome_text.pack(pady=20)
        
        # Consent form
        consent_text = tk.Text(self.root, height=10, width=60)
        consent_text.insert(tk.END, "This experiment involves watching 10 videos and rating them as positive or negative.\n"
                           "Your responses will be recorded for research purposes.\n"
                           "Participation is voluntary and you may withdraw at any time.\n\n"
                           "Do you consent to participate?")
        consent_text.config(state="disabled")
        consent_text.pack(pady=20)
        
        # Consent button
        consent_btn = tk.Button(self.root, text="I Consent", command=self.start_experiment)
        consent_btn.pack(pady=20)

    def start_experiment(self):
        if self.current_video < len(self.videos):
            self.show_video()
        else:
            self.show_results()

    # def show_video(self):
    #     self.clear_window()
        
    #     # Video player
    #     video_player = TkinterVideo(master=self.root, scaled=True)
    #     video_player.load(self.videos[self.current_video]["path"])
    #     video_player.pack(expand=True, fill="both", padx=10, pady=10)
    #     video_player.play()
        
    #     # Wait for video to finish then show rating
    #     video_player.bind("<<Ended>>", lambda e: self.show_rating(video_player))

    # def show_rating(self, video_player):
    #     video_player.pack_forget()
        
    #     # Rating frame
    #     rating_frame = ttk.Frame(self.root)
    #     rating_frame.pack(expand=True)
        
    #     tk.Label(rating_frame, text="Was this video positive or negative?", font=("Arial", 14)).pack(pady=20)
        
    #     response = tk.StringVar()
        
    #     tk.Radiobutton(rating_frame, text="Positive", variable=response, value="positive").pack()
    #     tk.Radiobutton(rating_frame, text="Negative", variable=response, value="negative").pack()
        
    #     submit_btn = tk.Button(rating_frame, text="Submit",
    #                          command=lambda: self.save_response(response.get()))
    #     submit_btn.pack(pady=20)

    def save_response(self, user_response):
        if not user_response:
            messagebox.showwarning("Warning", "Please select an option")
            return
            
        # Save to dataframe
        new_row = pd.DataFrame({
            "video": [self.videos[self.current_video]["path"]],
            "ground_truth": [self.videos[self.current_video]["ground_truth"]],
            "user_response": [user_response]
        })
        self.results = pd.concat([self.results, new_row], ignore_index=True)
        
        self.current_video += 1
        self.start_experiment()

    def show_results(self):
        self.clear_window()
        
        tk.Label(self.root, text="Experiment Complete!", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Thank you for participating.").pack(pady=20)
        
        # Save results to CSV
        self.results.to_csv("experiment_results.csv", index=False)
        
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentGUI(root)
    root.mainloop()
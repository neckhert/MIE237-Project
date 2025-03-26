from tkinter import Tk
from ui.consent_window import ConsentWindow
from ui.test_interface import TestInterface
import customtkinter as ctk


def main():
    # Set the appearance mode to "Dark" or "Light"
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")  # Set the color theme

    root = ctk.CTk()
    root.title("237 Stats Project")
    root.geometry("800x600")

    def switch_to_test(user_id):
        for widget in root.winfo_children():
            widget.destroy()
        test_interface = TestInterface(root, user_id, switch_to_main_menu)
        test_interface.pack(fill="both", expand=True)

    def switch_to_main_menu():
        for widget in root.winfo_children():
            widget.destroy()
        consent_window = ctk.CTkFrame(root)
        ctk.CTkLabel(consent_window, text="Do you consent to participate?", font=(
            "Arial", 16)).pack(pady=20)
        user_id_entry = ctk.CTkEntry(
            consent_window, placeholder_text="Enter your User ID")
        user_id_entry.pack(pady=10)
        ctk.CTkButton(consent_window, text="I Consent", command=lambda: switch_to_test(
            user_id_entry.get())).pack(pady=20)
        consent_window.pack(fill="both", expand=True)

    switch_to_main_menu()
    root.mainloop()


if __name__ == "__main__":
    main()
# TODO Button sizes
# ENd last video after voting
# Frame rate
# fix text
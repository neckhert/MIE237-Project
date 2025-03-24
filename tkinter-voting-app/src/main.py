from tkinter import Tk
from ui.consent_window import ConsentWindow
from ui.test_interface import TestInterface


def main():
    root = Tk()
    root.title("Voting App")
    root.geometry("800x600")

    def switch_to_test(user_id):
        # Clear the current window and load the TestInterface
        for widget in root.winfo_children():
            widget.destroy()
        test_interface = TestInterface(root, user_id, switch_to_main_menu)
        test_interface.pack(fill="both", expand=True)

    def switch_to_main_menu():
        # Clear the current window and reload the ConsentWindow
        for widget in root.winfo_children():
            widget.destroy()
        consent_window = ConsentWindow(root, switch_to_test)
        consent_window.pack(fill="both", expand=True)

    # Start with the ConsentWindow
    switch_to_main_menu()

    root.mainloop()


if __name__ == "__main__":
    main()

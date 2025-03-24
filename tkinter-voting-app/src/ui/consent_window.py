from tkinter import Frame, Label, Entry, Button


class ConsentWindow(Frame):
    def __init__(self, parent, switch_to_test):
        super().__init__(parent)
        self.switch_to_test = switch_to_test

        # Add a label for the consent message
        Label(self, text="Please consent to participate in the study.",
              font=("Arial", 16)).pack(pady=20)

        # Add a field to enter user ID
        Label(self, text="Enter your User ID:",
              font=("Arial", 12)).pack(pady=10)
        self.user_id_entry = Entry(self)
        self.user_id_entry.pack(pady=10)

        # Add a button to proceed
        Button(self, text="I Consent", command=self.proceed).pack(pady=10)

    def proceed(self):
        user_id = self.user_id_entry.get()
        if user_id.strip():
            self.switch_to_test(user_id)
        else:
            Label(self, text="User ID cannot be empty!",
                  fg="red", font=("Arial", 10)).pack(pady=5)

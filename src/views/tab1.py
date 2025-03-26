from tkinter import Frame, Label, Entry, Button, StringVar, messagebox, ttk
import requests

class Tab1(Frame):
    def __init__(self, parent, validate_cookie_callback):
        super().__init__(parent)
        self.validate_cookie_callback = validate_cookie_callback

        self.cookie_var = StringVar()

        Label(self, text="Enter Cookie:").pack(pady=10)
        Entry(self, textvariable=self.cookie_var).pack(pady=10)
        Button(self, text="Validate", command=self.validate_cookie).pack(pady=10)

    def validate_cookie(self):
        cookie = self.cookie_var.get()
        if self.validate_cookie_callback(cookie):
            self.master.select(1)  # Move to the second tab if the cookie is valid
        else:
            messagebox.showerror("Error", "Invalid cookie. Please try again.")
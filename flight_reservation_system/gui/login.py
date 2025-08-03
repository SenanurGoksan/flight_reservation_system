import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from gui.registration import RegistrationWindow
from gui.user_window import UserWindow
from gui.admin_window import AdminWindow
from database import conn, cursor

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")

        tk.Label(self, text="Select User Type:").pack(pady=10)
        self.user_type = ttk.Combobox(self, values=["User", "Admin"])
        self.user_type.pack()
        self.user_type.set("User")

        tk.Label(self, text="First Name:").pack(pady=5)
        self.entry_first_name = tk.Entry(self)
        self.entry_first_name.pack()

        tk.Label(self, text="Last Name:").pack(pady=5)
        self.entry_last_name = tk.Entry(self)
        self.entry_last_name.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Sign Up", command=self.sign_up).pack()

    def sign_up(self):
        RegistrationWindow()

    def login(self):
        user_type = self.user_type.get()
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()

        if not first_name or not last_name:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        cursor.execute("SELECT * FROM passengers WHERE first_name=? AND last_name=?", (first_name, last_name))
        user = cursor.fetchone()

        if not user and user_type == "User":
            messagebox.showerror("Error", "User not found. Please sign up.")
            return

        if user_type == "User":
            self.destroy()
            UserWindow(first_name, last_name)
        else:
            password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
            if password == "admin":
                self.destroy()
                AdminWindow()
            else:
                messagebox.showerror("Error", "Incorrect password")

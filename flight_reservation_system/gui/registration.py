import tkinter as tk
from tkinter import messagebox
from database import cursor, conn

class RegistrationWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Sign Up")
        self.geometry("400x300")

        tk.Label(self, text="First Name:").pack(pady=5)
        self.entry_first = tk.Entry(self)
        self.entry_first.pack()

        tk.Label(self, text="Last Name:").pack(pady=5)
        self.entry_last = tk.Entry(self)
        self.entry_last.pack()

        tk.Label(self, text="ID Number:").pack(pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=15)

    def register(self):
        fname = self.entry_first.get()
        lname = self.entry_last.get()
        id_num = self.entry_id.get()

        if not fname or not lname or not id_num:
            messagebox.showerror("Error", "All fields required.")
            return

        cursor.execute("SELECT * FROM passengers WHERE id_number=?", (id_num,))
        if cursor.fetchone():
            messagebox.showerror("Error", "User already exists.")
            return

        cursor.execute("INSERT INTO passengers (id_number, first_name, last_name) VALUES (?, ?, ?)", (id_num, fname, lname))
        conn.commit()
        messagebox.showinfo("Success", "Registration complete.")
        self.destroy()

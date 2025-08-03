import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from database import cursor, conn

class AdminWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Panel")
        self.geometry("900x500")

        tk.Label(self, text="Admin - Flight Control Panel", font=("Arial", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Flight Number", "Departure", "Arrival", "Departure Time", "Arrival Time", "Capacity", "is_domestic"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        tk.Button(self, text="Update Departure Time", command=self.update_departure).pack(pady=10)

        self.load_flights()

    def load_flights(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM flights")
        for flight in cursor.fetchall():
            self.tree.insert("", "end", values=flight)

    def update_departure(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a flight.")
            return

        flight_number = self.tree.item(selected[0], "values")[0]
        new_time = simpledialog.askstring("Update", "New departure time (YYYY-MM-DD HH:MM:SS):")
        if new_time:
            cursor.execute("UPDATE flights SET departure_time=? WHERE flight_number=?", (new_time, flight_number))
            conn.commit()
            messagebox.showinfo("Success", "Flight updated.")
            self.load_flights()

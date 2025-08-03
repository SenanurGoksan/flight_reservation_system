import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from gui.reservation_window import ReservationWindow
from database import cursor

class UserWindow(tk.Tk):
    def __init__(self, first_name, last_name):
        super().__init__()
        self.title("User Dashboard")
        self.geometry("800x500")
        self.first_name = first_name
        self.last_name = last_name

        tk.Label(self, text=f"Welcome {first_name} {last_name}!", font=("Arial", 14)).pack(pady=10)

        self.flight_type = ttk.Combobox(self, values=["Domestic", "International"])
        self.flight_type.set("Domestic")
        self.flight_type.pack(pady=5)
        self.flight_type.bind("<<ComboboxSelected>>", self.load_flights)

        self.tree = ttk.Treeview(self, columns=("Flight Number", "Departure", "Arrival", "Departure Time", "Arrival Time", "Capacity"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        self.reserve_btn = tk.Button(self, text="Make Reservation", command=self.open_reservation)
        self.reserve_btn.pack(pady=10)

        self.load_flights()

    def load_flights(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        is_domestic = 1 if self.flight_type.get() == "Domestic" else 0
        cursor.execute("SELECT * FROM flights WHERE is_domestic=?", (is_domestic,))
        for flight in cursor.fetchall():
            self.tree.insert("", "end", values=flight)

    def open_reservation(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a flight.")
            return

        flight_number = self.tree.item(selected[0], "values")[0]
        ReservationWindow(flight_number, self.first_name, self.last_name)

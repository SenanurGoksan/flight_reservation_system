import tkinter as tk
from tkinter import simpledialog, messagebox
from models import FlightWithSeats
from database import cursor, conn
import random

class ReservationWindow(tk.Toplevel):
    def __init__(self, flight_number, first_name, last_name):
        super().__init__()
        self.title("Reservation")
        self.geometry("400x300")

        self.flight_number = flight_number
        self.first_name = first_name
        self.last_name = last_name

        tk.Label(self, text=f"Flight: {flight_number}").pack(pady=5)
        tk.Label(self, text=f"Passenger: {first_name} {last_name}").pack(pady=5)

        tk.Label(self, text="Seat Class (Economy/Business):").pack()
        self.seat_class_entry = tk.Entry(self)
        self.seat_class_entry.pack(pady=5)

        tk.Button(self, text="Reserve", command=self.reserve).pack(pady=10)

    def reserve(self):
        seat_class = self.seat_class_entry.get().capitalize()
        if seat_class not in ["Economy", "Business"]:
            messagebox.showerror("Error", "Invalid seat class.")
            return

        cursor.execute("SELECT * FROM flights WHERE flight_number=?", (self.flight_number,))
        flight = cursor.fetchone()

        if not flight:
            messagebox.showerror("Error", "Flight not found.")
            return

        flight_obj = FlightWithSeats(*flight, num_business_seats=10, num_economy_seats=20)
        available = flight_obj.get_available_seats(seat_class)

        if not available:
            messagebox.showerror("Error", "No available seats.")
            return

        seat_number = f"{seat_class[0]}{random.randint(1, 50)}"
        flight_obj.reserve_seat(seat_class, seat_number)

        cursor.execute(
            "INSERT INTO reservations (flight_number, passenger_first_name, passenger_last_name, seat_class, seat_number) VALUES (?, ?, ?, ?, ?)",
            (self.flight_number, self.first_name, self.last_name, seat_class, seat_number)
        )
        conn.commit()

        messagebox.showinfo("Success", f"Seat {seat_number} reserved.")
        self.destroy()

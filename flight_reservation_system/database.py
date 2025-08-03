import sqlite3

conn = sqlite3.connect("havaalani10.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passengers (
        id_number TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        flight_number TEXT PRIMARY KEY,
        departure_airport_code TEXT,
        arrival_airport_code TEXT,
        departure_time TEXT,
        arrival_time TEXT,
        capacity INTEGER,
        is_domestic INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT,
        passenger_first_name TEXT,
        passenger_last_name TEXT,
        seat_class TEXT,
        seat_number TEXT,
        FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
    )
''')

# Örnek uçuş verileri
domestic_flights = [
    ("TK101", "IST", "ADB", "2023-02-01 08:00:00", "2023-02-01 09:30:00", 150),
    ("TK102", "IST", "ESB", "2023-02-02 10:00:00", "2023-02-02 11:30:00", 120),
    ("TK103", "ANK", "AYT", "2023-02-03 12:00:00", "2023-02-03 14:00:00", 180),
    ("TK104", "ADB", "IST", "2023-02-04 15:00:00", "2023-02-04 16:30:00", 160),
    ("TK105", "ESB", "ANK", "2023-02-05 18:00:00", "2023-02-05 19:30:00", 200)
]

international_flights = [
    ("TK201", "IST", "JFK", "2023-03-01 08:00:00", "2023-03-01 14:00:00", 200),
    ("TK202", "IST", "LHR", "2023-03-02 10:00:00", "2023-03-02 15:30:00", 150),
    ("TK203", "IST", "CDG", "2023-03-03 12:00:00", "2023-03-03 16:30:00", 180),
    ("TK204", "JFK", "IST", "2023-03-04 15:00:00", "2023-03-04 20:30:00", 160),
    ("TK205", "LHR", "IST", "2023-03-05 18:00:00", "2023-03-05 22:30:00", 200)
]

for flight in domestic_flights:
    cursor.execute("INSERT OR IGNORE INTO flights VALUES (?, ?, ?, ?, ?, ?, 1)", flight)

for flight in international_flights:
    cursor.execute("INSERT OR IGNORE INTO flights VALUES (?, ?, ?, ?, ?, ?, 0)", flight)

conn.commit()

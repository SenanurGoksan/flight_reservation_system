from abc import ABC, abstractmethod

class Flight:
    def __init__(self, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, capacity, is_domestic):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.capacity = capacity
        self.is_domestic = is_domestic

class DomesticFlight(Flight):
    def __init__(self, *args):
        super().__init__(*args, True)

class InternationalFlight(Flight):
    def __init__(self, *args):
        super().__init__(*args, False)

class Passenger:
    def __init__(self, first_name, last_name, id_number):
        self.first_name = first_name
        self.last_name = last_name
        self._id_number = id_number

    def get_id_number(self):
        return self._id_number

    def set_id_number(self, new_id_number):
        self._id_number = new_id_number

class Reservation:
    def __init__(self, flight_number, first_name, last_name, seat_class, seat_number):
        self.flight_number = flight_number
        self.first_name = first_name
        self.last_name = last_name
        self.seat_class = seat_class
        self.seat_number = seat_number

class Seat(ABC):
    @abstractmethod
    def __init__(self, seat_number, seat_class, is_reserved=False):
        self._seat_number = seat_number
        self._seat_class = seat_class
        self._is_reserved = is_reserved

    @property
    def seat_number(self):
        return self._seat_number

    @property
    def seat_class(self):
        return self._seat_class

    @property
    def is_reserved(self):
        return self._is_reserved

    def reserve_seat(self):
        self._is_reserved = True

class EconomySeat(Seat):
    def __init__(self, seat_number, is_reserved=False):
        super().__init__(seat_number, "Economy", is_reserved)

class BusinessSeat(Seat):
    def __init__(self, seat_number, is_reserved=False):
        super().__init__(seat_number, "Business", is_reserved)

class FlightWithSeats(Flight):
    def __init__(self, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, capacity,
                 is_domestic, num_business_seats, num_economy_seats):
        super().__init__(flight_number, departure_airport, arrival_airport, departure_time, arrival_time, capacity,
                         is_domestic)
        self.business_seats = [BusinessSeat(f"B{num}") for num in range(1, num_business_seats + 1)]
        self.economy_seats = [EconomySeat(f"E{num}") for num in range(1, num_economy_seats + 1)]

    def get_available_seats(self, seat_class):
        if seat_class == "Business":
            return [seat for seat in self.business_seats if not seat.is_reserved]
        elif seat_class == "Economy":
            return [seat for seat in self.economy_seats if not seat.is_reserved]
        return []

    def reserve_seat(self, seat_class, seat_number):
        seats = self.business_seats if seat_class == "Business" else self.economy_seats
        for seat in seats:
            if seat.seat_number == seat_number and not seat.is_reserved:
                seat.reserve_seat()
                return True
        return False

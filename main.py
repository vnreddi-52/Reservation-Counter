from enum import Enum
import uuid
import json
import os

COACH_FARE          = 850 
CANCELLATION_CHARGE = 60 
WAITLIST_CAPACITY   = 4 
AADHAAR_LENGTH      = 12 
MIN_NAME_LENGTH     = 3 
WAITING_LIST=[]

DATA_FILE = "reservations.json"
# setting up coach

print("Hey Clerk, set up a coach")

coach_name = input("Enter coach name: ")
num_cabins = int(input("Enter the number of cabins: "))
num_seats = int(input("Enter the number of seats: "))

dict_coach = {}

 
for i in range(1, num_cabins + 1):
    dict_seat = {}
    for j in range(1, num_seats + 1):
        dict_seat[str(j)] = None
    dict_coach[f"C{i}"] = dict_seat


class BookingError(Exception):
    pass

class ValidationError(BookingError):
    pass

class SeatUnavailableError(BookingError):
    pass

train_obj=[]
class Train:
    def __init__(self, seats, waiting_list, tickets):
        self.seats = seats
        self.waiting_list = waiting_list
        self.tickets = tickets

    def book_ticket(self, ticket):
        self.tickets.append(ticket)

    def cancel_ticket(self, pnr):
        return self.cancel_ticket(pnr)

seat_obj=[]
class Seat:
    def __init__(self, coach, cabin, seat_no, passenger,pnr):
        self.coach = coach
        self.cabin = cabin
        self.seat_no = str(seat_no)
        self.passengers = passenger
        self.PNR = pnr

    def __str__(self):
        return f"{self.coach} {self.cabin} {self.seat_no} {self.passengers} {self.PNR}"


TicketHolding_obj=[]
class TicketHolding:
    def __init__(self, passenger, status, seat, fare, refund, pnr):
        self.passenger = passenger
        self.status = status
        self.seat = seat
        self.fare = fare
        self.refund = refund
        self.pnr = pnr

    def __str__(self):
        return f"{self.passenger.name} {self.status} {self.status} {self.seat} {self.fare} {self.refund}"

passenger_obj=[]
class Passenger:
    def __init__(self, name, aadhaar, age, gender):
        self.name = name
        self.aadhaar = aadhaar
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name} {self.aadhaar} {self.age} {self.gender}"

def get_integer_input(msg, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(msg))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid integer between {min_value} and {max_value}.")

def get_name_input(msg):
    while True:
        name = input(msg).strip()
        if len(name) >= MIN_NAME_LENGTH:
            return name
        print(f"Name must be at least 3 characters long")

def get_aadhaar_input(msg):
    while True:
        aadhaar = input(msg).strip()
        if len(aadhaar) == AADHAAR_LENGTH and aadhaar.isdigit():
            return aadhaar
        print("Aadhaar number must be 12 digits long")

def get_choice_input(msg, choices):
    allowed = [str(choice).upper() for choice in choices]
    while True:
        value = input(msg).strip().upper()
        if value in allowed:
            return value
        print("Invalid choice. Choose from:", ", ".join(allowed))


def generate_pnr():
    return str(uuid.uuid4()).upper()
# display menu

def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read reservations.json.")
        return []

def save_data(tickets):
    data = {
        "coach_name": coach_name,
        "num_cabins": num_cabins,
        "num_seats": num_seats,
        "tickets": []
    }

    for ticket in tickets:
        seat_data = None
        if ticket.seat is not None:
            seat_data = {
                "coach": ticket.seat.coach,
                "cabin": ticket.seat.cabin,
                "seat_no": ticket.seat.seat_no
            }

        data["tickets"].append({
            "passenger": {
                "name": ticket.passenger.name,
                "aadhaar": ticket.passenger.aadhaar,
                "age": ticket.passenger.age,
                "gender": ticket.passenger.gender
            },
            "status": ticket.status,
            "seat": seat_data,
            "fare": ticket.fare,
            "refund": ticket.refund,
            "pnr": ticket.pnr
        })

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except OSError:
        print("Warning: Could not save reservations.")

def load_data():
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read reservations.json.")
        return
    
    if (
        data.get("coach_name") != coach_name
        or data.get("num_cabins") != num_cabins
        or data.get("num_seats") != num_seats
    ):
        print("Saved reservations belong to a different coach configuration.")
        print("Starting with an empty reservation list.")
        return

    for item in data.get("tickets", []):
        p = item["passenger"]
        passenger = Passenger(
            p["name"], p["aadhaar"], p["age"], p["gender"]
        )

        ticket_seat = None
        seat_data = item.get("seat")

        if seat_data is not None:
            cabin = seat_data["cabin"]
            seat_no = str(seat_data["seat_no"])

            if (
                cabin in dict_coach
                and seat_no in dict_coach[cabin]
                and dict_coach[cabin][seat_no] is None
                and item["status"] == "Confirmed"
            ):
                ticket_seat = Seat(
                    seat_data["coach"], cabin, seat_no,
                    passenger.name, item["pnr"]
                )
                dict_coach[cabin][seat_no] = ticket_seat
                seat_obj.append(ticket_seat)

        ticket = TicketHolding(
            passenger,
            item["status"],
            ticket_seat,
            item["fare"],
            item["refund"],
            item["pnr"]
        )

        passenger_obj.append(passenger)
        TicketHolding_obj.append(ticket)

        if ticket.status == "Waiting":
            WAITING_LIST.append(passenger)


def write_text_files():
    try:
        with open("passenger.txt", "w") as file:
            for passenger in passenger_obj:
                file.write(str(passenger) + "\n")

        with open("seats.txt", "w") as file:
            for seat in seat_obj:
                file.write(str(seat) + "\n")

        with open("waiting_list.txt", "w") as file:
            for passenger in WAITING_LIST:
                file.write(str(passenger) + "\n")

        with open("ticket.txt", "w") as file:
            for ticket in TicketHolding_obj:
                file.write(str(ticket) + "\n")

    except OSError:
        print("Warning: Could not update one or more text files.")
    

def find_seat_by_pnr(pnr):
    for ticket in TicketHolding_obj:
        if ticket.pnr == pnr:
            return ticket
    return None

def find_empty_seat(cabin):
    for seat_no, seat in dict_coach[cabin].items():
        if seat is None:
            return seat_no
    return None

def get_seat_for_ticket(ticket):
    if ticket.seat is not None:
        return (
            ticket.seat.coach,
            ticket.seat.cabin,
            ticket.seat.seat_no
        )
    return None

def find_ticket_by_pnr(pnr):
    pnr = pnr.strip().upper()
    for ticket in TicketHolding_obj:
        if ticket.pnr == pnr:
            return ticket
    return None

def book_ticket():
    name = get_name_input("Enter your name: ")
    aadhaar = get_aadhaar_input("Enter your Aadhaar number: ")
    age = get_integer_input("Enter your age: ", min_value=0)
    gender = get_choice_input("Enter gender (M/F): ", ["M", "F"])

    cabin = get_choice_input(
        f"Enter cabin preference ({', '.join(dict_coach.keys())}): ",
        dict_coach.keys()
    )

    passenger = Passenger(name, aadhaar, age, gender)

    for existing in TicketHolding_obj:
        if (
            existing.passenger.aadhaar == aadhaar
            and existing.status in ("Confirmed", "Waiting")
        ):
            print("This Aadhaar already has an active booking.")
            return

    pnr = generate_pnr()
    seat_no = find_empty_seat(cabin)

    if seat_no is not None:
        seat = Seat(coach_name, cabin, seat_no, passenger.name, pnr)
        dict_coach[cabin][seat_no] = seat
        seat_obj.append(seat)
        status = "Confirmed"
        print("Ticket booked successfully!")
    else:
        if len(WAITING_LIST) >= WAITLIST_CAPACITY:
            print("Cabin is full and the waiting list is also full.")
            return

        seat = None
        WAITING_LIST.append(passenger)
        status = "Waiting"
        print("Cabin is full. Passenger added to the waiting list.")

    ticket = TicketHolding(
        passenger, status, seat, COACH_FARE, 0, pnr
    )

    passenger_obj.append(passenger)
    TicketHolding_obj.append(ticket)

    print("Payment recorded.")
    print("Your PNR is:", pnr)
    print("Booking status:", status)

    save_data(TicketHolding_obj)
    write_text_files()

def cancel_ticket(pnr=None):
    if pnr is None:
        pnr = input("Enter PNR to cancel: ").strip().upper()

    ticket = find_ticket_by_pnr(pnr)

    if ticket is None:
        print("Ticket not found. Please check your PNR.")
        return
    
    if ticket.status not in ("Confirmed", "Waiting"):
        print("This ticket is already cancelled.")
        return

    if ticket.status == "Waiting":
        ticket.status = "Cancelled"
        ticket.refund = ticket.fare - CANCELLATION_CHARGE

        if ticket.passenger in WAITING_LIST:
            WAITING_LIST.remove(ticket.passenger)

        print("Waiting-list ticket cancelled.")
    else:
        old_seat = ticket.seat
        cabin = old_seat.cabin
        seat_no = old_seat.seat_no

        dict_coach[cabin][seat_no] = None

        if old_seat in seat_obj:
            seat_obj.remove(old_seat)

        ticket.status = "Cancelled"
        ticket.refund = max(0, ticket.fare - CANCELLATION_CHARGE)
        ticket.seat = None

        print("Ticket cancelled successfully.")
        print("Refund amount:", ticket.refund)

        while WAITING_LIST:
            next_passenger = WAITING_LIST.pop(0)

            waiting_ticket = next(
                (
                    t for t in TicketHolding_obj
                    if t.passenger is next_passenger
                    and t.status == "Waiting"
                ),
                None
            )

            if waiting_ticket is None:
                continue

            new_seat = Seat(
                coach_name, cabin, seat_no,
                next_passenger.name, waiting_ticket.pnr
            )

            dict_coach[cabin][seat_no] = new_seat
            seat_obj.append(new_seat)

            waiting_ticket.seat = new_seat
            waiting_ticket.status = "Confirmed"

            print(
                f"{next_passenger.name} promoted from waiting list. "
                f"New seat: {cabin}-{seat_no}"
            )
            break

    save_data(TicketHolding_obj)
    write_text_files()


def display_seats():
    print("\n--- Seat Status ---")
    for cabin, seats in dict_coach.items():
        print(f"\n{cabin}:")
        for seat_no, seat in seats.items():
            if seat is None:
                print(f"  Seat {seat_no}: Available")
            else:
                print(
                    f"  Seat {seat_no}: Occupied by "
                    f"{seat.passengers} (PNR: {seat.PNR})"
                )


def display_waiting_list():
    print("\n--- Waiting List ---")

    waiting_tickets = [
        ticket for ticket in TicketHolding_obj
        if ticket.status == "Waiting"
    ]

    if not waiting_tickets:
        print("Waiting list is empty.")
        return

    for index, ticket in enumerate(waiting_tickets, start=1):
        print(
            f"{index}. {ticket.passenger.name} | "
            f"PNR: {ticket.pnr}"
        )


def display_ticket():
    pnr = input("Enter PNR: ").strip().upper()
    ticket = find_ticket_by_pnr(pnr)

    if ticket is None:
        print("Ticket not found.")
        return

    print("\n--- Ticket Details ---")
    print(ticket)


def main():
    load_data()

    train = Train(seat_obj, WAITING_LIST, TicketHolding_obj)
    train_obj.append(train)

    while True:
        print("\nMenu")
        print("1.Book a ticket")
        print("2.Cancel a ticket")
        print("3.Display seats")
        print("4.Display waiting list")
        print("5.View ticket using PNR")
        print("6.Exit")

        choice = get_integer_input("Enter your choice: ", 1, 6)

        if choice == 1:
            book_ticket()
        elif choice == 2:
            cancel_ticket()
        elif choice == 3:
            display_seats()
        elif choice == 4:
            display_waiting_list()
        elif choice == 5:
            display_ticket()
        elif choice == 6:
            save_data(TicketHolding_obj)
            write_text_files()
            print("Exiting reservation system...")
            break

if __name__=="__main__":
    main()







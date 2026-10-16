
from enum import Enum
import uuid
# import json
# import os

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

# need to create a dictionary of dictionaries for S1 - C1, C2, C3, C4 - then no of seats another dict , 1, 2,3 4, they are keys , "1":passenger obj must be passed
# while booking ticket , check if there is any place or value for seats is empty , then put passenger object there 
for i in range(1, num_cabins + 1):
    dict_seat = {}
    for j in range(1, num_seats + 1):
        dict_seat[str(j)] = None
    dict_coach[f"C{i}"] = dict_seat


# for i,j in dict_coach.items():
#     for k,l in j.items():
#         if l is None:
#             j[k] = 1
#             break


# print(dict_coach)




# print(dict_coach)


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

    def book_ticket():
        pass

    def cancel_ticket():
        pass

seat_obj=[]
class Seat:
    def __init__(self, coach, cabin, seat_no, passenger,pnr):
        self.coach = coach
        self.cabin = cabin
        self.seat_no=seat_no
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
        return f"{self.passenger} {self.status} {self.status} {self.seat} {self.fare} {self.refund}"

passenger_obj=[]
class Passenger:
    def __init__(self, name, aadhaar, age, gender):
        self.name = name
        self.aadhaar = aadhaar
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name} {self.aadhaar} {self.age} {self.gender}"

 #Write one small function each kind of input and reuse it everywhere: one for a whole number within a range, one for a name, one for a choice from a fixed set of words, and one for an Aadhaar number. If the same asking-and-checking code appears twice in your program, it belongs in a function. 

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

def generate_pnr():
    return str(uuid.uuid4()).hes[:8]
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
    with open(DATA_FILE, "w") as file:
        json.dump(tickets, file, indent=4)

def find_seat_by_pnr(pnr):
    try:
        with open("seats.txt", "r") as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) >= 5:
                    coach, cabin, seat_no = parts[0], parts[1], parts[2]
                    saved_pnr = parts[-1]

                    if saved_pnr == pnr:
                        return coach, cabin, seat_no

    except FileNotFoundError:
        print("seats.txt file not found.")

    return None
def main():

    choice = int(input("Enter your choice: "))

    match choice:
        case 1:
            # book a ticket
            name = get_name_input("Enter your name: ")
            aadhaar = get_aadhaar_input("Enter your Aadhaar number: ")
            age = get_integer_input("Enter your age: ", min_value=0)
            gender = input("Enter your gender (M/F): ").strip().upper()
            if gender not in ['M', 'F']:
                print("Invalid gender. Please enter 'M' or 'F'.")
                return
            cabin = input("Enter your cabin preference (C1, C2, ...): ").strip().upper()
            if cabin not in dict_coach:
                print("Invalid cabin")
                return

            seat_no = None

            for i,j in dict_coach[cabin].items():
                if j is None:
                    seat_no = i
                    break

            # create objects for passenger and seat
            passenger = Passenger(name, aadhaar, age, gender)
            PNR = generate_pnr()
            passenger_obj.append(passenger)

            if seat_no is not None:
                seat = Seat(coach_name, cabin, num_seats, passenger.name, PNR)
                dict_coach[cabin][seat_no] =seat
                seat_obj.append(seat)

                status = "Confirmed"
                fare = COACH_FARE
                refund = 0

                print("Ticket Booked ")
                print("Payment done ")

            else:
                WAITING_LIST.append(passenger)
                status = "Waiting"
                fare = COACH_FARE
                refund = 0

                print("Ticket Waiting ")
                print("Payment done ")

            ticket = TicketHolding(passenger, status, seat, fare, refund, PNR)

            TicketHolding_obj.append(ticket)

            # create train object
            train = Train(seat_obj, WAITING_LIST, ticket)
            train_obj.append(train)

            with open("passenger.txt","a") as file:
                for i in passenger_obj:
                    file.write(f"{i}")

            with open("seats.txt", "a") as file:
                for i in seat_obj:
                    file.write(f"{i}")

            with open("waiting_list.txt", "a") as file:
                for i in WAITING_LIST:
                    file.write(f"{i}")

            with open("ticket.txt", "a") as file:
                for i in TicketHolding_obj:
                    file.write(f"{i}")
            
        case 2: 
            pnr = input("Enter PNR to cancel: ").strip()

            # coach, cabin, seat_no
            data = find_seat_by_pnr(pnr)
            print(data)

            print()
            # ticket_found=None
            # seat = None
            # for ticket in TicketHolding_obj:
            #     if ticket.pnr == pnr and ticket.status == "Confirmed":
            #         ticket_found = ticket
            #         break
            
            # if ticket_found is None:
            #     print("Ticket not found. Please check your PNR.")
            #     return
            # else:
            #     seat = ticket_found.seat

            #     if seat is None:
            #         print("No seat assigned to this ticket")
            #         return

                

            # seat = ticket_found.seat
            # dict_coach[seat.cabin][str(seat.seat_no)] = None
            # ticket_found.status = "Cancelled"
            # ticket_found.refund = ticket_found.fare - CANCELLATION_CHARGE

            # # waiting list
            # if WAITING_LIST:
            #     nxt_passenger = WAITING_LIST.pop(0)

            #     new_pnr = generate_pnr()

            #     new_seat = Seat(coach_name,seat.cabin, seat.seat_no, nxt_passenger, new_pnr)

            # for ticket in TicketHolding_obj:
            #     if (ticket.passenger is nxt_passenger
            #         and ticket.status == "Waiting"):

            #         ticket.status = "Confirmed"
            #         ticket.seat = new_seat
            #         ticket.refund = 0

            #         break



        case 3:
            for seat in seat_obj:
                print(seat)
            pass

        case 4:
            # display_waiting_list
            pass

        case 5:
            # enter pnr
            # for t in TicketHolding_obj:
            #     print(t)
            pass

        case _:
            print("Exited ...........")

if __name__=="__main__":
    main()
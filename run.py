import re
import datetime
from datetime import date
import sys
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

PRICES = {
    "Deluxe Double": 250,
    "Deluxe Twin": 200,
    "Standard Double": 160,
    "Standard Twin": 110,
}

ROOM_TYPE = {
    "Room type 1": "Deluxe Double",
    "Room type 2": "Deluxe Twin",
    "Room type 3": "Standard Double",
    "Room type 4": "Standard Twin",
}

WELCOME_MESSAGE = """
Welcome to the Hotel Los Santos Reservation Application.

Thank you for confiding in our establishment.

Please pick one of the following options.

1. Make a reservation

2. Room information

3. Contact details

4. Exit
"""

STANDARD_TWIN = """
Standard Twin Room.

Our standard twin room features two 110cm individual beds with a standard
bathroom with shower and bath.

Available in the room is also a sofa-bed which can fit up to two more people.

"""

STANDARD_DOUBLE = """
Standard Double Room.

Our standard double room features a single double bed which is 75” (191 cm)
long and 54” (137 cm) wide.

Room also has a bathroom with both a shower and a bath.

Available in the room is also a sofa-bed which can fit up to two more people.

"""

DELUXE_TWIN = """
Deluxe Twin Room.

Our deluxe twin room features two 130cm individual beds with a plush,
luxurious bathroom with a shower and bath.

Room also has access to a balcony off which can be seen a beautiful
view of Los Santos and the beach.

Available in the room is also a sofa-bed which can fit up to two more people.

"""

DELUXE_DOUBLE = """
Deluxe Double Room.

Our deluxe double room features a king size double bed with a plush,
luxurious bathroom with a shower and bath.

Room also has access to a balcony off which can be seen a
beautiful view of Los Santos and the beach.

Available in the room is also a sofa-bed which can fit up to two more people.

"""

CONTACT = """
Los Santos Hotel can be contacted via 0034 987 654 321.

Telephone lines are open between 10AM and 9PM.

Please note that no reservations can be taken directly over phone.

All reservations must be carried out via the Los Santos Hotel
Reservation Application.

For any further questions, do not hesitate to send us
an e-mail at info@lossantoshotel.com.

We thank you for your interest in our establishment.
"""

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# This variable refers to the Google Sheets document
reserves = GSPREAD_CLIENT.open("los_santos_hotel").worksheet("reserves")

# Date variables are for the check-in and check-out functions
present_date = date.today()
max_date = "01/01/2023"
max_check_out_date = datetime.datetime.strptime(max_date, "%d/%m/%Y").date()


def room_info():
    """
    Displays brief information about the amenities available to the client
    """
    print(colored(("------ LOS SANTOS HOTEL ROOMS INFO ------"), "cyan"))
    print(colored((STANDARD_TWIN), "cyan"))
    print(colored((STANDARD_DOUBLE), "cyan"))
    print(colored((DELUXE_TWIN), "cyan"))
    print(colored((DELUXE_DOUBLE), "cyan"))

    input("Press any key to return to main menu.")


def contact_details():
    """
    Displays the contact details for the user to be able to access
    """
    print(colored((CONTACT), "cyan"))

    input("Press any key to return to main menu.")


def full_name():
    """
    Takes the full name and details of the client
    """
    while True:

        print(colored(("Please enter your full name\n"), "cyan"))
        print(colored(("For example: Tarik Khan \n"), "cyan"))

        customer_name = input("Enter your full name here: \n")
        print(colored((f"You have entered '{customer_name}'\n"), "cyan"))

        if validate_full_name(customer_name):
            break

    return customer_name


def validate_full_name(customer_name):
    """
    Validates the input entered as the customers full name
    making sure that there are no numbers or symbols used.
    Code inspired by https://www.geeksforgeeks.org/
    name-validation-using-ignorecase-in-python-regex/
    """

    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

    res = regex_name.search(customer_name)

    if res:
        print(colored(("Updating your reservation... \n"), "cyan"))
        return True
    else:
        print(colored(("Invalid. Please enter a valid name.\n"), "red"))
        return False


def customer_age():
    """
    Receives input of the age of the customer, turns input into
    an integer and also checks whether the user is over 18 to
    be able to make a reservation.
    """
    while True:
        try:
            print(colored(("How old are you?\n"), "cyan"))
            age = int(input("Please enter your age: \n"))
            # Validates user input for age
            if age <= 18:
                print(colored(
                    ("You must be over 18 to make a reservation.\n"), "red"))
            elif age >= 101:
                print(colored(("Invalid age input.\n"), "red"))
            else:
                print(colored((f"You are {age} years old.\n"), "cyan"))
                print(colored(("Updating your reservation...\n"), "cyan"))
                break
        except ValueError:
            print(colored(("Invalid age input. Use numbers only.\n"), "red"))

    return age


def guest_quantity():
    """
    Takes in input for the number of guests
    """
    while True:
        try:
            print(colored(
                ("Please indicate the numbers of guests staying.\n"), "cyan"))
            print(colored(
                ("Enter the amount as a digit, for example: 4\n"), "cyan"))
            print(colored(("Maximum 4 people per room.\n"), "cyan"))
            guest_number = int(input("Amount guests staying: \n"))
            # Validates user input for guest quantity
            if guest_number > 4:
                print(colored(("Only 4 persons maximum per room.\n"), "red"))
                continue
            elif guest_number <= 0:
                print(colored(("Invalid number input.\n"), "red"))
                continue
            else:
                print(colored(
                    (f"You have entered {guest_number} guests.\n"), "cyan"))
                print(colored(("Updating your reservation...\n"), "cyan"))
                break
        except ValueError:
            print(colored(
                ("Invalid input. Please only use numbers.\n"), "red"))
            continue
    return guest_number


def customer_email_address():
    """
    For taking in the details of a clients email address
    """
    while True:

        print(colored(("Please provide an e-mail address.\n"), "cyan"))
        print(colored(("Please use correct characters.\n"), "cyan"))
        print(colored(("For example: email@domain.com\n"), "cyan"))

        email = input("Your e-mail address: \n")

        if validate_email_address(email):
            break

    return email


def validate_email_address(email):
    """
    Checks whether user email input is valid or invalid.
    Code inspired by the validate_full_name function.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        print(colored(("E-mail address is valid.\n"), "cyan"))
        print(colored((f"Your e-mail address is {email}.\n"), "cyan"))
        print(colored(("Updating your reservation...\n"), "cyan"))
        return True

    else:
        print(colored(("Invalid e-mail, please try again.\n"), "red"))
        return False


def room_type():
    """
    Collects input for whether user chooses standard twin,
    double or deluxe twin, double.
    """
    while True:
        try:
            print(
                colored(
                    (
                        "Please indicate room type entering 1, 2, 3 or 4.\n"
                    ),
                    "cyan",
                )
            )
            print(colored(("1. Deluxe Double. 2. Deluxe Twin."), "cyan"))
            print(colored(("3. Standard Double. 4. Standard Twin.\n"), "cyan"))

            room_choice = int(input("Write your room choice here: \n"))

            if room_choice == 1:
                selected_room = "Deluxe Double"
                break
            elif room_choice == 2:
                selected_room = "Deluxe Twin"
                break
            elif room_choice == 3:
                selected_room = "Standard Double"
                break
            elif room_choice == 4:
                selected_room = "Standard Twin"
                break
            elif room_choice >= 5:
                print(colored(("Invalid choice input.\n"), "red"))
                continue
            else:
                print(colored(("Invalid input.\n"), "red"))
                continue
        except ValueError:
            print(colored(("Please use only numbers.\n"), "red"))
            continue
    if selected_room:
        price = PRICES[selected_room]
    print(colored((f"{selected_room} option selected.\n"), "cyan"))
    print(colored((f"Price is {price}€.\n"), "cyan"))
    print(colored(("This price is per night of your stay."), "cyan"))
    print(colored(("Updating your reservation...\n"), "cyan"))

    return room_choice


def customer_check_in_date():
    """
    Collects input from user for their check-in date
    """

    while True:
        print(colored(("Please use format dd/mm/yyyy for dates\n"), "cyan"))
        input_date_check_in = input("Indicate your check-in date here: \n")

        try:
            # Converts user input into a datetime
            check_in_date = datetime.datetime.strptime(
                input_date_check_in, "%d/%m/%Y"
            ).date()
            print(colored((f"You have entered {check_in_date}.\n"), "cyan"))
            print(colored(("Updating your reservation...\n"), "cyan"))
            # Validates user input for check-in date
            if check_in_date <= present_date:
                print(colored(
                    ("Invalid check-in date. Please try again.\n"), "red"))
                continue
            elif check_in_date >= max_check_out_date:
                print(colored(
                    ("Invalid check-in date. Please try again.\n"), "red"))
                continue
            else:
                break
        except ValueError:
            print(colored(
                ("Invalid check-in date. Please try again.\n"), "red"))
            continue

    return check_in_date


def customer_check_out_date(check_in_date):
    """
    Collects input from user for their check-out date
    Validates user input for check-out date
    """

    while True:
        print(colored(("Please use format dd/mm/yyyy for dates\n"), "cyan"))
        input_date_check_out = input("Indicate your check-out date here: \n")

        try:
            # Converts user input into a datetime
            check_out_date = datetime.datetime.strptime(
                input_date_check_out, "%d/%m/%Y"
            ).date()
            print(colored((f"You have entered {check_out_date}.\n"), "cyan"))
            print(colored(("Updating your reservation...\n"), "cyan"))
            # Validation for check-out date input
            if check_out_date <= check_in_date:
                print(colored(
                    ("Invalid check-out date. Please try again.\n"), "red"))
                continue
            elif check_out_date >= max_check_out_date:
                print(colored(
                    ("Invalid check-out date. Please try again.\n"), "red"))
                continue
            else:
                break
        except ValueError:
            print(colored(
                ("Invalid check-out date. Please try again.\n"), "red"))
            continue

    return check_out_date


def calculate_total_price(room_choice, check_out_date, check_in_date):
    """
    Calculates the total price of the stay based on
    user input in the check-in and -out field.
    """
    num_days = 0
    total_price = 0

    if room_choice == 1:
        selected_room = "Deluxe Double"
    elif room_choice == 2:
        selected_room = "Deluxe Twin"
    elif room_choice == 3:
        selected_room = "Standard Double"
    elif room_choice == 4:
        selected_room = "Standard Twin"

    if selected_room:
        price = PRICES[selected_room]
    num_days = (check_out_date - check_in_date).days
    total_price = num_days * price
    print(colored(
        (f"The total price for your stay is {total_price}€.\n"), "cyan"))
    print(colored(("Updating your reservation...\n"), "cyan"))

    return num_days, total_price


def confirm_reservation(
    cust_name,
    cust_age,
    no_of_guest,
    cust_email,
    type_of_room,
    date_check_in,
    date_check_out,
    num_days,
    total_price,
):
    """
    Accumulates customer information items, presents it as a list, prints
    a confirmation of the reservation for the client to see and appends it
    onto a google sheets row for reference.
    Learned how to append a worksheet via Code Institute, source:
    https://github.com/keironchaudhry/love-sandwiches/blob/main/run.py
    """

    reservation_items = [
        cust_name,
        cust_age,
        no_of_guest,
        cust_email,
        type_of_room,
        date_check_in.strftime("%d/%m/%Y"),
        date_check_out.strftime("%d/%m/%Y"),
        total_price,
    ]
    worksheet_to_update = reserves
    worksheet_to_update.append_row(reservation_items)

    user_information_reservation = f"""
    The following is confirmation of your reservation details:\n
    Room numbers are as follows:\n
    1. Deluxe Double, 2. Deluxe Twin, 3. Standard Double, 4. Standard Twin.\n
    Name: {cust_name}
    Age: {cust_age}
    Guest(s): {no_of_guest}
    Email address: {cust_email}
    Room: {type_of_room}
    Check-in date: {date_check_in}
    Check-out date: {date_check_out}
    Total price for stay: {total_price}.00€\n
    """

    print(colored((user_information_reservation), "green"))

    print(colored(
        ("Thank you for confiding in Hotel Los Santos.\n"), "cyan"))
    print(colored(
        ("Application now closing.\n"), "blue"))

    sys.exit()


def program():
    """
    Runs all the previous functions for the program
    """
    cust_name = full_name()
    cust_age = customer_age()
    no_of_guest = guest_quantity()
    cust_email = customer_email_address()
    type_of_room = room_type()
    date_check_in = customer_check_in_date()
    date_check_out = customer_check_out_date(date_check_in)
    num_days, total_price = calculate_total_price(
        type_of_room, date_check_out, date_check_in
    )
    confirm_reservation(
        cust_name,
        cust_age,
        no_of_guest,
        cust_email,
        type_of_room,
        date_check_in,
        date_check_out,
        num_days,
        total_price,
    )


def main():
    """
    The landing page to welcome the user upon initiation of the application
    """
    while True:
        try:
            print(colored((WELCOME_MESSAGE), "cyan"))
            user_menu_choice = int(input("Enter here your input: \n"))
            if user_menu_choice == 1:
                print(program())
            elif user_menu_choice == 2:
                print(room_info())
            elif user_menu_choice == 3:
                print(contact_details())
            elif user_menu_choice == 4:
                print(
                    colored(
                        ("Application now closing. Thank you."),
                        "blue",
                    )
                )
                sys.exit()
            elif user_menu_choice >= 5:
                print(colored(("Invalid key. Please try again.\n"), "red"))
                main()
            elif user_menu_choice >= 0:
                print(colored(("Invalid key. Please try again.\n"), "red"))
                main()
        except ValueError:
            print(colored(("Invalid key. Please try again.\n"), "red"))
            continue


if __name__ == "__main__":
    main()

import re
import datetime
import sys
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

PRICES = {
    "Deluxe Double": 250,
    "Deluxe Twin": 200,
    "Standard Double": 160,
    "Standard Twin": 110
}

WELCOME_MESSAGE = """
Welcome to the Hotel Los Santos Reservation Application. 

Thank you for confiding in our establishment.

1. Make a reservation

2. Room information

3. Contact details

4. Exit
"""

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


reservations = GSPREAD_CLIENT.open('los_santos_hotel').worksheet('reservations')


def welcome_page():
    """
    The landing page to welcome the user upon initiation of the application
    """
    print(WELCOME_MESSAGE)
    user_menu_choice = int(input("Please enter one of the above options: \n"))

    if user_menu_choice == 1:
        print(main())
    
    elif user_menu_choice == 2:
        print(room_info())
    
    elif user_menu_choice == 3:
        print(contact_details())

    elif user_menu_choice == 4:
        exit()


def full_name():
    """
    Takes the full name and details of the client
    """
    while True: 

        print("Please enter your full name\n")
        print("For example: Tarik Khan \n")

        customer_name = input("Enter your full name here: \n")
        print(f"You have entered '{customer_name}'\n")

        if validate_full_name(customer_name):
            break


    return customer_name


def validate_full_name(customer_name):
    """
    Validates the input entered as the customers full name
    making sure that there are no numbers or symbols used.
    """

    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

    res = regex_name.search(customer_name)

    if res:
        print("Updating your reservation... \n")
        return True
    else: 
        print("Invalid. Please enter a valid name.\n")
        return False


def customer_age():
    """
    Receives input of the age of the customer, turns input into
    an integer and also checks whether the user is over 18 to
    be able to make a reservation.
    """
    while True:
        try:
            print("How old are you?\n")
            age = int(input("Please enter your age: \n"))
        except ValueError:
            print("Please enter a valid input. Use numbers only.\n")
            continue
        else:
            break

    if age <= 18:
        print("You must be over 18 to make a reservation.\n")
        customer_age()
    else: 
        print(f"You are {age} years old.\n")
        print("Updating your reservation...\n")

    return age


def guest_quantity():
    """
    Takes in input for the number of guests
    """
    while True:
        try:
            print("Please indicate the numbers of guests staying.\n")
            print("Enter the amount as a digit, for example: 4\n")
            print("Please bear in mind it is a maximum 4 people per room.\n")
            guest_number = int(input("Amount guests staying: \n"))
        except ValueError:
            print("Invalid characters. Please use only numeric digits.\n")
            continue
        else:
            break

    if guest_number > 4:
        print("Only 4 persons maximum per room.\n")

    else: 
        print(f"You have entered {guest_number} guests.\n")
        print("Updating your reservation...\n")
        
    return guest_number

def customer_email_address():
    """
    For taking in the details of a clients email address
    """

    print("Please provide us with an e-mail address for contact purposes.\n")
    print("E-mail address must be written as such: email@domain.com\n")
    email = input("Your e-mail address: \n")

    validate_email_address(email)

    return email


def validate_email_address(email):
    """
    Checks whether user email input is valid or invalid.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    
    if (re.fullmatch(regex, email)):
        print("E-mail address is valid.\n")
        print(f"Your e-mail address is {email}.\n")
        print("Updating your reservation...\n")
    
    else:
        print("Invalid e-mail, please try again.\n")
        customer_email_address()


def room_type():
    """
    Collects input for whether user chooses standard twin, double or deluxe twin, double.
    """
    while True:
        try:
            print("Please indicate which room type you desire by typing in 1, 2, 3 or 4.\n")
            print("1. Deluxe Double. 2. Deluxe Twin. 3. Standard Double. 4. Standard Twin.\n")
            room_choice = int(input("Write your room choice here: \n"))
        except ValueError:
            print("Please use only numbers.\n")
            continue
        else:
            break

    if room_choice == 1:
        print("You have picked the Deluxe Double bed option.\n")
        print(f"The price per night is {PRICES['Deluxe Double']}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 2:
        print("You have picked the Deluxe Twin bed option.\n")
        print(f"The price per night is {PRICES['Deluxe Twin']}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 3:
        print("You have picked the Standard Double bed option.\n")
        print(f"The price per night is {PRICES['Standard Double']}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 4:
        print("You have picked the Standard Twin bed option.\n")
        print(f"The price per night is {PRICES['Standard Twin']}€.\n")
        print("Updating your reservation...\n")
    else:
        print("Invalid input. Please enter a valid choice.\n")
        room_type()
    
    return room_choice


def customer_check_in_date():
    """
    Collects input from user for their check-in date
    """
    print("Please use format dd/mm/yyyy for dates\n")
    input_date_check_in = input("Indicate your check-in date here: \n")

    valid_check_in = True
    try:
        # day, month, year = input_date_check_in.split('/')
        # datetime.datetime(int(year), int(month), int(day))
        check_in_date = datetime.datetime.strptime(input_date_check_in, "%d/%m/%Y").date()
    except ValueError:
        valid_check_in = False
        print("Invalid check-in date. Please try again.\n")
        check_in_date()

    if(valid_check_in): 
        print(f"You have entered {check_in_date}.\n")
        print("Updating your reservation...\n")
    else:
        print("Invalid check-in date. Please try again.\n")
        check_in_date()
    
    return check_in_date


def customer_check_out_date():
    """
    Collects input from user for their check-out date
    """
    print("Please use format dd/mm/yyyy for dates\n")
    input_date_check_out = input("Indicate your check-out date here: \n")

    valid_check_out = True
    try:
        # day, month, year = input_date_check_out.split('/')
        # datetime.datetime(int(year), int(month), int(day))
        check_out_date = datetime.datetime.strptime(input_date_check_out, "%d/%m/%Y").date()
    except ValueError:
        valid_check_out = False
        print("Invalid check-out date. Please try again.")
        check_out_date()

    if(valid_check_out): 
        print(f"You have entered {check_out_date}.\n")
        print("Updating your reservation...\n")
    else:
        print("Invalid input date. Please try again.\n")
        check_out_date()

    return check_out_date


def calculate_total_price(room_choice, check_out_date, check_in_date):
    """
    Calculates the total price of the stay based on
    user input in the check-in and -out field.
    """
    num_choice = 0
    total_price = 0

    if room_choice == 1:
        num_days = (check_out_date - check_in_date).days
        total_price = num_days * PRICES['Deluxe Double']
        print(f"The total price for your stay is {total_price}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 2:
        num_days = (check_out_date - check_in_date).days
        total_price = num_days * PRICES['Deluxe Twin']
        print(f"The total price for your stay is {total_price}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 3:
        num_days = (check_out_date - check_in_date).days
        total_price = num_days * PRICES['Standard Double']
        print(f"The total price for your stay is {total_price}€.\n")
        print("Updating your reservation...\n")
    elif room_choice == 4:
        num_days = (check_out_date - check_in_date).days
        total_price = num_days * PRICES['Standard Twin']
        print(f"The total price for your stay is {total_price}€.\n")
        print("Updating your reservation...\n")

    return num_days, total_price

def confirm_reservation(
    cust_name,
    cust_age,
    no_of_guest,
    cust_email,
    type_of_room,
    date_check_in,
    date_check_out,
    num_days, total_price):
    """
    Accumulates customer information items, presents it as a list, prints 
    a confirmation of the reservation for the client to see and appends it
    onto a google sheets row for reference.
    """
    reservation_items = [cust_name, cust_age, no_of_guest, cust_email, type_of_room, date_check_in.strftime("%d/%m/%Y"), date_check_out.strftime("%d/%m/%Y"), total_price]
    print(f"""
    The following is confirmation of your reservation details:
    Name: {cust_name}
    Age: {cust_age}
    
    """)
    worksheet_to_update = reservations
    worksheet_to_update.append_row(reservation_items)

def main():
    """
    Runs all the previous functions for the program
    """
    cust_name = full_name()
    cust_age = customer_age()
    no_of_guest = guest_quantity()
    cust_email = customer_email_address()
    type_of_room = room_type()
    date_check_in = customer_check_in_date()
    date_check_out = customer_check_out_date()
    num_days, total_price = calculate_total_price(type_of_room, date_check_out, date_check_in)

    confirm_reservation(
    cust_name,
    cust_age,
    no_of_guest,
    cust_email,
    type_of_room,
    date_check_in,
    date_check_out,num_days, total_price)

if __name__ == "__main__":
    welcome_page()


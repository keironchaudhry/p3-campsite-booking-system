import re
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel_reservations')


reservations = GSPREAD_CLIENT.open('hotel_reservations').worksheet('reservations')


def full_name():
    """
    Takes the full name and details of the client and updates spreadsheet
    """
    while True: 

        print("Please enter your full name\n")
        print("For example: Tarik Khan \n")

        customer_name = input("Enter your full name here: \n")
        print(f"You have entered '{customer_name}'\n")

        validate_full_name(customer_name)

    return customer_name


def validate_full_name(customer_name):
    """
    Validates the input entered as the customers full name
    making sure that there are no numbers or symbols used.
    """

    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

    res = regex_name.search(customer_name)

    if res:
        print("Valid input. Updating datasheet...\n")
    else: 
        print("Invalid. Please enter a valid name.\n")


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
    else: 
        print(f"You are {age} years old.\n")
        print("Updating worksheet...\n")
        return age


def guest_quantity():
    """
    Takes in input for the number of guests
    """
    while True:
        try:
            print("Please indicate the numbers of guests staying.\n")
            print("Enter the amount as a digit, for example: 2\n")
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
        return guest_number

guest_quantity()

   
    






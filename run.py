import re
import gspread
import datetime
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

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel_reservations')


reservations = GSPREAD_CLIENT.open('hotel_reservations').worksheet('reservations')


def full_name():
    """
    Takes the full name and details of the client
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
        customer_email_address()
        
    return guest_number

def customer_email_address():
    """
    For taking in the details of a clients email address
    """

    print("Please provide us with an e-mail address for contact purposes.\n")
    print("E-mail address must be written as such: email@domain.com\n")
    email = input("Your e-mail address: \n")

    validate_email_address(email)


def validate_email_address(email):
    """
    Checks whether user email input is valid or invalid.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    
    if (re.fullmatch(regex, email)):
        print("E-mail address is valid.\n")
        print(f"Your e-mail address is {email}.\n")
    
    else:
        print("Invalid e-mail, please try again.\n")
        customer_email_address()

    return email

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
        print("Updating worksheet...\n")
    elif room_choice == 2:
        print("You have picked the Deluxe Twin bed option.\n")
        print(f"The price per night is {PRICES['Deluxe Twin']}€.\n")
        print("Updating worksheet...\n")
    elif room_choice == 3:
        print("You have picked the Standard Double bed option.\n")
        print(f"The price per night is {PRICES['Standard Double']}€.\n")
        print("Updating worksheet...\n")
    elif room_choice == 4:
        print("You have picked the Standard Twin bed option.\n")
        print(f"The price per night is {PRICES['Standard Twin']}€.\n")
        print("Updating worksheet...\n")
    else:
        print("Invalid input. Please enter a valid choice.\n")
        room_type()
    
    return room_choice


def check_in_date():
    """
    Collects input from user for their check-in date
    """
    print("Please use format dd/mm/yyyy for dates\n")
    input_date_check_in = input("Indicate your check-in date here: \n")

    valid_check_in = True
    try:
        day, month, year = input_date_check_in.split('/')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        valid_check_in = False
        print("Invalid check-in date. Please try again.")
        check_in_date()

    if(valid_check_in): 
        print("Valid check-in date.\n")
        print("Updating worksheet...\n")
    else:
        print("Invalid check-in date. Please try again.\n")
        check_in_date()
    
    return input_date_check_in


def check_out_date():
    """
    Collects input from user for their check-out date
    """
    print("Please use format dd/mm/yyyy for dates\n")
    input_date_check_out = input("Indicate your check-out date here: \n")

    valid_check_out = True
    try:
        day, month, year = input_date_check_out.split('/')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        valid_check_out = False
        print("Invalid check-out date. Please try again.")
        check_out_date()

    if(valid_check_out): 
        print("Valid check-out date.\n")
        print("Updating worksheet...\n")
    else:
        print("Invalid input date. Please try again.\n")
        check_out_date()

    return input_date_check_out


def calculate_total_price(input_date_check_out, input_date_check_in):
    """
    Calculates the total price of the stay based on
    user input in the check-in and -out field.
    """
    if room_choice == 1:
        num_days = (input_date_check_out - input_date_check_in).days
        total_price = num_days * {PRICES['Deluxe Double']}
        print(f"The total price for your stay is {total_price}€.")
    elif room_choice == 2:
        num_days = (input_date_check_out - input_date_check_in).days
        total_price = num_days * {PRICES['Deluxe Twin']}
        print(f"The total price for your stay is {total_price}€.")
    elif room_choice == 3:
        num_days = (input_date_check_out - input_date_check_in).days
        total_price = num_days * {PRICES['Standard Double']}
        print(f"The total price for your stay is {total_price}€.")
    elif room_choice == 4:
        num_days = (input_date_check_out - input_date_check_in).days
        total_price = num_days * {PRICES['Standard Twin']}
        print(f"The total price for your stay is {total_price}€.")


def main():
    """
    Runs all the previous functions for the program
    """
    

main()


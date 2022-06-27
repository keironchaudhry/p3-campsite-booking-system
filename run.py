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

reservations = SHEET.worksheet('reservations')

def full_name():
    """
    Takes the full name and details of the client and updates spreadsheet
    """
    print("Please enter your full name")

    customer_name = input("Enter your full name here: \n")
    print(f"Thank you, {customer_name}\n")

full_name()
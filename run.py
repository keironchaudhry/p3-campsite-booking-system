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

print("updating worksheet...")
reservations.update_cell(4, 1, "Mutton")
print("successfully updated.")

print("updating with input...")
i = 1
while reservations.cell(i, 1).value != "":
    i = i + 1
reservations.update_cell(i, 1, "Hello")
print("done.")


# def name():
#     """
#     Short test function to get a simple name
#     """
#     print("Please enter your full name:\n")
#     print("Enter name as such: Yoda Murray.\n")

#     full_name = input("Enter your full name here:\n")
#     print(f"Thank you, {full_name}.")

#     return full_name

# def update_worksheet():    
#     """    
#     Function used to make changes to the worksheet with full name    
#     """    

#     print("Updating worksheet...")

#     i = 1

#     while reservations.cell(i, 1).value != "":
#         i = i + 1
    
#     reservations.update_cell(i, 1, "yoda")

#     print("Worksheet updated successfully.")


###############################################################


# def full_name():
#     """
#     Takes the full name and details of the client and updates spreadsheet
#     """
#     while True: 

#         print("Please enter your full name\n")
#         print("For example: Tarik Khan \n")

#         customer_name = input("Enter your full name here: \n")
#         print(f"You have entered '{customer_name}'\n")

#         validate_full_name(customer_name)

#     return customer_name


# def validate_full_name(name):
#     """
#     Validates the input entered as the customers full name
#     """

#     regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

#     res = regex_name.search(name)


#     if res:
#         print("Valid input. Updating datasheet...\n")
#         add_customer_name()
#     else: print("Invalid. Please enter a valid name.\n")


# def update_worksheet_full_name(reservation_worksheet, row, col, value):
#     """
#     Transfers the validated customer input to google sheets
#     """
#     reservation_worksheet.update_cell(row, col, value)


# def add_customer_name():
#     """
#     Adds the customer name input after validation to google sheets
#     """
#     print("Adding your full name to reservation...")

#     reservation_worksheet = SHEET.worksheet("reservations")

#     reservation_worksheet.add_cols(1)

#     new_column_numer = len(reservation_worksheet.row_values(1)) + 1
#     print("Updating worksheet...")
#     update_worksheet_full_name(reservation_worksheet, 1, new_column_numer, name)

# room_number = 1

# full_name()
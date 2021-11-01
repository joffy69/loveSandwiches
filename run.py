import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPEAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures from the user
    """
    while True:
        print('Please enter sales figures from the last market.')
        print('Data should be six number separated by commas.')
        print('example: 10,19,10,2,43,8\n')

        data_str = input("Enter data here: ")
    
        sale_data = data_str.split(',')
       

        if validate_data(sale_data):
            print('data is valid')
            break
    
    return sale_data

def validate_data(values):
    """
    inside the try, converts all str values into integers
    raises valueerror if str cannot be converted into int, 
    or if there arent exactly 6 values
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'exactly 6 values, you provided {len(values)}'
            )
        print(values)
    except ValueError as e:
        print(f'invalid data: {e}. please try again\n')
        return False

    return True 

data = get_sales_data()
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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


def update_sales_worksheet(data):
    """
    update sales worksheet, add new row
    """
    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales updated correctly\n')

def calc_surplus_data(sales_row):
    """
    compare sales with stock
    """
    print('calculating surplus....\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    print(stock_row)



def main():
    """
    run all program files
    """
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calc_surplus_data(sales_data)

print('welcome to love sandwiches data automation\n')

main()
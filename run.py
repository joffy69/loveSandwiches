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


def calc_surplus_data(sales_row):
    """
    compare sales with stock
    """
    print('calculating surplus....\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data =[]
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

"""
for reference re refactoring
def update_sales_worksheet(data):
    
    update sales worksheet, add new row
    
    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales updated correctly\n')

def update_surplus_worksheet(data):
    
    update surplus worksheet with calculated surplus
    
    print(f'updating surplus worksheet....\n')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print('sales updated correctly\n')
"""

def update_worksheet(data, worksheet):
    """
    receive data and worksheet for updating
    """
    print(f'updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} updated correctly\n')

def get_last_5_entries_sales():
    """ 
    collects last 5 entries
    """
    sales = SHEET.worksheet('sales')
    # column = sales.col_values(3)
    # print(column)

    columns=[]
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns 

def calc_stock_data(data):
    """
    calc the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data=[]

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average*1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    run all program files
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,'sales')
    new_surplus_data = calc_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calc_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print('welcome to love sandwiches data automation\n')

main()

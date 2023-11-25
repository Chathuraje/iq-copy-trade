import time
from iqoptionapi.stable_api import IQ_Option
import datetime
import pytz
import json
from dotenv import load_dotenv
import os
load_dotenv()

def write_order_data_to_file(order_data):
    with open('order_data.json', 'w') as file:
        json.dump(order_data, file)
        
def check_balance():
    IQ_Account.change_balance(balance_type)
    return f"{balance_type} Account balance: {IQ_Account.get_balance()}"

def convert_time(dt_object_utc):
    utc_timezone = pytz.utc
    sri_lanka_timezone = pytz.timezone('Asia/Colombo')
    dt_object_sri_lanka = dt_object_utc.replace(tzinfo=utc_timezone).astimezone(sri_lanka_timezone)
    readable_date_time = dt_object_sri_lanka.strftime('%Y-%m-%d %H:%M:%S')
    
    return readable_date_time

def extract_data():
    order_data = IQ_Account.get_option_open_by_other_pc()

    # Extract the desired values into new variables
    data = list(order_data.values())[0]['msg']  # Get the inner dictionary

    balance = check_balance()
    active = data['active']
    dir = data['dir']
    type_name = data['type_name']
    microserviceName = order_data[list(order_data.keys())[0]]['microserviceName']
    profit_amount = data['profit_amount']
    exp_time = data['exp_time']
    
    dt_object_utc = datetime.datetime.utcfromtimestamp(exp_time)
    readable_date_time = convert_time(dt_object_utc)
        
    id = list(IQ_Account.get_option_open_by_other_pc().keys())[0]
    IQ_Account.del_option_open_by_other_pc(id)   
    # print(data)
     
    return balance, active, dir, microserviceName, profit_amount, exp_time, readable_date_time, type_name


def get_binary_orders():
    if IQ_Account.get_option_open_by_other_pc()!={}:
               
        balance, active, dir, microserviceName, profit_amount, exp_time, readable_date_time, type_name = extract_data()     
        
        # Print the values of the new variables
        print("\nOrder Placed!\n") 
        print(balance)
        print("active:", active)
        print("dir:", dir)
        print("microserviceName:", microserviceName)
        print("profit_amount:", profit_amount)
        print("type_name:", type_name)
        print(f"exp_time: {exp_time} ({readable_date_time})")
        print("----------------------------------------------------------------")
        
        # Write the order data to a file
        order_data = {
            "balance": balance,
            "active": active,
            "direction": dir,
            "microservice_name": microserviceName,
            "profit_amount": profit_amount,
            "exp_time": exp_time,
            "readable_date_time": readable_date_time,
            "type_name": type_name
        }
        write_order_data_to_file(order_data)

balance_type="PRACTICE" # "PRACTICE"/"REAL"/"TOURNAMENT"

# Retrieve sensitive information from environment variables
email = os.getenv("USERNAME_BUY")
password = os.getenv("PASSWORD_BUY")

# Create an instance of IQ_Option using the retrieved credentials
IQ_Account = IQ_Option(email, password)
IQ_Account.connect()

print(check_balance())

while True:
    get_binary_orders()
    time.sleep(1)
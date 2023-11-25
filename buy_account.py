import json
from iqoptionapi.stable_api import IQ_Option
import logging
import time
from dotenv import load_dotenv
import os
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# Initialize last_known_order_data as None
last_known_order_data = None

def buy(order_data):
    
    # Extract values into variables
    balance = order_data["balance"]
    active = order_data["active"]
    direction = order_data["direction"]
    microservice_name = order_data["microservice_name"]
    profit_amount = order_data["profit_amount"]
    exp_time = order_data["exp_time"]
    readable_date_time = order_data["readable_date_time"]
    type_name = order_data["type_name"]
    
    
    Money=profit_amount
    ACTIVES=active
    ACTION=direction
    expirations_mode=1

    check,id=IQ_Account.buy(Money,ACTIVES,ACTION,expirations_mode)
    
    if check:
        print("!buy!")
    else:
        print("buy fail")

# Retrieve sensitive information from environment variables
email = os.getenv("USERNAME_COPY")
password = os.getenv("PASSWORD_COPY")

# Create an instance of IQ_Option using the retrieved credentials
IQ_Account = IQ_Option(email, password)
IQ_Account.connect()

def read_order_data_from_file():
    try:
        with open('order_data.json', 'r') as file:
            order_data = json.load(file)
            return order_data
    except FileNotFoundError:
        return None

while True:
    order_data = read_order_data_from_file()

    if order_data and order_data != last_known_order_data:
        print("New order data Placed")
        buy(order_data)
        
        last_known_order_data = order_data
    
    time.sleep(1)

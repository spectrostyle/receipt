import csv
import os
import re
from datetime import date


def main():
    print("Welcome to a receipt generator.")
    current_month = date.today().strftime('%B')
    current_year = date.today().strftime('%Y')
    csv_filename = f'{current_year}-{current_month}_monthly-spending.csv'
    print(f"{csv_filename} has been be created.")
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, 'a', newline='') as file:
        fieldnames = ["Date", "Item", "Price", "Type"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        purchase_date = date.today()
        item = item_input()
        price = price_input()
        purchase_type = purchase_input()
        writer.writerow({"Date": purchase_date, "Item": item, "Price": price, "Type": purchase_type})


def price_input():
    print("Enter how much the item costs ($xx.xx)")
    price_input = input("Price: ")
    if not re.search(r'\.\d{2}$', price_input):
        price_input += ".00"
    price_match = re.match(r'^\$(\d+\.\d{2})$', price_input)
    while not price_match:
        print("Invalid price format. Please use $xx.xx format.")
        price_input = input("Price: ")
        if not re.search(r'\.\d{2}$', price_input):
            price_input += ".00"
        price_match = re.match(r'^\$(\d+\.\d{2})$', price_input)
    price = price_match.group(1)
    return price


def item_input():
    print("Enter what you purchased")
    item = input("Item: ")
    while not re.match(r'^[A-Za-z\s]+$', item):
        print("Invalid format!")
        item = input("Item (letters and spaces only): ")
    return item


def purchase_input():
    print("Was it personal, food, bill, etc?")
    purchase_type = input("Type of purchase: ")
    while not re.match(r'^[A-Za-z\s]+$', purchase_type):
        print("Invalid format!")
        purchase_type = input("Type of purchase (letters and spaces only): ")
    return purchase_type


"""
this gets the date, an item, the price of item, what type of item, and makes/updates a csv
of the current month with stated inputs. if it is a new month, this will make a new csv.

things to consider:
may want to include uploading my paycheck.
if so, have files start weekly. if day = friday, make new csv
if including paycheck, keep it a variable to subtract purchases from it to have a total remaining paycheck.

to do:
implement payday 
"""

if __name__ == '__main__':
    main()

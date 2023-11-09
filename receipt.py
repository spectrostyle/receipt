from datetime import date, timedelta
from csv import DictWriter, DictReader
from re import search, match
from os import path


"""
to do:
user functionality ie "add item, view maybe, exit?"
error checking
handling as well
loop to ask if more inputs
ask if want pdf exported (next longest part)
maybe either switch header pay to be amount or add new secondary header to store some info?
maybe make the secondary header as main header?
???
"""


def main():
    # self-explanatory
    current_date = date.today()

    # gets start of pay period, friday, if already friday, return current date
    week_start = start_friday(current_date)

    # gets the ending friday of pay period, if already friday, find next friday
    # week_end = ending_friday(current_date)

    # assign csv to 'current_file' variable. checks if current file doesn't exist, creates new file if so
    current_file = f'{week_start}_spending.csv'
    if not path.isfile(current_file):
        create_file(current_file)

    # this should find the current 'pay' amount, if today is payday, asks for amount
    # else if not payday, loads previous amount from current csv
    # this one needs work?
    pay = pay_day(week_start, current_date, current_file)

    # get what was purchased
    item = item_input()

    # get cost of item
    price = float(price_input())

    # update remainder of money
    pay -= price

    # get category of purchase. prob make list of avail. cat.
    purchase_type = purchase_input()

    # updates current csv with new line of purchase details
    with open(current_file, 'a', newline='') as file:
        writer = DictWriter(file, fieldnames=["Date", "Item", "Price", "Type", "Pay"])
        writer.writerow({"Date": current_date, "Item": item, "Price": price, "Type": purchase_type, "Pay": pay})


def start_friday(current_date):
    week_start = current_date
    if week_start.weekday() == 4:    # if 'friday'
        return week_start
    while week_start.weekday() != 4:
        week_start -= timedelta(days=1)
    return week_start


def ending_friday(current_date):
    week_end = current_date
    if week_end.weekday() == 4:
        week_end += timedelta(days=1)
    while week_end.weekday() != 4:    # while not 'friday'
        week_end += timedelta(days=1)
    return week_end


def pay_day(week_start, current_date, current_file):
    if week_start == current_date:
        # add regex
        payday = float(input("Pay amount: "))

        week_start -= timedelta(days=1)
        while week_start.weekday() != 4:
            week_start -= timedelta(days=1)
        last_week = week_start
        with open(f'{last_week}_spending.csv', 'r') as file:
            reader = DictReader(file)
            for row in reader:
                last_row = row
            if last_row:
                # noinspection PyTypeChecker
                pay = float(last_row["Pay"])
        pay += payday
    else:
        with open(f'{current_file}', 'r') as file:
            reader = DictReader(file)
            for row in reader:
                last_row = row
            try:
                if last_row:
                    # noinspection PyTypeChecker
                    pay = float(last_row["Pay"])
            except UnboundLocalError:
                pay = float(input("Pay amount: "))

    return pay


def create_file(current_file):
    with open(current_file, 'a', newline='') as file:
        fieldnames = ["Date", "Item", "Price", "Type", "Pay"]
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    print(f"{current_file} has been be created.")


def price_input():
    price = input(f"Enter how much the item costs ($xx.xx)\nPrice: ")
    # allow to not type $
    if not search(r'\.\d{2}$', price):
        price += ".00"
    price_match = match(r'^\$(\d+\.\d{2})$', price)
    while not price_match:
        price = input(f"Invalid price format. Please use $xx.xx format.\nPrice: ")
        if not search(r'\.\d{2}$', price):
            price += ".00"
        price_match = match(r'^\$(\d+\.\d{2})$', price)
    price = price_match.group(1)
    return price


def item_input():
    item = input(f"Enter what you purchased\nItem: ")
    while not match(r'^[A-Za-z\s]+$', item):
        item = input(f"Invalid format! \nItem (letters and spaces only): ")
    return item


def purchase_input():
    print("Was it personal, food, bill, etc?")
    purchase_type = input("Type of purchase: ")
    while not match(r'^[A-Za-z\s]+$', purchase_type):
        print("Invalid format!")
        purchase_type = input("Type of purchase (letters and spaces only): ")
    return purchase_type


if __name__ == '__main__':
    main()

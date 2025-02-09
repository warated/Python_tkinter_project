import datetime
from tkinter import *
from random import choice
import time
import json


collection = {
    "Computer": [],
    "Camera": [],
    "Phone": [],
    "Video Player":[]
}

def display_menu(): # Function to display our menu with (Add/Show/Delete/Exit)
    print("--------Python Retro Collection---------")
    print("1. Add Item to Collection.")
    print("2. Show Items in Collection.")
    print("3. Delete Items from Collection.")
    print("4. Edit Item.")
    print("5. Exit.")
    choice = input("Choice> ")
    return choice

def add_item(): # Function to add Items
    print("Add an item title....")
    title = input("Title> ")
    print("Types: 1. Computer, 2. Camera, 3. Phone, 4. Video Player")
    type_choice = int(input("Type> "))
    item_type = list(collection.keys())[type_choice - 1]
    while True: # While loop validation for user inputting the correct date formating.
        date_added_str = input("Date Added (dd/mm/yyyy): ")
        try:
            date_added = datetime.datetime.strptime(date_added_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Invalid date format. Please enter in the format DD/MM/YYYY.")
    while True:
        date_manufacture_str = input("Date of Manufacture: (dd/mm/yyyy)")
        try:
            date_manufacture = datetime.datetime.strptime(date_manufacture_str, "%d/%m/%Y").date()
            if date_manufacture > datetime.date.today():
                print("Date of Manufacture cannot be in the future!")
            else:
                break
        except ValueError:
            print("Invalid date format. Please enter in the format DD/MM/YYYY.")
    description = input("Description:> ")


    print("Adding item...", end="") # Animation with ...
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\n")

    item = {
        "Title": title,
        "Date Added": date_added,
        "Date of manufacture": date_manufacture,
        "Description": description
    }
    collection[item_type].append(item)
    print("Item Added Successfully!")




def edit_item():
    print("Editing an item....")
    print("Types: 1. Computer, 2. Camera, 3. Phone, 4. Video Player")
    type_choice = int(input("Type> "))
    item_type = list(collection.keys())[type_choice - 1]

    if not collection[item_type]:
        print(f"No items to edit in {item_type}.")
        return

    # List items for the user to select
    print(f"Editing from: {item_type}")
    for idx, item in enumerate(collection[item_type], 1):
        print(f"{idx}. {item['Title']}")

    edit_idx = int(input("Select item number to edit> "))
    if 0 < edit_idx <= len(collection[item_type]):
        item = collection[item_type][edit_idx - 1]
    else:
        print("Invalid selection.")
        return

    print("Item found. Enter new values or press Enter to keep current values.")

    # Edit fields
    new_title = input(f"Title ({item['Title']}): ") or item["Title"]
    while True:
        date_added_str = input(f"Date Added (DD/MM/YYYY) [{item['Date Added']}]: ")
        if not date_added_str:
            new_date_added = item["Date Added"]
            break
        try:
            new_date_added = datetime.datetime.strptime(date_added_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Invalid date format. Please enter in the format DD/MM/YYYY.")

    while True:
        date_manufacture_str = input(f"Date of Manufacture (DD/MM/YYYY) [{item['Date of manufacture']}]: ")
        if not date_manufacture_str:
            new_date_manufacture = item["Date of manufacture"]
            break
        try:
            new_date_manufacture = datetime.datetime.strptime(date_manufacture_str, "%d/%m/%Y").date()
            if new_date_manufacture > datetime.date.today():
                print("Date of Manufacture cannot be in the future!")
            else:
                break
        except ValueError:
            print("Invalid date format. Please enter in the format DD/MM/YYYY.")

    new_description = input(f"Description ({item['Description']}): ") or item["Description"]

    # Update the item
    item.update({
        "Title": new_title,
        "Date Added": new_date_added,
        "Date of manufacture": new_date_manufacture,
        "Description": new_description
    })
    print("Item updated successfully!")




def show_items(): # Function to show items
    print("Types: 1. Computer, 2. Camera, 3. Phone, 4. Video Player")
    type_choice = int(input("Type> "))
    item_type = list(collection.keys())[type_choice - 1]
    print(f"Showing: {item_type}")
    for item in collection[item_type]:
        print("Title: ", item["Title"])
        print("Date Added: ", item["Date Added"])
        print("Date of Manufacture: ", item["Date of manufacture"])
        print("Description: ", item["Description"])





def delete_item(): # Function to delete items
    print("Types: 1. Computer, 2. Camera, 3. Phone, 4. Video Player")
    type_choice = int(input("Type> "))
    item_type = list(collection.keys())[type_choice - 1]

    if not collection[item_type]:
        print(f"No items to delete in {item_type}.")
        return

    print(f"Deleting from: {item_type}")
    for idx, item in enumerate(collection[item_type], 1):
        print(f"{idx}. {item['Title']}")

    delete_idx = int(input("Select item number to delete> "))
    if 0 < delete_idx <= len(collection[item_type]):
        removed_item = collection[item_type].pop(delete_idx - 1)
        print(f"Deleting Item:1 {removed_item['Title']}!")
    else:
        print("Invalid selection.")


    print("Deleting item...", end="") # Animation with ...
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\nDeleted Successfully!")


# Main loop
def main():
    while True:
        choice = display_menu()
        if choice == "1":
            add_item()
        elif choice == "2":
            show_items()
        elif choice == "3":
            delete_item()
        elif choice == "4":
             edit_item()
        elif choice == "5":
            print("Exiting program..", end="")
            for _ in range(5):
                print(".", end="", flush=True)
                time.sleep(0.5)
            break
        else:
            print("Invalid entry. Please try again.")


if __name__ == "__main__":
    main()
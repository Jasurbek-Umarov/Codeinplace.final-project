import os
import json
import getpass
import hashlib

DATA_FILE = 'budget_tracker_data.json'

# Utility functions for handling data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"users": [], "budgets": {}, "expenses": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Utility functions for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    data = load_data()
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    confirm_password = getpass.getpass("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    for user in data['users']:
        if user['email'] == email:
            print("Email already registered.")
            return

    hashed_password = hash_password(password)
    user = {"name": name, "email": email, "password": hashed_password}
    data['users'].append(user)
    save_data(data)
    print("Registration successful!")

def login():
    data = load_data()
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    hashed_password = hash_password(password)
    for user in data['users']:
        if user['email'] == email and user['password'] == hashed_password:
            print(f"Welcome, {user['name']}!")
            return user
    print("Invalid email or password.")
    return None

def set_budget(user):
    data = load_data()
    budget_amount = float(input("Enter your budget amount: "))
    data['budgets'][user['email']] = budget_amount
    save_data(data)
    print("Budget set successfully!")

def add_expense(user):
    data = load_data()
    amount = float(input("Enter the amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category: ")
    description = input("Enter the description: ")

    expense = {
        "amount": amount,
        "date": date,
        "category": category,
        "description": description
    }
    if user['email'] not in data['expenses']:
        data['expenses'][user['email']] = []
    data['expenses'][user['email']].append(expense)
    save_data(data)
    print("Expense added successfully!")

def display_budget(user):
    data = load_data()
    budget = data['budgets'].get(user['email'])
    if budget:
        expenses = data['expenses'].get(user['email'], [])
        total_expenses = sum(exp["amount"] for exp in expenses)
        remaining_budget = budget - total_expenses
        print(f"Current budget: {budget}")
        print(f"Remaining budget: {remaining_budget}")
        print(f"Expenses used: {total_expenses}")
    else:
        print("No budget set. Please set your budget first.")

def display_expenses(user):
    data = load_data()
    expenses = data['expenses'].get(user['email'], [])
    if expenses:
        print("Date\t\tAmount\tCategory\tDescription")
        print("----------------------------------------------------")
        for expense in expenses:
            print(f"{expense['date']}\t{expense['amount']}\t{expense['category']}\t{expense['description']}")
    else:
        print("No expenses found.")

def main():
    while True:
        print("1. Register")
        print("2. Login")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                break
        else:
            print("Invalid choice. Please choose again.")

    while True:
        print("\n1. Set Budget")
        print("2. Add Expense")
        print("3. Display Budget")
        print("4. Display Expenses")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            set_budget(user)
        elif choice == "2":
            add_expense(user)
        elif choice == "3":
            display_budget(user)
        elif choice == "4":
            display_expenses(user)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()

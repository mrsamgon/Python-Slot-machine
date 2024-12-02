import random
import time
import json
import os

BALANCE_FILE = "balance.json"

def load_balance():
    """Load balance from file or return default balance if file doesn't exist or is invalid."""
    if os.path.exists(BALANCE_FILE):
        try:
            with open(BALANCE_FILE, "r") as file:
                data = json.load(file)
                if "balance" in data and isinstance(data["balance"], (int, float)):
                    return data["balance"]
                else:
                    print("Invalid data in balance file. Starting with default balance.")
                    return 100  # Default balance if file is corrupted
        except (json.JSONDecodeError, ValueError):
            print("Error reading balance file. Starting with default balance.")
            return 100  # Default balance if file can't be read properly
    return 100  # Default balance if no file exists

def save_balance(balance):
    """Save balance to a file."""
    try:
        with open(BALANCE_FILE, "w") as file:
            json.dump({"balance": balance}, file)
    except Exception as e:
        print(f"Error saving balance: {e}")

def top_up(balance):
    """Allow the player to top up their balance."""
    while True:
        try:
            amount = float(input("Enter the amount to top up: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            balance += amount
            print(f"Your new balance is: ${balance}")
            save_balance(balance)  # Save the new balance to the file
            return balance
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def spin_row():
    symbols = ['🍒', '🍉', '🍋', '🔔', '⭐']
    return [random.choice(symbols) for _ in range(3)]

def print_row(row):
    print("*****************************")
    print(" | ".join(row))
    print("*****************************")

def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '🍒':
            return bet * 3
        elif row[0] == '🍉':
            return bet * 4
        elif row[0] == '🍋':
            return bet * 6
        elif row[0] == '🔔':
            return bet * 10
        elif row[0] == '⭐':
            print("Congratulations, you hit the jackpot!")
            return bet * 30
    return 0

def main():
    balance = load_balance()
    print("*****************************")
    print("Welcome to Python Slots")
    print("Symbols: 🍒 🍉 🍋 🔔 ⭐ ")
    print("*****************************")

    while True:
        if balance <= 0:
            print("Your balance is $0!")
            choice = input("Would you like to top up your balance? (Y/N): ").lower()
            if choice == 'y':
                balance = top_up(balance)
            else:
                break

        print(f"Current balance: ${balance}")
        print("1. Spin the slot machine")
        print("2. Top up balance")
        print("3. Quit")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            bet = input("Enter your bet amount: ")

            if not bet.isdigit() or int(bet) <= 0:
                print("Please enter a valid positive number")
                continue

            bet = int(bet)

            if bet > balance:
                print("Insufficient balance")
                continue

            balance -= bet
            row = spin_row()
            print("Spinning....\n")
            time.sleep(0.5)
            print_row(row)

            payout = get_payout(row, bet)

            if payout > 0:
                print(f"You won ${payout}!")
            else:
                print("Sorry, you lost! Please try again.")

            balance += payout
            save_balance(balance)  # Save the updated balance

        elif choice == "2":
            balance = top_up(balance)  # Top up balance

        elif choice == "3":
            break

        else:
            print("Invalid choice! Please select a valid option.")

    print("*****************************")
    print(f"Game over! Your final balance is ${balance}")
    print("*****************************")
    save_balance(balance)  # Save the final balance when exiting


if __name__ == "__main__":
    main()

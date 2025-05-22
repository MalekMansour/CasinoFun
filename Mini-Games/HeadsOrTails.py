import random

CHOICES = ['heads', 'tails']
STARTING_BALANCE = 100
MIN_BET = 1

def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Enter your bet amount (${MIN_BET}-{balance}): $"))
            if MIN_BET <= bet <= balance:
                return bet
            else:
                print(f"Invalid bet. Enter a value between {MIN_BET} and {balance}.")
        except ValueError:
            print("Please enter a valid number.")

def get_user_choice():
    while True:
        user_choice = input("Choose heads or tails: ").strip().lower()
        if user_choice in CHOICES:
            return user_choice
        print("Invalid choice. Please choose 'heads' or 'tails'.")

def play_round(balance):
    print(f"\nYour current balance: ${balance}")
    bet = get_bet(balance)
    user_choice = get_user_choice()
    result = random.choice(CHOICES)
    print(f"The coin landed on: {result}")

    if user_choice == result:
        print("You win!")
        balance += bet
    else:
        print("You lose!")
        balance -= bet
    return balance

def heads_or_tails():
    print("Welcome to Heads or Tails!")
    balance = STARTING_BALANCE

    while True:
        balance = play_round(balance)
        if balance <= 0:
            print("You have run out of money. Resetting balance to starting amount.")
            balance = STARTING_BALANCE

if __name__ == "__main__":
    heads_or_tails()

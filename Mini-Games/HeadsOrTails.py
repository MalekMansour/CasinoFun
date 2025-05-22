import random

CHOICES = ['heads', 'tails']
STARTING_BALANCE = 100
MIN_BET = 1
STARTING_WIN_CHANCE = 0.5  # 50%
WIN_CHANCE_STEP = 0.02     # 2%

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

def play_round(balance, win_chance):
    print(f"\nYour current balance: ${balance}")
    print(f"Current win chance: {int(win_chance * 100)}%")
    bet = get_bet(balance)
    user_choice = get_user_choice()

    if random.random() < win_chance:
        result = user_choice
    else:
        result = CHOICES[1] if user_choice == CHOICES[0] else CHOICES[0]

    print(f"The coin landed on: {result}")

    if user_choice == result:
        print("You win!")
        balance += bet
        win_chance = max(0.0, win_chance - WIN_CHANCE_STEP)
    else:
        print("You lose!")
        balance -= bet
        win_chance = min(1.0, win_chance + WIN_CHANCE_STEP)
    return balance, win_chance

def heads_or_tails():
    print("Welcome to Heads or Tails!")
    balance = STARTING_BALANCE
    win_chance = STARTING_WIN_CHANCE

    while True:
        balance, win_chance = play_round(balance, win_chance)
        if balance <= 0:
            print("You have run out of money. Resetting balance to starting amount.")
            balance = STARTING_BALANCE
            win_chance = STARTING_WIN_CHANCE

if __name__ == "__main__":
    heads_or_tails()

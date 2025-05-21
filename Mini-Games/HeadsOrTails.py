import random

def heads_or_tails():
    print("Welcome to Heads or Tails!")
    CHOICES = ['heads', 'tails']
    STARTING_BALANCE = 100
    MIN_BET = 1

    balance = STARTING_BALANCE

    while True:
        print(f"\nYour current balance: ${balance}")

        # Get bet amount
        while True:
            try:
                bet = int(input(f"Enter your bet amount (${MIN_BET}-{balance}): $"))
                if MIN_BET <= bet <= balance:
                    break
                else:
                    print(f"Invalid bet. Enter a value between {MIN_BET} and {balance}.")
            except ValueError:
                print("Please enter a valid number.")

        # Get user choice
        while True:
            user_choice = input("Choose heads or tails: ").strip().lower()
            if user_choice in CHOICES:
                break
            print("Invalid choice. Please choose 'heads' or 'tails'.")

        result = random.choice(CHOICES)
        print(f"The coin landed on: {result}")

        if user_choice == result:
            print("You win!")
            balance += bet
        else:
            print("You lose!")
            balance -= bet

        if balance <= 0:
            print("You have run out of money. Resetting balance to starting amount.")
            balance = STARTING_BALANCE

if __name__ == "__main__":
    heads_or_tails()

import random

def heads_or_tails():
    print("Welcome to Heads or Tails!")
    choices = ['heads', 'tails']
    balance = 100  # Starting currency

    while True:
        print(f"\nYour current balance: ${balance}")
        # Get bet amount
        while True:
            try:
                bet = int(input("Enter your bet amount: $"))
                if 1 <= bet <= balance:
                    break
                else:
                    print(f"Invalid bet. Enter a value between 1 and {balance}.")
            except ValueError:
                print("Please enter a valid number.")

        # Get user choice
        while True:
            user_choice = input("Choose heads or tails: ").strip().lower()
            if user_choice in choices:
                break
            print("Invalid choice. Please choose 'heads' or 'tails'.")

        result = random.choice(choices)
        print(f"The coin landed on: {result}")

        if user_choice == result:
            print("You win!")
            balance += bet
        else:
            print("You lose!")
            balance -= bet

        if balance <= 0:
            print("You have run out of money. Game over!")
            break

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print(f"You leave with ${balance}.")
            break

if __name__ == "__main__":
    heads_or_tails()
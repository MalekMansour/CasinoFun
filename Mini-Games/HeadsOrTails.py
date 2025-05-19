import random

def heads_or_tails():
    print("Welcome to Heads or Tails!")
    choices = ['heads', 'tails']
    while True:
        user_choice = input("Choose heads or tails: ").strip().lower()
        if user_choice in choices:
            break
        print("Invalid choice. Please choose 'heads' or 'tails'.")

    result = random.choice(choices)
    print(f"The coin landed on: {result}")

    if user_choice == result:
        print("You win!")
    else:
        print("You lose!")

if __name__ == "__main__":
    heads_or_tails()
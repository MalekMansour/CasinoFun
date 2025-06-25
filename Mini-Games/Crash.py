import random
import time

def crash_game():
    print("Welcome to Crash!")
    balance = 100.0
    high_score = balance

    while True:
        print(f"\nYour balance: ${balance:.2f} | High Score: ${high_score:.2f}")
        try:
            bet = float(input("Enter your bet (0 to quit): "))
        except ValueError:
            print("Invalid input.")
            continue
        if bet == 0:
            print("Thanks for playing!")
            break
        if bet < 0 or bet > balance:
            print("Invalid bet amount.")
            continue

        multiplier = 1.0
        crashed = False
        crash_point = round(random.uniform(1.1, 10.0), 2)
        print(f"Game started! (Crash point is hidden)")

        while True:
            time.sleep(0.5)
            multiplier = round(multiplier + random.uniform(0.05, 0.25), 2)
            print(f"Multiplier: x{multiplier}", end='\r')
            action = input("Press 'c' to cash out, Enter to continue: ").strip().lower()
            if action == 'c':
                winnings = round(bet * multiplier, 2)
                balance += winnings - bet
                print(f"\nYou cashed out at x{multiplier}! You won ${winnings:.2f}")
                if balance > high_score:
                    high_score = balance
                    print("🎉 New High Score! 🎉")
                break
            if multiplier >= crash_point:
                print(f"\nCrashed at x{crash_point}! You lost your bet.")
                balance -= bet
                crashed = True
                break

        if balance <= 0:
            print("You are out of money! Game over.")
            break

        # Offer to play again or quit
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    crash_game()
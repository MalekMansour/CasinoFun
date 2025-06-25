import random

def get_bet(money):
    while True:
        try:
            bet = float(input(f"Enter your bet amount (Available: ${money:.2f}): $"))
            if bet <= 0:
                print("Bet must be a positive number.")
            elif bet > money:
                print("You don't have enough money to make that bet.")
            else:
                return bet
        except ValueError:
            print("Please enter a valid number.")

def print_status(round_number, cycle, money, quota):
    print(f"\n--- Round {round_number} ---")
    print(f"Cycle {cycle} | Money: ${money:.2f} | Quota: ${quota:.2f}")

def main():
    money = 100.0
    quota = 100.0
    round_number = 1
    cycle = 1

    multipliers = [0.2, 0.5, 1, 2, 5, 10, 100]
    weights = [205, 205, 205, 205, 100, 30, 50]

    print("Welcome to the Survival Gambling Game!")
    print("Every 7 rounds, you must meet the money quota or you lose.")
    print("Starting money: $100.00\n")

    while True:
        print_status(round_number, cycle, money, quota)
        bet = get_bet(money)

        multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        win_amount = bet * multiplier
        money = money - bet + win_amount

        print(f"Multiplier: x{multiplier}")
        print(f"You {'won' if multiplier > 1 else 'lost' if multiplier < 1 else 'broke even'} ${win_amount - bet:.2f}.")
        print(f"After round {round_number}, you have: ${money:.2f}")

        if money <= 0:
            print("You went bankrupt! Game over.")
            break

        if round_number % 7 == 0:
            print(f"\n--- End of cycle {cycle} ---")
            print(f"You need at least ${quota:.2f} to survive.")
            if money >= quota:
                print("Congratulations! You met the quota and advance to the next cycle.")
                cycle += 1
                quota = round(quota * 1.5, 2)
                print(f"New quota: ${quota:.2f}\n")
            else:
                print("You failed to meet the quota. Game over.")
                break

        round_number += 1

if __name__ == "__main__":
    main()

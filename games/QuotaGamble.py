import random

def main():
    money = 100.0
    quota = 100.0
    round_number = 1
    cycle = 1

    multipliers = [0.2, 0.5, 1, 2, 5, 10, 100]
    # Jackpot (x100) has a 0.0003% chance; the other six share the remaining probability equally
    weights = [16.666616667] * 6 + [0.0003]

    print("Welcome to the Survival Gambling Game!")
    print("Every 7 rounds, you must meet the money quota or you lose.")
    print("Starting money: $100.00\n")

    while True:
        print(f"--- Round {round_number} ---")
        print(f"Cycle {cycle}, Money: ${money:.2f}, Quota: ${quota:.2f}")

        # Prompt user for their bet
        while True:
            try:
                bet = float(input("Enter your bet amount: $"))
                if bet <= 0:
                    print("Bet must be a positive number.")
                elif bet > money:
                    print("You don't have enough money to make that bet.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")

        # Perform the gamble
        multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        win_amount = bet * multiplier
        money = money - bet + win_amount

        print(f"Multiplier: x{multiplier}")
        print(f"After round {round_number}, you have: ${money:.2f}\n")

        # Check for bankruptcy
        if money <= 0:
            print("You went bankrupt! Game over.")
            break

        # After every 7 rounds, check the quota
        if round_number % 7 == 0:
            print(f"End of cycle {cycle}. You need at least ${quota:.2f} to survive.")
            if money >= quota:
                print("Congratulations! You met the quota and advance to the next cycle.\n")
                cycle += 1
                # Increase quota for next cycle (adjust factor as desired)
                quota *= 1.5
                print(f"New quota: ${quota:.2f}\n")
            else:
                print("You failed to meet the quota. Game over.")
                break

        round_number += 1

if __name__ == "__main__":
    main()

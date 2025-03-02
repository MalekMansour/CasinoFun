import random

def create_deck():
    deck = []
    for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
        for rank in range(2, 11):
            deck.append(f'{rank} of {suit}')
        for face in ['Jack', 'Queen', 'King', 'Ace']:
            deck.append(f'{face} of {suit}')
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card.split(' ')[0]
        if rank in ['Jack', 'Queen', 'King']:
            value += 10
        elif rank == 'Ace':
            aces += 1
            value += 11
        else:
            value += int(rank)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(hand, name):
    print(f"{name}'s hand: {', '.join(hand)}")

def blackjack():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    while True:
        display_hand(player_hand, 'Player')
        player_value = calculate_hand_value(player_hand)
        print(f"Player's hand value: {player_value}")

        if player_value > 21:
            print("Player busts! Dealer wins.")
            return

        action = input("Do you want to [h]it or [s]tand? ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    display_hand(dealer_hand, 'Dealer')
    dealer_value = calculate_hand_value(dealer_hand)
    print(f"Dealer's hand value: {dealer_value}")

    if dealer_value > 21 or player_value > dealer_value:
        print("Player wins!")
    elif player_value < dealer_value:
        print("Dealer wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    blackjack()
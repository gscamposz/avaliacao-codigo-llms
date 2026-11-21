def calculate_hand_value(self, hand):
    """
    Calculate the total value of a hand, considering Ace as 1 or 11.
    """
    total = 0
    aces = 0

    for card in hand:
        rank = card[:-1]  # Remove suit (e.g., 'A', 'J', '5', '10')

        if rank == 'J' or rank == 'Q' or rank == 'K':
            total += 10
        elif rank == 'A':
            total += 11
            aces += 1
        else:
            total += int(rank)

    # Adjust Aces to 1 if total exceeds 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def check_winner(self, player_hand, dealer_hand):
    """
    Determine the winner of a round based on hand values.
    Returns 'Player wins', 'Dealer wins', or 'Tie' if values are equal.
    """
    player_value = self.calculate_hand_value(player_hand)
    dealer_value = self.calculate_hand_value(dealer_hand)

    if player_value > dealer_value:
        return 'Player wins'
    elif player_value < dealer_value:
        return 'Dealer wins'
    else:
        return 'Tie'

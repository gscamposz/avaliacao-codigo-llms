
import random


class BlackjackGame:
    """
    This is a class representing a game of blackjack, which includes
    creating a deck, calculating the value of a hand, and determining
    the winner based on the hand values of the player and dealer.
    """

    def __init__(self):
        """
        Initialize the Blackjack Game with the attributes deck,
        player_hand and dealer_hand.
        """
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        """
        Create a deck of 52 cards in random order, without Jokers.
        :return: A list of 52 cards.
        """
        suits = ['S', 'H', 'D', 'C']
        ranks = ['A', '2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'J', 'Q', 'K']

        deck = [rank + suit for suit in suits for rank in ranks]
        random.shuffle(deck)

        return deck

    def calculate_hand_value(self, hand):
        """
        Calculate the value of the cards in a hand according
        to the rules of Blackjack.
        :param hand: list
        :return: The total value of the hand.
        """
        total = 0
        aces = 0

        for card in hand:
            rank = card[:-1]

            if rank == 'A':
                total += 11
                aces += 1
            elif rank in ['J', 'Q', 'K']:
                total += 10
            else:
                total += int(rank)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def check_winner(self, player_hand, dealer_hand):
        """
        Determine the winner by comparing the hand values.
        :param player_hand: list
        :param dealer_hand: list
        :return: 'Dealer wins' or 'Player wins'
        """
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        if player_value <= 21 and dealer_value <= 21:
            if player_value > dealer_value:
                return 'Player wins'
            else:
                return 'Dealer wins'

        if player_value < dealer_value:
            return 'Player wins'
        else:
            return 'Dealer wins'

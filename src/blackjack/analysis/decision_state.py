from ..hand import Hand
from ..card import Card
import copy

class DecisionState:
    def __init__(self, hand: Hand, dealer_upcard: Card, card_count):
        self.cards = hand.cards
        self.is_soft = hand.is_soft
        self.dealer_upcard = dealer_upcard
        self.card_count = card_count
        self.bet = hand.bet

    @property
    def total(self):
        hand = Hand()
        hand.cards = self.cards
        return hand.evaluate()

    @property
    def is_blackjack(self):
        hand = Hand()
        hand.cards = self.cards
        return hand.isBlackjack()

    @property
    def is_pair(self):
        hand = Hand()
        hand.cards = self.cards
        return hand.isPair()

    @property
    def legal_moves(self):
        hand = Hand()
        hand.cards = self.cards
        hand.bet = self.bet
        return hand.getLegalMoves()

    def withdrawCardFromDeck(self, card: Card):
        if card.value.value in "23456789":
            self.card_count[int(card.value.value)] -= 1
        elif card.value.value in "TJQK":
            self.card_count[10] -= 1
        else:
            self.card_count[11] -= 1

    def clone(self):
        return copy.deepcopy(self)
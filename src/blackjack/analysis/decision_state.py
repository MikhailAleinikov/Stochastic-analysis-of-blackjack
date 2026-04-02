from ..hand import Hand
from ..card import Card

class DecisionState:
    def __init__(self, hand: Hand, dealer_upcard: Card, card_count):
        self.total = hand.evaluate()
        self.cards = hand.cards
        self.is_soft = hand.is_soft
        self.is_blackjack = hand.isBlackjack()
        self.legal_moves = hand.getLegalMoves()
        self.dealer_upcard = dealer_upcard
        self.card_count = card_count
        self.bet = hand.bet
        self.is_pair = hand.isPair()
from ...rules import Moves
from ...hand import Hand
from ...card import Card
from .eval_hand_from_int import evalHandFromInt
import copy

class SimState:
    def __init__(self, hand: Hand, dealer_upcard: Card, card_count):
        self.cards = [i.toInt() for i in hand.cards]
        self.is_soft = hand.is_soft
        self.dealer_upcard = dealer_upcard.toInt()
        self.card_count = card_count
        self.bet = hand.bet
        self.is_split = hand.is_split


    @property
    def total(self):
        return evalHandFromInt(self.cards)

    @property
    def is_blackjack(self):
        return sorted(self.cards) == [10, 11]

    @property
    def is_pair(self):
        if len(self.cards) == 2:
            return self.cards[0] == self.cards[1]
        else: return False

    @property
    def legal_moves(self):
        output = []
        output.append(Moves.STAND)
        if self.total < 21:
            output.append(Moves.HIT)
            if len(self.cards) == 2:
                output.append(Moves.DOUBLE)
            if self.is_pair:
                output.append(Moves.SPLIT)
        return output

    def withdrawCardFromDeck(self, card: int):
        self.card_count[card] -= 1

    def clone(self):
        return copy.deepcopy(self)
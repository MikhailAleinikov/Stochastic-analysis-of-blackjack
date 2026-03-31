from enum import Enum
from .rules import Suit, CardValue

class Card:
    def __init__(self, suit: Suit, value: CardValue):
        if not isinstance(suit, Suit):
            raise ValueError("suit must be of type Suit")
        if not isinstance(value, CardValue):
            raise ValueError("value must be of type CardValue")

        self.suit = suit
        self.value = value

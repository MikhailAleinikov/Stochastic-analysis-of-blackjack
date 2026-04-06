from .rules import Suit, CardValue

class Card:
    def __init__(self, suit: Suit, value: CardValue):
        if not isinstance(suit, Suit):
            raise ValueError("suit must be of type Suit")
        if not isinstance(value, CardValue):
            raise ValueError("value must be of type CardValue")
        self.suit = suit
        self.value = value

    def toInt(self):
        if self.value.value in "23456789": return int(self.value.value)
        elif self.value.value in "TJQK": return 10
        else: return 11
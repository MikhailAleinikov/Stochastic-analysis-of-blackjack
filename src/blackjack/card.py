from enum import Enum

class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"

class CardValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    def __init__(self, suit: Suit, value: CardValue):
        if not isinstance(suit, Suit):
            raise ValueError("suit must be of type Suit")
        if not isinstance(value, CardValue):
            raise ValueError("value must be of type CardValue")

        self.suit = suit
        self.value = value

from enum import Enum

class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"

class CardValue(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class Moves(Enum):
    HIT = 'Hit'
    STAND = 'Stand'
    DOUBLE = "Double"
    SPLIT = "Split"

class GameState(Enum):
    PLAYERS = "Dealing"
    DEALER = "DealerCards"
    SETTLEMENTS = "Settlements"
    BETTING = "Betting"
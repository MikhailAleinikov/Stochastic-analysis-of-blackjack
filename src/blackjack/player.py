from .hand import Hand

class Player:
    def __init__(self, number: int):
        self.hands = [Hand()]
        self.number = number
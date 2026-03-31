class Player:
    def __init__(self, number: int, policy):
        self.hands = []
        self.number = number
        self.policy = policy
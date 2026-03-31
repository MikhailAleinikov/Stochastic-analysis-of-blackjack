from .card import Card, CardValue, Suit

card_suits = [
    Suit.SPADES,
    Suit.HEARTS,
    Suit.DIAMONDS,
    Suit.CLUBS
]
card_values = [
    CardValue.TWO,
    CardValue.THREE,
    CardValue.FOUR,
    CardValue.FIVE,
    CardValue.SIX,
    CardValue.SEVEN,
    CardValue.EIGHT,
    CardValue.NINE,
    CardValue.TEN,
    CardValue.JACK,
    CardValue.QUEEN,
    CardValue.KING,
    CardValue.ACE
]

class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.able_to_hit = True
        self.is_soft = True
        self.is_blackjack = False
        self.is_double = False

    def evaluate(self):
        output = 0
        number_of_aces = 0
        if [i.value for i in self.cards].count(CardValue.ACE) and sum([[i.value for i in self.cards].count(j) for j in
                                                                       [CardValue.TEN,
                                                                        CardValue.JACK,
                                                                        CardValue.QUEEN,
                                                                        CardValue.KING]]):
            self.is_blackjack = True
            return 21
        for card in self.cards:
            if card.value == CardValue.ACE:
                number_of_aces += 1
            else:
                output += [2,3,4,5,6,7,8,9,10,10,10,10][card_values.index(card.value)]
        for i in range(number_of_aces):
            if output + 11 > 21:
                output += 1
            else:
                output += 11
                self.is_soft = False
        return output


    def canSplit(self):
        if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value and self.able_to_hit:
            return True
        else:
            return False
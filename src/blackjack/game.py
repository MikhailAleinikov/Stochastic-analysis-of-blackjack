from .card import Card, Suit, CardValue
from .player import Player
from .dealer import Dealer
from .hand import Hand
import random

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


class Game:
    def __init__(self, num_players: int):
        standard_deck = []
        for i in enumerate(card_suits):
            for j in enumerate(card_values):
                standard_deck.append(Card(i[1], j[1]))
        print("Game started, deck reshuffled")
        random.shuffle(standard_deck)
        self.deck = standard_deck
        self.players = [Player(i + 1) for i in range(num_players)]
        self.dealer = Dealer()



    def giveCard(self, player, hand_index: int):
        if isinstance(player, Player):
            player.hands[hand_index].cards.append(self.deck.pop(0))
        elif isinstance(player, Dealer):
            player.hand.cards.append(self.deck.pop(0))


    def voiceHand(self, player: Player, hand_index: int):
        output = "Player " + str(player.number) + ", hand " + str(hand_index+1) + ": "
        for card in player.hands[hand_index].cards:
            output += '23456789TJQKA'[card_values.index(card.value)]
            output += '♠♥♦♣'[card_suits.index(card.suit)] + " "
        output += "| " + str(player.hands[hand_index].evaluate())
        if player.hands[hand_index].evaluate() > 21:
            output += " BUST"
        print(output)


    def startGame(self):
        for _ in range(2):
            for player in self.players:
                self.giveCard(player, 0)
            self.giveCard(self.dealer, 1)
        print("Dealer's card:    " + str('23456789TJQKA'[card_values.index(self.dealer.hand.cards[0].value)]) +
              '♠♥♦♣'[card_suits.index(self.dealer.hand.cards[0].suit)])
        for player in self.players:
            self.voiceHand(player, 0)

    def hit(self, player: Player, hand_index: int):
        if player.hands[hand_index].able_to_hit == True:
            self.giveCard(player, hand_index)
            self.voiceHand(player, hand_index)
            if player.hands[hand_index].evaluate() > 21:
                player.hands[hand_index].able_to_hit = False
        else:
            print("Player " + str(player.number) + " cannot hit anymore at hand " + str(hand_index+1))

    def stand(self, player: Player, hand_index: int):
        player.hands[hand_index].able_to_hit = False
        print("Player " + str(player.number) + " chose 'stand' at hand " + str(hand_index+1))

    def double(self, player: Player, hand_index: int):
        player.hands[hand_index].able_to_hit = False
        self.giveCard(player, hand_index)
        player.hands[hand_index].is_double = True
        print("Player " + str(player.number) + " chose 'double' at hand " + str(hand_index + 1))
        self.voiceHand(player, hand_index)

    def split(self, player_number: int, hand_index: int):
        player = self.players[player_number - 1]
        if not player.hands[hand_index].able_to_split:
            print("Unable to split")
            return
        player.hands.append([player.hands[hand_index].cards.pop(0)])
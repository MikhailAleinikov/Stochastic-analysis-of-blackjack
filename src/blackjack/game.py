from numpy.ma.core import shape

from .card import Card
from .rules import Suit, CardValue, Moves, GameState
from .player import Player
from .dealer import Dealer
from .hand import Hand
import random
import numpy as np

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
    def __init__(self, num_players: int, vocal=False):
        standard_deck = []
        for i in enumerate(card_suits):
            for j in enumerate(card_values):
                standard_deck.append(Card(i[1], j[1]))
        if vocal:
            print("Game started, deck reshuffled")
        random.shuffle(standard_deck)
        self.deck = standard_deck
        self.players = [Player(i + 1) for i in range(num_players)]
        self.dealer = Dealer()
        self.game_state = GameState.BETTING
        self.vocal = vocal


    def giveCard(self, player, hand_index: int):
        if isinstance(player, Player):
            player.hands[hand_index].cards.append(self.deck.pop(0))
        elif isinstance(player, Dealer):
            player.hand.cards.append(self.deck.pop(0))


    def voiceHand(self, hand: Hand):
        output = ""
        for card in hand.cards:
            output += '23456789TJQKA'[card_values.index(card.value)]
            output += '♠♥♦♣'[card_suits.index(card.suit)] + " "
        output += "| " + str(hand.evaluate())
        if hand.evaluate() > 21:
            output += " BUST"
        return output

    """
    def startGame(self):
        for _ in range(2):
            for player in self.players:
                self.giveCard(player, 0)
            self.giveCard(self.dealer, 1)
        print("Dealer's card:    " + str('23456789TJQKA'[card_values.index(self.dealer.hand.cards[0].value)]) +
              '♠♥♦♣'[card_suits.index(self.dealer.hand.cards[0].suit)])
        for player in self.players:
            self.voiceHand(player, 0)
    """

    def hit(self, player: Player, hand_index: int):
        if player.hands[hand_index].able_to_hit == True:
            self.giveCard(player, hand_index)
            if self.vocal:
                print("Player " + str(player.number) + ", hand " +
                      str(hand_index + 1) + ": " + self.voiceHand(player.hands[hand_index]))
            if player.hands[hand_index].evaluate() > 21:
                player.hands[hand_index].able_to_hit = False
        elif self.vocal:
            print("Player " + str(player.number) + " cannot hit anymore at hand " + str(hand_index+1))

    def stand(self, player: Player, hand_index: int):
        player.hands[hand_index].able_to_hit = False
        if self.vocal:
            print("Player " + str(player.number) + " chose 'stand' at hand " + str(hand_index+1))

    def double(self, player: Player, hand_index: int):
        player.hands[hand_index].able_to_hit = False
        self.giveCard(player, hand_index)
        player.hands[hand_index].is_double = True
        if self.vocal:
            print("Player " + str(player.number) + " chose 'double' at hand " + str(hand_index + 1))
            print("Player " + str(player.number) + ", hand " +
                  str(hand_index+1) + ": " + self.voiceHand(player.hands[hand_index]))

    def split(self, player: Player, hand_index: int):
        if not player.hands[hand_index].canSplit():
            if self.vocal:
                print("Unable to split")
            return
        new_hand = Hand()
        new_hand.cards.append(player.hands[hand_index].cards.pop(0))
        player.hands.append(new_hand)

    def takeBets(self):
        for player in self.players:
            player.hands = [Hand()]
            player.hands[0].bet = 1         # Taking fixed normalized bets is essential for a better analysis
            self.game_state = GameState.PLAYERS

    def dealInitialCards(self):
        for _ in range(2):
            for player in self.players:
                if player.hands[0].bet != 0:
                    self.giveCard(player, 0)
            self.giveCard(self.dealer, 0)

    def oneHandTurn(self, player: Player, hand_index, chooser):
        hand = player.hands[hand_index]
        choice = chooser(hand)
        if choice == Moves.STAND:
            self.stand(player, hand_index)
        elif choice not in hand.getLegalMoves():
            if self.vocal:
                print("Invalid move")
            self.oneHandTurn(hand, chooser)
            return
        elif choice == Moves.SPLIT:
            self.split(player, hand_index)
        elif choice == Moves.DOUBLE:
            self.double(player, hand_index)
        elif choice == Moves.HIT:
            self.hit(player, hand_index)

    def round(self, chooser):
        if all(not any([hand.able_to_hit for hand in player.hands]) for player in self.players):
            if self.vocal:
                print("All players have been dealt")
                print("Dealer's cards: " + self.voiceHand(self.dealer.hand))
            self.game_state = GameState.DEALER
            return
        for player in self.players:
            for i in range(len(player.hands)):
                self.oneHandTurn(player, i, chooser)

    def dealerTurns(self):
        while self.dealer.hand.evaluate() < 17:
            self.giveCard(self.dealer, 0)
        self.game_state = GameState.SETTLEMENTS

    # note that settlements are differences between initial and after-game player's balance
    def Settlements(self):
        settlements = np.zeros(len(self.players), 4)
        for j in range(len(self.players)):
            player = self.players[j]
            for i in range(len(player.hands)):
                if player.hands[i].evaluate() > 21:
                    settlements[j, i] = -player.hands[i].bet
                elif player.hands[i].isBlackjack():
                    if not self.dealer.hand.isBlackjack():
                        settlements[j, i] = player.hands[i].bet * 0.5
                elif self.dealer.hand.evaluate() > 21:
                    settlements[j, i] = player.hands[i].bet
                elif player.hands[i].evaluate() > self.dealer.hand.evaluate():
                    settlements[j, i] = player.hands[i].bet
                elif player.hands[i].evaluate() == self.dealer.hand.evaluate():
                    if player.hands[i].isBlackjack() and self.dealer.hand.isBlackjack():
                        settlements[j, i] = 0
                    elif (not player.hands[i].isBlackjack()) and self.dealer.hand.isBlackjack():
                        settlements[j, i] = -player.hands[i].bet
                    else:
                        settlements[j, i] = 0
                elif player.hands[i].evaluate() < self.dealer.hand.evaluate():
                    settlements[j, i] = -player.hands[i].bet



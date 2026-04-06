"""
1. Приватные методы
2. Константы не повторять
3. Нэйминг debug
4. В какой класс лучше опрелять методы game
5* Обращение к вложенным полям лучше исключить
6. Error handling
"""
from ..rules import GameState
from .logger import Logger

def runOneGame(policies,
               number_of_players: int = 5,
               logger: Logger | None = None,
               vocal=False,
               round_id=0,
               simulation_id: str | None = None,):
    from ..game import Game
    game = Game(number_of_players, round_id, policies, vocal=vocal)
    game.takeBets()
    game.dealInitialCards()
    while game.checkDealing():
        for player in game.players:
            for i in range(len(player.hands)):
                if player.hands[i].able_to_hit:
                    game.oneHandTurn(player, i, logger=logger, simulation_id=simulation_id)
    game.game_state = GameState.DEALER
    game.dealerTurns()
    return game.settlements(logger=logger)

def runFromAPoint(game,
                  last_player_id: int = 1,
                  last_hand_id: int = -1,
                  simulation_id: str | None = None,
                  logger: Logger | None = None,):
    if game.game_state == GameState.BETTING:
        game.takeBets()
        game.dealInitialCards()
    if game.game_state == GameState.PLAYERS:
        player_id = last_player_id
        hand_id = last_hand_id + 1
        while game.checkDealing():
            while player_id <= len(game.players):
                while hand_id < len(game.players[player_id-1].hands):
                    #print(player_id, hand_id)
                    if game.players[player_id-1].hands[hand_id].able_to_hit:
                        game.oneHandTurn(game.players[player_id-1], hand_id, logger=logger, simulation_id=simulation_id)
                    hand_id += 1
                hand_id = 0
                player_id += 1
            player_id = 1
        game.game_state = GameState.DEALER
    if game.game_state == GameState.DEALER:
        game.dealerTurns()
        return game.settlements(logger=logger, simulation_id=simulation_id)
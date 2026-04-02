
from ..rules import GameState
from .logger import Logger

def runOneGame(policies,
               number_of_players: int = 5,
               logger: Logger | None = None,
               vocal=False,
               round_id=0):
    from ..game import Game
    game = Game(number_of_players, round_id, policies, vocal=vocal)
    game.takeBets()
    game.dealInitialCards()
    while game.checkDealing():
        for player in game.players:
            for i in range(len(player.hands)):
                if player.hands[i].able_to_hit:
                    game.oneHandTurn(player, i, logger=logger)
    game.game_state = GameState.DEALER
    game.dealerTurns()
    return game.settlements(logger=logger)
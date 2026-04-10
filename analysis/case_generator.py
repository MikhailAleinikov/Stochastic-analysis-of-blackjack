import sys
import os

sys.path.append(os.path.abspath("../src"))
from blackjack import Game, Moves
from blackjack.analysis import Logger, DecisionState
from blackjack.analysis.monte_carlo.ev import estimateMoveEv
from blackjack.strategy import fixedStrategy

def generateCase(player_hand: list[int], dealer_upcard: int, path: str, se_threshold=0.005, debug=False):
    game = Game(1, 0, [fixedStrategy])
    game.takeBets()
    for card in player_hand:
        game.giveCard(game.players[0], 0, card)
    game.giveCard(game.dealer, 0, dealer_upcard)
    logger = Logger(1)
    for number_of_aces in range(game.card_count[11]+1):
        game.card_count[11] = number_of_aces
        for number_of_tens in range(game.card_count[10]+1):
            if debug: print(number_of_aces, number_of_tens)
            game.card_count[10] = number_of_tens
            data = [estimateMoveEv(move,
                                    1000,
                                    game,
                                    1,
                                    0,
                                    logger=None,
                                    max_recursion_depth=2,
                                    adaptive_stopping=True,
                                    minimum_iterations_branches=50,
                                    down_factor_hit=3,
                                    down_factor_split=5,
                                    se_threshold=se_threshold,
                                    batch_size=70,
                                    ) if move in game.players[0].hands[0].getLegalMoves() else [None, None] for move in [Moves.HIT, Moves.STAND, Moves.DOUBLE, Moves.SPLIT]]

            hit_ev, stand_ev, double_ev, split_ev = [i[0] for i in data]
            hit_se, stand_se, double_se, split_se = [i[1] for i in data]
            decision_state = DecisionState(game.players[0].hands[0], game.dealer.hand.cards[0], game.card_count)
            best_move = ["Hit", "Stand", "Double", "Split"][[hit_ev, stand_ev, double_ev, split_ev].index(max(i if i is not None else -2 for i in
                                                                                                              [hit_ev, stand_ev, double_ev, split_ev]))]
            logger.log_evs(decision_state,
                           hit_ev,
                           stand_ev, double_ev, split_ev, hit_se, stand_se, double_se, split_se, best_move, fixed_strategy_move=fixedStrategy(decision_state).value)
    logger.save_evs_csv(path)
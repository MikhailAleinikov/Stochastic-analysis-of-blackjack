from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from ...rules import Moves
from ...strategy import fixedStrategy
from .ev_double import estimateDoubleEV
from .ev_hit import estimateHitEV
from .ev_stand import estimateStandEV
from .ev_split import estimateSplitEV
from .sim_state import SimState

if TYPE_CHECKING:
    from blackjack.analysis.logger import Logger


def estimateMoveEv(move: Moves,
            number_of_experiments: int, #per branch
            game,
            player_id: int,
            hand_id: int,
            logger: Logger|None = None,
            max_recursion_depth = 2,
            adaptive_stopping: bool = False,
            minimum_iterations_branches: int = 3,
            down_factor_hit: int = 5,
            down_factor_split: int = 5,
            se_threshold: float = 0.01,
            batch_size: int = 100,
            debug: bool = False,):
    available_actions = game.players[player_id-1].hands[hand_id].getLegalMoves()
    if move not in available_actions:
        raise ValueError("Invalid move")
    if not adaptive_stopping:
        if move == Moves.SPLIT:
            return np.mean(estimateSplitEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                    number_of_experiments,
                                    game.round_id,
                                    player_id,
                                    hand_id,
                                    game.players[player_id-1].hands[hand_id].decision_id,
                                    fixedStrategy,
                                    logger=logger,
                                    recursion_depth=max_recursion_depth,
                                   minimum_iterations_branches=minimum_iterations_branches,
                                   down_factor=down_factor_split))
        if move == Moves.HIT:
            return np.mean(estimateHitEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                    number_of_experiments,
                                    game.round_id,
                                    player_id,
                                    hand_id,
                                    game.players[player_id-1].hands[hand_id].decision_id,
                                    fixedStrategy,
                                    logger=logger,
                                    recursion_depth=max_recursion_depth,
                                 minimum_iterations_branches=minimum_iterations_branches,
                                 down_factor=down_factor_hit))
        if move == Moves.DOUBLE:
            return np.mean(estimateDoubleEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                    number_of_experiments,
                                    game.round_id,
                                    player_id,
                                    hand_id,
                                    game.players[player_id-1].hands[hand_id].decision_id,
                                    logger=logger,))
        if move == Moves.STAND:
            return estimateStandEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                    number_of_experiments,
                                    game.round_id,
                                    player_id,
                                    hand_id,
                                    game.players[player_id-1].hands[hand_id].decision_id,
                                    logger=logger,)
    else:
        number_of_batches = 0
        data = np.array([])
        se = 1.0
        while se > se_threshold:
            number_of_batches += 1
            if move == Moves.SPLIT:
                data = np.concatenate([data, estimateSplitEV(
                    SimState(game.players[player_id - 1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                    batch_size,
                    game.round_id,
                    player_id,
                    hand_id,
                    game.players[player_id - 1].hands[hand_id].decision_id,
                    fixedStrategy,
                    logger=logger,
                    recursion_depth=max_recursion_depth,
                    minimum_iterations_branches=minimum_iterations_branches,
                    down_factor=down_factor_split)])
            if move == Moves.HIT:
                data = np.concatenate([data, estimateHitEV(
                    SimState(game.players[player_id - 1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                    batch_size,
                    game.round_id,
                    player_id,
                    hand_id,
                    game.players[player_id - 1].hands[hand_id].decision_id,
                    fixedStrategy,
                    logger=logger,
                    recursion_depth=max_recursion_depth,
                    minimum_iterations_branches=minimum_iterations_branches,
                    down_factor=down_factor_hit)])
            if move == Moves.DOUBLE:
                data = np.concatenate([data, estimateDoubleEV(
                    SimState(game.players[player_id - 1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                    batch_size,
                    game.round_id,
                    player_id,
                    hand_id,
                    game.players[player_id - 1].hands[hand_id].decision_id,
                    logger=logger, )])
            if move == Moves.STAND:
                data = np.concatenate([data, estimateStandEV(
                    SimState(game.players[player_id - 1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                    batch_size,
                    game.round_id,
                    player_id,
                    hand_id,
                    game.players[player_id - 1].hands[hand_id].decision_id,
                    logger=logger, )])
            se = np.std(data)/np.sqrt(np.size(data, 0))
        if debug:
            print("batches:", number_of_batches)
            print("final n:", data.size)
            print("final se:", se)
        return [np.mean(data), se]




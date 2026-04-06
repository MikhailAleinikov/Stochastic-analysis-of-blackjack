from __future__ import annotations
from typing import TYPE_CHECKING

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
            max_recursion_depth = 2,):
    available_actions = game.players[player_id-1].hands[hand_id].getLegalMoves()
    if move not in available_actions:
        raise ValueError("Invalid move")
    if move == Moves.SPLIT:
        return estimateSplitEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                number_of_experiments,
                                game.round_id,
                                player_id,
                                hand_id,
                                game.players[player_id-1].hands[hand_id].decision_id,
                                fixedStrategy,
                                logger=logger,
                                recursion_depth=max_recursion_depth,)
    if move == Moves.HIT:
        return estimateHitEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                number_of_experiments,
                                game.round_id,
                                player_id,
                                hand_id,
                                game.players[player_id-1].hands[hand_id].decision_id,
                                fixedStrategy,
                                logger=logger,
                                recursion_depth=max_recursion_depth,)
    if move == Moves.DOUBLE:
        return estimateDoubleEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                number_of_experiments,
                                game.round_id,
                                player_id,
                                hand_id,
                                game.players[player_id-1].hands[hand_id].decision_id,
                                logger=logger,)
    if move == Moves.STAND:
        return estimateStandEV(SimState(game.players[player_id-1].hands[hand_id], game.dealer.hand.cards[0], game.card_count),
                                number_of_experiments,
                                game.round_id,
                                player_id,
                                hand_id,
                                game.players[player_id-1].hands[hand_id].decision_id,
                                logger=logger,)



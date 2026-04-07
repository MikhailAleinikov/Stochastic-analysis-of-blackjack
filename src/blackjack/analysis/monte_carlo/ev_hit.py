from .sim_state import SimState
from .eval_hand_from_int import evalHandFromInt
from .give_reward import giveReward
from .random_card import randomCard
from ..logger import Logger
from ...rules import Moves
from .hand_to_str import handToStr
from .ev_stand import estimateStandEV
import numpy as np

def estimateHitEV(
    state: SimState,
    number_of_iterations: int,
    round_id: int,
    player_id: int,
    hand_id: int,
    decision_id: int,
    strategy_after_recursion,
    logger: Logger | None = None,
    simulation_prefix: str = "",
    recursion_depth: int = 3,
    minimum_iterations_branches: int = 3,
    down_factor: int = 5,
):
    cache = {}
    return _estimateHitEV_inner(
        state=state,
        number_of_iterations=number_of_iterations,
        round_id=round_id,
        player_id=player_id,
        hand_id=hand_id,
        decision_id=decision_id,
        strategy_after_recursion=strategy_after_recursion,
        logger=logger,
        simulation_prefix=simulation_prefix,
        recursion_depth=recursion_depth,
        cache=cache,
    )



def _estimateHitEV_inner(state: SimState,
                     number_of_iterations: int,
                     round_id: int,
                     player_id: int,
                     hand_id: int,
                     decision_id: int,
                     strategy_after_recursion,
                     cache: dict|None = None,
                     logger: Logger | None = None,
                     simulation_prefix: str = "",
                     recursion_depth: int = 3,
                     minimum_iterations_branches: int = 3,
                     down_factor: int = 5,):
    if cache is None:
        cache = {}
    rewards = np.zeros(number_of_iterations)
    key = (
        tuple(sorted(state.cards)),
        state.dealer_upcard,
        tuple(sorted(state.card_count.items())),
        state.bet,
        state.is_split,
        recursion_depth,
        number_of_iterations,
    )
    if key in cache:
        return cache[key]
    for sim_id in range(number_of_iterations):
        sim_state = state.clone()
        current_sim_id = f"{simulation_prefix}.{sim_id}" if simulation_prefix else str(sim_id)

        if logger is not None:
            logger.log_decision(round_id,
                                player_id,
                                hand_id,
                                decision_id,
                                sim_state,
                                Moves.HIT,
                                simulation_id=current_sim_id,)
        dealer_cards = [sim_state.dealer_upcard]
        new_card = randomCard(sim_state.card_count)
        sim_state.withdrawCardFromDeck(new_card)
        sim_state.cards.append(new_card)

        if sim_state.total > 21:
            rewards[sim_id] = -sim_state.bet
            if logger is not None:
                logger.log_reward(round_id,
                                  player_id,
                                  hand_id,
                                  -sim_state.bet,
                                  evalHandFromInt(dealer_cards),
                                  handToStr(dealer_cards),
                                  outcome="Bust",
                                  simulation_id=current_sim_id,
                                  )
        elif recursion_depth > 0:
            rewards[sim_id] = max(np.mean(estimateStandEV(sim_state,
                                       max(number_of_iterations // down_factor, minimum_iterations_branches),
                                       round_id,
                                       player_id,
                                       hand_id,
                                       decision_id+1,
                                       logger=None,
                                       simulation_prefix=current_sim_id)),
                      np.mean(_estimateHitEV_inner(sim_state,
                                       max(number_of_iterations // down_factor, minimum_iterations_branches),
                                       round_id,
                                       player_id,
                                       hand_id,
                                       decision_id + 1,
                                       strategy_after_recursion,
                                       cache=cache,
                                       logger=None,
                                       simulation_prefix=current_sim_id,
                                     recursion_depth=recursion_depth - 1)),
                      )
        else:
            while strategy_after_recursion(sim_state) != Moves.STAND:
                if logger is not None:
                    logger.log_decision(round_id,
                                        player_id,
                                        hand_id,
                                        decision_id,
                                        sim_state,
                                        Moves.HIT,
                                        simulation_id=current_sim_id, )
                new_card = randomCard(sim_state.card_count)
                sim_state.withdrawCardFromDeck(new_card)
                sim_state.cards.append(new_card)
            while evalHandFromInt(dealer_cards) < 17:
                new_card = randomCard(sim_state.card_count)
                dealer_cards.append(new_card)
                sim_state.withdrawCardFromDeck(new_card)
            rewards[sim_id] = giveReward(sim_state.total,
                              sim_state.is_blackjack,
                             sim_state.is_split,
                              sim_state.bet,
                              evalHandFromInt(dealer_cards),
                              sorted(dealer_cards) == [10, 11],
                              handToStr(dealer_cards),
                              round_id,
                              player_id,
                              hand_id,
                              logger=logger,
                              simulation_id=current_sim_id
            )
    cache[key] = rewards
    return rewards
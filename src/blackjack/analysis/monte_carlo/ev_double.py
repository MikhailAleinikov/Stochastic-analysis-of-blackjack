import numpy as np

from .sim_state import SimState
from .eval_hand_from_int import evalHandFromInt
from .give_reward import giveReward
from .random_card import randomCard
from ..logger import Logger
from ...rules import Moves
from .hand_to_str import handToStr


def estimateDoubleEV(state: SimState,
                     number_of_iterations: int,
                     round_id: int,
                     player_id: int,
                     hand_id: int,
                     decision_id: int,
                     logger: Logger | None = None,
                     simulation_prefix: str = ""):
    rewards = np.zeros(number_of_iterations)
    for sim_id in range(number_of_iterations):
        sim_state = state.clone()
        current_sim_id = f"{simulation_prefix}.{sim_id}" if simulation_prefix else str(sim_id)
        if logger is not None:
            logger.log_decision(round_id,
                                player_id,
                                hand_id,
                                decision_id,
                                sim_state,
                                Moves.DOUBLE,
                                simulation_id=current_sim_id)
        dealer_cards = [sim_state.dealer_upcard]
        new_card = randomCard(sim_state.card_count)
        sim_state.withdrawCardFromDeck(new_card)
        sim_state.cards.append(new_card)
        sim_state.bet = sim_state.bet*2
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
        else:
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
    return rewards
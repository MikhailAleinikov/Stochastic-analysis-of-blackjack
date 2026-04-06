from .sim_state import SimState
from .random_card import randomCard
from ..logger import Logger
from ...rules import Moves
from .ev_stand import estimateStandEV
from .ev_hit import estimateHitEV
from .ev_double import estimateDoubleEV

def estimateSplitEV(state: SimState,
                     number_of_iterations: int,
                     round_id: int,
                     player_id: int,
                     hand_id: int,
                   decision_id: int,
                    strategy_after_recursion,
                     logger: Logger | None = None,
                     simulation_prefix: str = "",
                     recursion_depth: int = 3,):
    ev = 0
    for sim_id in range(number_of_iterations):
        inter_factor = 10
        current_sim_id = f"{simulation_prefix}.{sim_id}" if simulation_prefix else str(sim_id)
        if logger is not None:
            logger.log_decision(round_id,
                                player_id,
                                hand_id,
                                decision_id,
                                state,
                                Moves.SPLIT,
                                simulation_id=current_sim_id)
        sim_state_one = state.clone()
        sim_state_one.cards.pop(1)
        sim_state_two = state.clone()
        sim_state_two.cards.pop(0)
        new_card_one = randomCard(sim_state_one.card_count)
        sim_state_one.cards.append(new_card_one)
        sim_state_one.withdrawCardFromDeck(new_card_one)
        new_card_two = randomCard(sim_state_two.card_count)
        sim_state_two.cards.append(new_card_two)
        sim_state_two.withdrawCardFromDeck(new_card_two)
        """
        if recursion_depth > 0:
            secondary_split_ev_one = estimateSplitEV(sim_state_one,
                                           max(number_of_iterations // 20, 2),
                                           round_id,
                                           player_id,
                                           hand_id,
                                           decision_id + 1,
                                         strategy_after_recursion,
                                           logger=None,
                                           simulation_prefix=current_sim_id+".L",
                                         recursion_depth=recursion_depth - 1) if sim_state_one.is_pair else -1
            secondary_split_ev_two = estimateSplitEV(sim_state_two,
                                                       max(number_of_iterations // 20, 2),
                                                       round_id,
                                                       player_id,
                                                       hand_id,
                                                       decision_id + 1,
                                                       strategy_after_recursion,
                                                       logger=None,
                                                       simulation_prefix=current_sim_id + ".R",
                                                       recursion_depth=recursion_depth - 1) if sim_state_two.is_pair else -1
        else:
            secondary_split_ev_one = -1
            secondary_split_ev_two = -1
        ev1 = max(estimateStandEV(sim_state_one,
                                       max(number_of_iterations//20, 2),
                                       round_id,
                                       player_id,
                                       hand_id,
                                       decision_id+1,
                                       logger=None,
                                       simulation_prefix=current_sim_id+".L"),
                      estimateHitEV(sim_state_one,
                                       max(number_of_iterations // 20, 2),
                                       round_id,
                                       player_id,
                                       hand_id,
                                       decision_id + 1,
                                     strategy_after_recursion,
                                       logger=None,
                                       simulation_prefix=current_sim_id+".L",
                                     recursion_depth=recursion_depth - 1),
                  estimateDoubleEV(sim_state_one,
                                 max(number_of_iterations // 20, 2),
                                 round_id,
                                 player_id,
                                 hand_id,
                                 decision_id + 1,
                                 logger=None,
                                 simulation_prefix=current_sim_id+".L"),
                  secondary_split_ev_one,
                      )
        ev2 = max(estimateStandEV(sim_state_two,
                                   max(number_of_iterations // 20, 2),
                                   round_id,
                                   player_id,
                                   hand_id,
                                   decision_id + 1,
                                   logger=None,
                                   simulation_prefix=current_sim_id + ".R"),
                  estimateHitEV(sim_state_two,
                                 max(number_of_iterations // 20, 2),
                                 round_id,
                                 player_id,
                                 hand_id,
                                 decision_id + 1,
                                 strategy_after_recursion,
                                 logger=None,
                                 simulation_prefix=current_sim_id + ".R",
                                 recursion_depth=recursion_depth - 1),
                  estimateDoubleEV(sim_state_two,
                                    max(number_of_iterations // 20, 2),
                                    round_id,
                                    player_id,
                                    hand_id,
                                    decision_id + 1,
                                    logger=None,
                                    simulation_prefix=current_sim_id+".R"),
                  secondary_split_ev_two,
                  )
        """
        choice_one = strategy_after_recursion(sim_state_one)
        choice_two = strategy_after_recursion(sim_state_two)
        if choice_one == Moves.STAND:
            ev1 = estimateStandEV(sim_state_one,
                                  max(number_of_iterations // inter_factor, 2),
                                  round_id,
                                  player_id,
                                  hand_id,
                                  decision_id + 1,
                                  logger=None,
                                  simulation_prefix=current_sim_id + ".L",)
        elif choice_one == Moves.DOUBLE:
            ev1 = estimateDoubleEV(sim_state_one,
                                  max(number_of_iterations // inter_factor, 2),
                                  round_id,
                                  player_id,
                                  hand_id,
                                  decision_id + 1,
                                  logger=None,
                                  simulation_prefix=current_sim_id + ".L", )
        elif choice_one == Moves.HIT:
            ev1 = estimateHitEV(sim_state_one,
                                  max(number_of_iterations // inter_factor, 2),
                                  round_id,
                                  player_id,
                                  hand_id,
                                  decision_id + 1,
                                  logger=None,
                                  simulation_prefix=current_sim_id + ".L",
                                recursion_depth=recursion_depth - 1,
                                strategy_after_recursion=strategy_after_recursion)
        else:
            ev1 = estimateSplitEV(sim_state_one,
                                max(number_of_iterations // inter_factor, 2),
                                round_id,
                                player_id,
                                hand_id,
                                decision_id + 1,
                                logger=None,
                                simulation_prefix=current_sim_id + ".L",
                                recursion_depth=recursion_depth - 1,
                                strategy_after_recursion=strategy_after_recursion)

        if choice_two == Moves.STAND:
            ev2 = estimateStandEV(sim_state_two,
                                  max(number_of_iterations // inter_factor, 2),
                                  round_id,
                                  player_id,
                                  hand_id,
                                  decision_id + 1,
                                  logger=None,
                                  simulation_prefix=current_sim_id + ".R", )
        elif choice_two == Moves.DOUBLE:
            ev2 = estimateDoubleEV(sim_state_two,
                                   max(number_of_iterations // inter_factor, 2),
                                   round_id,
                                   player_id,
                                   hand_id,
                                   decision_id + 1,
                                   logger=None,
                                   simulation_prefix=current_sim_id + ".R", )
        elif choice_two == Moves.HIT:
            ev2 = estimateHitEV(sim_state_two,
                                max(number_of_iterations // inter_factor, 2),
                                round_id,
                                player_id,
                                hand_id,
                                decision_id + 1,
                                logger=None,
                                simulation_prefix=current_sim_id + ".R",
                                recursion_depth=recursion_depth - 1,
                                strategy_after_recursion=strategy_after_recursion)
        else:
            ev2 = estimateSplitEV(sim_state_two,
                                  max(number_of_iterations // inter_factor, 2),
                                  round_id,
                                  player_id,
                                  hand_id,
                                  decision_id + 1,
                                  logger=None,
                                  simulation_prefix=current_sim_id + ".R",
                                  recursion_depth=recursion_depth - 1,
                                  strategy_after_recursion=strategy_after_recursion)
            

        ev += ev1+ev2
    return ev/number_of_iterations

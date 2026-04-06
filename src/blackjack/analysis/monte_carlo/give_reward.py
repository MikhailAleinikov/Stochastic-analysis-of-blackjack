from ..logger import Logger

def giveReward(total: int,
                is_blackjack: bool,
               is_split: bool,
                bet: float,
                dealer_total: int,
                dealer_is_blackjack: bool,
                dealer_hand_repr: str,
                round_id: int,
                player_id: int,
                hand_id: int,
                simulation_id: str,
                logger: Logger|None = None):
    reward = 0
    if total > 21:
        reward = -bet
        if logger is not None: logger.log_reward(round_id,
                                                 player_id,
                                                 hand_id,
                                                 -bet,
                                                 dealer_total,
                                                 dealer_hand_repr,
                                                 outcome="Bust",
                                                 simulation_id=simulation_id)
    elif is_blackjack and not is_split:
        if not dealer_is_blackjack:
            reward = bet * 1.5
            if logger is not None: logger.log_reward(round_id, player_id, hand_id,
                                                     bet * 1.5,
                                                     dealer_total,
                                                     dealer_hand_repr,
                                                     outcome="Blackjack",
                                                     simulation_id=simulation_id)
    elif dealer_total > 21 or total > dealer_total:
        reward = bet
        if logger is not None: logger.log_reward(round_id,
                                                 player_id,
                                                 hand_id,
                                                 bet,
                                                 dealer_total,
                                                 dealer_hand_repr,
                                                 outcome="Win",
                                                 simulation_id=simulation_id)
    elif total == dealer_total:
        if is_blackjack and dealer_is_blackjack:
            reward = 0
            if logger is not None: logger.log_reward(round_id,
                                                     player_id,
                                                     hand_id,
                                                     0,
                                                     dealer_total,
                                                     dealer_hand_repr,
                                                     outcome="Tie",
                                                     simulation_id=simulation_id)
        elif (not is_blackjack) and dealer_is_blackjack:
            reward = -bet
            if logger is not None: logger.log_reward(round_id,
                                                     player_id,
                                                     hand_id,
                                                     -bet,
                                                     dealer_total,
                                                     dealer_hand_repr,
                                                     outcome="Lose",
                                                     simulation_id=simulation_id)
        else:
            reward = 0
            if logger is not None: logger.log_reward(round_id,
                                                     player_id,
                                                     hand_id,
                                                     0,
                                                     dealer_total,
                                                     dealer_hand_repr,
                                                     outcome="Tie",
                                                     simulation_id=simulation_id)
    elif total < dealer_total:
        reward = -bet
        if logger is not None: logger.log_reward(round_id, player_id, hand_id,
                                                 -bet,
                                                 dealer_total,
                                                 dealer_hand_repr,
                                                 outcome="Lose",
                                                 simulation_id=simulation_id)
    return reward
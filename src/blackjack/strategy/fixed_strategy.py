from ..analysis.decision_state import DecisionState
from ..analysis.monte_carlo.sim_state import SimState
from ..rules import Moves

def fixedStrategy(decision_state):
    if isinstance(decision_state, DecisionState):
        cards = [i.toInt() for i in decision_state.cards]
        dealer_upcard = decision_state.dealer_upcard.toInt()
    elif isinstance(decision_state, SimState):
        cards = decision_state.cards
        dealer_upcard = decision_state.dealer_upcard
    else: raise TypeError("Invalid decision state")
    if Moves.SPLIT in decision_state.legal_moves:
        if cards[0] == cards[1] == 8 or cards[0] == cards[1] == 11:
            return Moves.SPLIT
    if Moves.DOUBLE in decision_state.legal_moves:
        if decision_state.total == 11 and dealer_upcard != 11:
            return Moves.DOUBLE
        elif decision_state.total == 10 and dealer_upcard not in [2,3,4,5,6,7,8,9]:
            return Moves.DOUBLE
        elif decision_state.total == 9 and dealer_upcard not in [3,4,5,6]:
            return Moves.DOUBLE
    if Moves.HIT in decision_state.legal_moves:
        if not decision_state.is_soft:
            if decision_state.total >= 17:
                return Moves.STAND
            elif 12 <= decision_state.total <= 17:
                if dealer_upcard in [2,3,4,5,6]:
                    return Moves.STAND
                else:
                    return Moves.HIT
            else:
                return Moves.HIT
        else:
            if decision_state.total >= 19:
                return Moves.STAND
            elif decision_state.total == 18:
                if dealer_upcard in [2,7,8]:
                    return Moves.STAND
                else:
                    return Moves.HIT
            else:
                return Moves.HIT
    return Moves.STAND


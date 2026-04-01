from ..analysis.decision_state import DecisionState
from ..rules import Moves, CardValue

def fixedStrategy(decision_state: DecisionState):
    cards = [i.value for i in decision_state.cards]
    if Moves.SPLIT in decision_state.legal_moves:
        if cards[0] == cards[1] == CardValue.EIGHT or cards[0] == cards[1] == CardValue.ACE:
            return Moves.SPLIT
    if Moves.DOUBLE in decision_state.legal_moves:
        if decision_state.total == 11 and decision_state.dealer_upcard.value != CardValue.ACE:
            return Moves.DOUBLE
        elif decision_state.total == 10 and decision_state.dealer_upcard.value not in [
            CardValue.TWO,
            CardValue.THREE,
            CardValue.FOUR,
            CardValue.FIVE,
            CardValue.SIX,
            CardValue.SEVEN,
            CardValue.EIGHT,
            CardValue.NINE,
        ]:
            return Moves.DOUBLE
        elif decision_state.total == 9 and decision_state.dealer_upcard.value not in [
            CardValue.THREE,
            CardValue.FOUR,
            CardValue.FIVE,
            CardValue.SIX,
        ]:
            return Moves.DOUBLE
    if Moves.HIT in decision_state.legal_moves:
        if not decision_state.is_soft:
            if decision_state.total >= 17:
                return Moves.STAND
            elif 12 <= decision_state.total <= 17:
                if decision_state.dealer_upcard.value in [
                    CardValue.TWO,
                    CardValue.THREE,
                    CardValue.FOUR,
                    CardValue.FIVE,
                    CardValue.SIX
                ]:
                    return Moves.STAND
                else:
                    return Moves.HIT
            else:
                return Moves.HIT
        else:
            if decision_state.total >= 19:
                return Moves.STAND
            elif decision_state.total == 18:
                if decision_state.dealer_upcard.value in [
                    CardValue.TWO,
                    CardValue.SEVEN,
                    CardValue.EIGHT
                ]:
                    return Moves.STAND
                else:
                    return Moves.HIT
            else:
                return Moves.HIT
    return Moves.STAND


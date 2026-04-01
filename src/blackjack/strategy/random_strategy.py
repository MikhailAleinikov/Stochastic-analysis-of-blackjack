from ..analysis.decision_state import DecisionState
import random

def randomStrategy(decision_state: DecisionState):
    return random.choice(decision_state.legal_moves)
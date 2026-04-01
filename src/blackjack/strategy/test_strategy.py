from ..analysis.decision_state import DecisionState
from ..rules import Moves

def testStrategy(decision_state: DecisionState, iterations=0):
    iterations += 1
    choice = input()
    if choice == "hit":
        return Moves.HIT
    elif choice == "stand":
        return Moves.STAND
    elif choice == "split":
        return Moves.SPLIT
    elif choice == "double":
        return Moves.DOUBLE
    elif iterations == 2:
        return Moves.STAND
    else:
        print("invalid choice")
        return testStrategy(decision_state, iterations)

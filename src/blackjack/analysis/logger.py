import pandas as pd
from .monte_carlo.hand_to_str import handToStr
from .decision_state import DecisionState


class Logger:
    def __init__(self, focal_player_id: int):
        self.decision_records = []
        self.outcome_records = []
        self.ev_records = []
        self.focal_player_id = focal_player_id

    def log_decision(self, round_id, player_id, hand_id, decision_id, state, action, simulation_id: str | None = None):
        if player_id != self.focal_player_id: return
        self.decision_records.append({
            "round_id": round_id,
            "simulation_id": simulation_id,
            "player_id": player_id,
            "hand_id": hand_id,
            "decision_index": decision_id,
            "action": action.value,
            "hand_repr": "".join(card.value.value for card in state.cards) if isinstance(state, DecisionState)
            else handToStr(state.cards),
            "dealer_upcard": state.dealer_upcard.value.value if isinstance(state, DecisionState)
            else handToStr([state.dealer_upcard]),
            "bet": state.bet,
            "n_cards": len(state.cards),
            "total": state.total,
            "soft": state.is_soft,
            "is_pair": state.is_pair,
            "is_blackjack": state.is_blackjack,
            "legal_moves": ",".join(move.value for move in state.legal_moves),
            "remaining_cards": sum(state.card_count.values()),
            "two_density": state.card_count[2] / sum(state.card_count.values()),
            "three_density": state.card_count[3] / sum(state.card_count.values()),
            "four_density": state.card_count[4] / sum(state.card_count.values()),
            "five_density": state.card_count[5] / sum(state.card_count.values()),
            "six_density": state.card_count[6] / sum(state.card_count.values()),
            "seven_density": state.card_count[7] / sum(state.card_count.values()),
            "eight_density": state.card_count[8] / sum(state.card_count.values()),
            "nine_density": state.card_count[9] / sum(state.card_count.values()),
            "ten_density": state.card_count[10] / sum(state.card_count.values()),
            "ace_density": state.card_count[11] / sum(state.card_count.values()),
            "dealer_upcard_group": (10 if state.dealer_upcard.value.value in ["T", "J", "Q", "K"]
                else 11 if state.dealer_upcard.value.value == "A"
                else int(state.dealer_upcard.value.value)) if isinstance(state, DecisionState)
            else state.dealer_upcard,
        })

    def log_evs(self,
                state: DecisionState,
                ev_hit: float|None,
                ev_stand: float|None,
                ev_double: float|None,
                ev_split: float|None,
                hit_se: float|None,
                stand_se: float|None,
                double_se: float|None,
                split_se: float|None,
                best_move: str,
                fixed_strategy_move: str,):
        self.ev_records.append({
            "hand_repr": ",".join([str(card.toInt()) for card in state.cards]),
            "total": state.total,
            "dealer_upcard": state.dealer_upcard.toInt(),
            "bet": state.bet,
            "soft": state.is_soft,
            "is_pair": state.is_pair,
            "remaining_cards": sum(state.card_count.values()),
            "low_density": sum(state.card_count[i] / sum(state.card_count.values()) for i in [2,3,4,5,6]),
            "ten_density": state.card_count[10] / sum(state.card_count.values()),
            "ace_density": state.card_count[11] / sum(state.card_count.values()),
            "ev_hit": ev_hit,
            "ev_stand": ev_stand,
            "ev_double": ev_double,
            "ev_split": ev_split,
            "best_move": best_move,
            "ev_gap": sorted([ev if ev is not None else -2 for ev in [ev_stand, ev_double, ev_split, ev_hit]], reverse=True)[0]
            - sorted([ev if ev is not None else -2 for ev in [ev_stand, ev_double, ev_split, ev_hit]], reverse=True)[1],
            "hit_se": hit_se,
            "stand_se": stand_se,
            "double_se": double_se,
            "split_se": split_se,
            "fixed_strategy_move": fixed_strategy_move,
        })


    def log_reward(self,
                   round_id: int,
                   player_id: int,
                   hand_id: int,
                   reward: float,
                   dealer_total: int,
                   dealer_hand: str,
                   simulation_id: str | None = None,
                   outcome: str | None = None,):
        if player_id != self.focal_player_id: return
        self.outcome_records.append({
            "round_id": round_id,
            "simulation_id": simulation_id,
            "player_id": player_id,
            "hand_id": hand_id,
            "reward": reward,
            "type_of_win": outcome,
            "dealer_total": dealer_total,
            "dealer_hand": dealer_hand,
        })

    def decisions_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.decision_records)

    def rewards_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.outcome_records)

    def evs_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.ev_records)

    def save_decisions_csv(self, path: str) -> None:
        df = self.decisions_to_dataframe()
        df.to_csv(path, index=False)

    def save_rewards_csv(self, path: str) -> None:
        df = self.rewards_to_dataframe()
        df.to_csv(path, index=False)

    def save_evs_csv(self, path: str) -> None:
        df = self.evs_to_dataframe()
        df.to_csv(path, index=False)

    def merged_to_dataframe(self) -> pd.DataFrame:
        decisions_df = self.decisions_to_dataframe()
        rewards_df = self.rewards_to_dataframe()

        if decisions_df.empty:
            return decisions_df
        if rewards_df.empty:
            return decisions_df.copy()

        df = decisions_df.merge(
            rewards_df,
            on=["round_id", "player_id", "hand_id",  "simulation_id"],
            how="left",
        )

        cols = list(df.columns)

        if "action" in cols and "reward" in cols:
            cols.remove("reward")
            action_index = cols.index("dealer_upcard")
            cols.insert(action_index + 1, "reward")

        return df[cols]

    def save_merged_csv(self, path: str) -> None:
        df = self.merged_to_dataframe()
        df.to_csv(path, index=False)
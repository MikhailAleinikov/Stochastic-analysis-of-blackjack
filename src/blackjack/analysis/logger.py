import pandas as pd

class Logger:
    def __init__(self, focal_player_id: int):
        self.decision_records = []
        self.outcome_records = []
        self.focal_player_id = focal_player_id

    def log_decision(self, round_id, player_id, hand_id, decision_id, state, action):
        if player_id != self.focal_player_id: return
        self.decision_records.append({
            "round_id": round_id,
            "player_id": player_id,
            "hand_id": hand_id,
            "decision_index": decision_id,
            "action": action.value,
            "hand_repr": "".join(card.value.value for card in state.cards),
            "dealer_upcard": state.dealer_upcard.value.value,
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
            "dealer_upcard_group": 10 if state.dealer_upcard.value.value in ["T", "J", "Q", "K"]
                else 11 if state.dealer_upcard.value.value == "A"
                else int(state.dealer_upcard.value.value),
        })

    def log_reward(self, round_id: int, player_id: int, hand_id: int, reward: float):
        if player_id != self.focal_player_id: return
        self.outcome_records.append({
            "round_id": round_id,
            "player_id": player_id,
            "hand_id": hand_id,
            "reward": reward,
        })

    def decisions_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.decision_records)

    def rewards_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.outcome_records)

    def save_decisions_csv(self, path: str) -> None:
        df = self.decisions_to_dataframe()
        df.to_csv(path, index=False)

    def save_rewards_csv(self, path: str) -> None:
        df = self.rewards_to_dataframe()
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
            on=["round_id", "player_id", "hand_id"],
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
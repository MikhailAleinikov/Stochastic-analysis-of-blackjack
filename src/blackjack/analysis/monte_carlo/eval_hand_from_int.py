def evalHandFromInt(cards: list[int]):
    result = 0
    for card_value in sorted(cards):
        if card_value < 11:
            result += card_value
        else:
            if result + card_value <= 21:
                result += 11
            else:
                result += 1
    return result

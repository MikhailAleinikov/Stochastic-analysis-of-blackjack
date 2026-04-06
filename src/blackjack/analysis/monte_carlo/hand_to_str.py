def handToStr(hand: list[int]) -> str:
    return "".join(str(i) if str(i) in "23456789"
                   else "T" if i == 10 else "A" for i in hand)
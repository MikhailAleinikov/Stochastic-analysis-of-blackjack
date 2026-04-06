import random

def randomCard(card_count):
    total = sum(card_count.values())
    r = random.randint(1, total)

    cumulative = 0
    for value, count in card_count.items():
        cumulative += count
        if r <= cumulative:
            return value
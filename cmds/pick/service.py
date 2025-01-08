import random


def pick(items):
    lst = items.strip().split(",")
    picked = random.choice(lst)
    response = f"보기: {items}\n결과: {picked}"
    return response

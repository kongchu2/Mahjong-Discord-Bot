import random


def coin():
    n = random.randint(1, 6001)
    if n == 1:
        content = "동전이 섰다!"
    elif n % 2 == 0:
        content = "동전이 앞면으로 떨어졌습니다."
    else:
        content = "동전이 뒷면으로 떨어졌습니다."
    return content

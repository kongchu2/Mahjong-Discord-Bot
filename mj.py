from PIL import Image

import os
import random
from collections import defaultdict

card_list = [
    {
        "key": 'm',
        "max": 9
    },
    {
        "key": 's',
        "max": 9
    },
    {
        "key": 'p',
        "max": 9
    },
    {
        "key": 'z',
        "max": 7
    }
]
deck = [f"{cardkind['key']}{number}" for cardkind in card_list for number in range(1, cardkind["max"] + 1)] * 4

def get_random_cards(count=14, sort=True, alt_deck=None):
    _deck = deck.copy()
    if alt_deck:
        _deck = alt_deck
    picked = random.sample(_deck, count)
    if sort:
        picked = sorted(picked)
    return picked

def to_string_cards(cards):
    grouped_tiles = defaultdict(list)
    for tile in cards:
        grouped_tiles[tile[0]].append(tile[-1])
    result = ''.join(''.join(sorted(grouped_tiles[char])) + char for char in 'mpsz')
    return result

def sort_cards(cards):
    return list(sorted(cards))

def parse_cards(card_str):
    result = []
    current_tiles = ''
    
    # 주어진 문자열을 순회하면서 처리
    for char in card_str:
        if char.isdigit():
            current_tiles += char
        else:
            # 문자가 나타나면 앞의 숫자들과 결합해 리스트에 추가
            result.extend([char + num for num in current_tiles])
            current_tiles = ''  # 숫자 초기화
            
    return result

def pick_card(remove_cards: list):
    _deck = deck.copy()
    for card in remove_cards:
        _deck.remove(card)
    card = random.sample(_deck, 1)[0]
    return card

def create_image(cards=None):
    if not cards:
        cards = get_random_cards()
    filename = f'{to_string_cards(cards)}.jpg'
    image_files = [f"image/{card}.jpg" for card in cards]

    # 이미지 열기
    images = [Image.open(image) for image in image_files]

    # 각 이미지의 너비와 높이 가져오기
    widths, heights = zip(*(i.size for i in images))

    # 총 너비와 최대 높이 계산
    total_width = sum(widths)
    max_height = max(heights)

    # 새로운 이미지 생성
    new_image = Image.new('RGB', (total_width, max_height))

    # 이미지를 옆으로 붙이기
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return filename, new_image

def translater(msg:str):
    
    z = '동남서북백발중'
    b = '만삭통'
    a = 'msp'
    num = 0
    for char in msg:
        if char.isdigit():
           num = int(char)
        elif num == 0:
            num = z.index(char)+1
            return f'z{num}'
        else:
            idx = b.index(char)
            return f'{a[idx]}{num}'
        
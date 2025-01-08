import io
import random
from collections import defaultdict

import discord
from PIL import Image

from makoto import bot


@bot.tree.command(name="마작", description="이미지를 전송합니다.")
async def send_image(interaction: discord.Interaction):
    with io.BytesIO() as image_binary:
        filename, image = create_image()
        image.save(image_binary, "PNG")
        image_binary.seek(0)
        await interaction.response.send_message(
            file=discord.File(fp=image_binary, filename=filename)
        )


card_list = [
    {"key": "m", "max": 9},
    {"key": "s", "max": 9},
    {"key": "p", "max": 9},
    {"key": "z", "max": 7},
]
deck = [
    f"{cardkind['key']}{number}"
    for cardkind in card_list
    for number in range(1, cardkind["max"] + 1)
] * 4


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
    result = "".join("".join(sorted(grouped_tiles[char])) + char for char in "mpsz")
    return result


def sort_cards(cards):
    return list(sorted(cards))


def parse_cards(card_str):
    result = []
    current_tiles = ""

    # 주어진 문자열을 순회하면서 처리
    for char in card_str:
        if char.isdigit():
            current_tiles += char
        else:
            # 문자가 나타나면 앞의 숫자들과 결합해 리스트에 추가
            result.extend([char + num for num in current_tiles])
            current_tiles = ""  # 숫자 초기화

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
    filename = f"{to_string_cards(cards)}.jpg"
    image_files = [f"image/majak/{card}.jpg" for card in cards]

    # 이미지 열기
    images = [Image.open(image) for image in image_files]

    # 각 이미지의 너비와 높이 가져오기
    widths, heights = zip(*(i.size for i in images))

    # 총 너비와 최대 높이 계산
    total_width = sum(widths)
    max_height = max(heights)

    # 새로운 이미지 생성
    new_image = Image.new("RGB", (total_width, max_height))

    # 이미지를 옆으로 붙이기
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return filename, new_image


def translater(msg: str):
    z = "동남서북백발중"
    b = "만삭통"
    a = "msp"
    num = 0
    for char in msg:
        if char.isdigit():
            num = int(char)
        elif num == 0:
            num = z.index(char) + 1
            return f"z{num}"
        else:
            idx = b.index(char)
            return f"{a[idx]}{num}"


async def send_majak(
    message: discord.Message, referenced_message: discord.Message, failed_message=True
):
    if referenced_message.attachments:
        for attachment in referenced_message.attachments:
            if attachment.filename.endswith("jpg"):
                filename = attachment.filename.replace(".jpg", "")
                cards = parse_cards(filename)
                cards = sort_cards(cards)
                msg = message.content.lower().strip()
                remove_cards = []
                giri_history = []
                if referenced_message.content:
                    giri_history = parse_cards(referenced_message.content)
                if giri_history:
                    remove_cards = giri_history + cards
                else:
                    remove_cards = cards
                giri = msg
                remove_not_except(cards, giri)
                if len(cards) == 14:
                    if len(msg) == 2:
                        giri = f"{msg[-1]}{msg[0]}"
                        remove_not_except(cards, giri)
                if len(cards) == 14:
                    try:
                        giri = translater(msg)
                        remove_not_except(cards, giri)
                    except:
                        pass
                if len(cards) == 14:
                    if failed_message:
                        await message.reply("타패에 실패했습니다.")
                    return
                giri_history.append(giri)
                tsumo = pick_card(remove_cards)
                cards.append(tsumo)
                with io.BytesIO() as image_binary:
                    filename, image = create_image(cards)
                    image.save(image_binary, "PNG")
                    image_binary.seek(0)

                    await message.reply(
                        f"{to_string_cards(giri_history)}",
                        file=discord.File(fp=image_binary, filename=filename),
                    )


@bot.event
async def on_message(message: discord.Message):
    if (
        message.author == bot.user
        or message.is_system()
        or message.type == discord.MessageType.thread_starter_message
    ):
        return

    if message.reference:
        try:
            referenced_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            if referenced_message.author == bot.user:
                await send_majak(message, referenced_message, True)
                return
        except discord.errors.NotFound:
            pass

    if isinstance(message.channel, discord.Thread):
        thread = message.channel
        last_ref_message = None
        async for msg in thread.history(limit=10):  # 최근 10개의 메시지 가져오기
            if msg.author.id == bot.user.id and msg.attachments:
                last_ref_message = msg
                break
        if not last_ref_message:
            last_ref_message = await thread.parent.fetch_message(thread.id)
        if last_ref_message.author.id != bot.user.id:
            return
        await send_majak(message, last_ref_message, False)
        return


def remove_not_except(list, key):
    try:
        list.remove(key)
    except:
        pass

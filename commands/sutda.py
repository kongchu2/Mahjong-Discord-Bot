from makoto import bot
from discord import app_commands
import io
import discord


@bot.tree.command(name="섯다", description="섯다 뽑기")
@app_commands.describe(장수="몇장?")
@app_commands.choices(
    장수=[
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3),
    ]
)
async def send_sutda(interaction: discord.Interaction, 장수: int = 2):
    with io.BytesIO() as image_binary:
        image = pick_random_hwatu(장수)
        image.save(image_binary, "PNG")
        image_binary.seek(0)
        await interaction.response.send_message(
            file=discord.File(fp=image_binary, filename="sutda.png")
        )


import random
from PIL import Image


def pick_random_hwatu(count=2):
    # 이미지 파일 목록 생성
    image_files = [f"image/hwatu/{i}.png" for i in range(1, 21)]

    # 랜덤으로 두 개의 이미지 선택
    selected_images = random.sample(image_files, count)

    # 이미지 열기
    images = [Image.open(img) for img in selected_images]

    # 이미지 크기 설정 (가로로 붙이기 위해 크기 조정)
    total_width = sum(image.width for image in images)
    max_height = max(image.height for image in images)

    # 새로운 이미지 생성
    new_image = Image.new("RGB", (total_width, max_height))

    # 이미지를 붙이기
    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    # 결과 이미지 저장
    return new_image

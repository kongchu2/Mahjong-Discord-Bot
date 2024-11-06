import discord
from discord.ext import commands
from discord import app_commands

import os
from dotenv import load_dotenv
import requests
import io
import mj

import random

from sd import pick_random_hwatu


load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f'Logged in as {bot.user}')
    print(f'Bot is ready and logged in as {bot.user.name}')
    await bot.tree.sync()

def remove_not_except(list, key):
    try:
        list.remove(key)
    except:
        pass

@bot.event
async def on_message(message):
    if message.author == bot.user or message.is_system() or message.type == discord.MessageType.thread_starter_message:
        return

    if message.reference:
        try:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
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
            

async def send_majak(message: discord.Message, referenced_message: discord.Message, failed_message=True):
    if referenced_message.attachments:
        for attachment in referenced_message.attachments:
            if attachment.filename.endswith('jpg'):
                filename = attachment.filename.replace(".jpg", "")
                cards = mj.parse_cards(filename)
                cards = mj.sort_cards(cards)
                msg = message.content.lower().strip()
                remove_cards = []
                giri_history = []
                if referenced_message.content:
                    giri_history = mj.parse_cards(referenced_message.content)
                if giri_history:
                    remove_cards = giri_history + cards
                else:
                    remove_cards = cards
                giri = msg
                remove_not_except(cards, giri)
                if len(cards) == 14:
                    if len(msg) == 2:
                        giri = f'{msg[-1]}{msg[0]}'
                        remove_not_except(cards, giri)
                if len(cards) == 14:
                    try:
                        giri = mj.translater(msg)
                        remove_not_except(cards, giri)
                    except:
                        pass
                if len(cards) == 14:
                    if failed_message:
                        await message.reply("타패에 실패했습니다.")
                    return
                giri_history.append(giri)
                tsumo = mj.pick_card(remove_cards)
                cards.append(tsumo)
                with io.BytesIO() as image_binary:
                    filename, image = mj.create_image(cards)
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    
                    await message.reply(f"{mj.to_string_cards(giri_history)}", file=discord.File(fp=image_binary, filename=filename))

@bot.tree.command(name="마작", description="이미지를 전송합니다.")
async def send_image(interaction: discord.Interaction):
    with io.BytesIO() as image_binary:
        filename, image = mj.create_image()
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await interaction.response.send_message(file=discord.File(fp=image_binary, filename=filename))

@bot.tree.command(name="뽑기", description="척척박사")
@app_commands.describe(items=", 으로 구분해주세요.")
async def send_pick(interaction: discord.Interaction, items: str):
    try:
        lst = items.strip().split(',')
        picked = random.choice(lst)
        response = f"보기: {items}\n결과: {picked}"
    except:
        response = "뽑기에 실패했습니다."
    await interaction.response.send_message(content=response)

@bot.tree.command(name="섯다", description="섯다 뽑기")
@app_commands.describe(장수="몇장?")
@app_commands.choices(장수=[
    app_commands.Choice(name="2", value=2),
    app_commands.Choice(name="3", value=3),
])
async def send_sutda(interaction: discord.Interaction, 장수: int = 2):
    with io.BytesIO() as image_binary:
        image = pick_random_hwatu(장수)
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await interaction.response.send_message(file=discord.File(fp=image_binary, filename="sutda.png"))

@bot.tree.command(name="동전", description="동전이 설 수도?")

async def send_coin(interaction: discord.Interaction):
    if random.randint(1, 6000) == 1:
        content = "동전이 섰다!"
    elif random.randint(0, 1) == 1:
        content = "동전이 앞면으로 떨어졌습니다."
    else:
        content = "동전이 뒷면으로 떨어졌습니다."
        
    await interaction.response.send_message(content=content)

bot.run(TOKEN)
from makoto import bot
from discord import app_commands
import random
import discord

@bot.tree.command(name="뽑기", description="척척박사")
@app_commands.describe(items=", 으로 구분해주세요.")
async def send_pick(interaction: discord.Interaction, items: str):
    try:
        lst = items.strip().split(",")
        picked = random.choice(lst)
        response = f"보기: {items}\n결과: {picked}"
    except:
        response = "뽑기에 실패했습니다."
    await interaction.response.send_message(content=response)
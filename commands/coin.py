import discord
import random
from makoto import bot

@bot.tree.command(name="동전", description="동전이 설 수도?")
async def command(interaction: discord.Interaction) -> None:
    if random.randint(1, 6000) == 1:
        content = "동전이 섰다!"
    elif random.randint(0, 1) == 1:
        content = "동전이 앞면으로 떨어졌습니다."
    else:
        content = "동전이 뒷면으로 떨어졌습니다."
        
    await interaction.response.send_message(content=content)
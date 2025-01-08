import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"Logged in as {bot.user}")
    print(f"Bot is ready and logged in as {bot.user.name}")
    await bot.tree.sync()


import run

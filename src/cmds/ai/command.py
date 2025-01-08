import discord
from src.cmds.ai.service import prompt
from src.cmds.custom_command import CustomCommand
from src.discord.discord_bot import DiscordBot


class AICommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.event
        async def on_message(message: discord.Message):
            if bot.user and bot.user.mentioned_in(message):
                async with message.channel.typing():
                    await message.reply(prompt(message.content))

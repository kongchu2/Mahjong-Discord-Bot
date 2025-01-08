import discord

from cmds.coin.service import coin
from cmds.custom_command import CustomCommand
from discord_bot import DiscordBot


class CoinCommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.tree.command(name="동전", description="동전이 설 수도?")
        async def command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message(content=coin())

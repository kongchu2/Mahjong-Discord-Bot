import discord
from src.cmds.coin.service import coin
from src.cmds.custom_command import CustomCommand
from src.discord.discord_bot import DiscordBot


class CoinCommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.tree.command(name="동전", description="동전이 설 수도?")
        async def command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message(content=coin())

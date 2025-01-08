import discord
from discord import app_commands

from cmds.custom_command import CustomCommand
from cmds.pick.service import pick
from discord_bot import DiscordBot


class PickCommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.tree.command(name="뽑기", description="척척박사")
        @app_commands.describe(items=", 으로 구분해주세요.")
        async def command(interaction: discord.Interaction, items: str):
            response = pick(items)
            await interaction.response.send_message(content=response)

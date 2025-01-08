import io

import discord
from discord import app_commands
from src.cmds.custom_command import CustomCommand
from src.cmds.sutda.service import pick_random_hwatu
from src.discord.discord_bot import DiscordBot


class SutdaCommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.tree.command(name="섯다", description="섯다 뽑기")
        @app_commands.describe(장수="몇장?")
        @app_commands.choices(
            장수=[
                app_commands.Choice(name="2", value=2),
                app_commands.Choice(name="3", value=3),
            ]
        )
        async def command(interaction: discord.Interaction, 장수: int = 2):
            with io.BytesIO() as image_binary:
                image = pick_random_hwatu(장수)
                image.save(image_binary, "PNG")
                image_binary.seek(0)
                await interaction.response.send_message(
                    file=discord.File(fp=image_binary, filename="sutda.png")
                )

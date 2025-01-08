import discord
from discord.ext import commands
from src.cmds.custom_command import CustomCommand


class DiscordBot(commands.Bot):
    COMMAND_PREFIX = "/"

    def __init__(self, token: str, custom_commands: list[type[CustomCommand]]):
        self.token = token

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=DiscordBot.COMMAND_PREFIX, intents=intents)

        self.event(DiscordBot.make_on_ready(self))
        for command in custom_commands:
            command().init(self)

    @staticmethod
    def make_on_ready(_self):
        async def on_ready():
            await _self.wait_until_ready()
            if _self.user is None:
                import sys

                print("failed to load bot.user")
                sys.exit(1)
            print(f"Logged in as {_self.user}")
            print(f"Bot is ready and logged in as {_self.user.name}")
            await _self.tree.sync()

        return on_ready

    def run(self):
        super().run(self.token)

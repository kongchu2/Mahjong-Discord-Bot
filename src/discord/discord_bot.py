import discord
from discord.ext import commands
from src.cmds.custom_command import CustomCommand


class DiscordBot(commands.Bot):
    COMMAND_PREFIX = "/"

    def __init__(self, token: str, custom_commands: list[type[CustomCommand]]):
        self.token = token

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=DiscordBot.COMMAND_PREFIX,
            intents=intents,
            # /뽑기와 AI 답변은 사용자 입력을 그대로 내보내므로, 그 안의 @everyone·@here·역할·사용자 멘션이
            # 실제 알림으로 가지 않게 막습니다. 답장 대상에게 가는 알림은 그대로 둡니다.
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False, replied_user=True
            ),
        )

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

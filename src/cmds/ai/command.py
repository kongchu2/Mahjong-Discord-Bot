import contextlib

import discord
from src.cmds.ai.limiter import AIRateLimiter
from src.cmds.ai.service import clean_prompt, prompt
from src.cmds.custom_command import CustomCommand
from src.core.config import Config
from src.discord.discord_bot import DiscordBot


def should_answer(
    bot_user: discord.abc.User | None,
    message: discord.Message,
    allowed_guild_ids: frozenset[int],
) -> bool:
    if bot_user is None:
        return False
    # 봇이 쓴 메시지(자기 자신 포함)에는 답하지 않습니다. 답변에 멘션이 섞여 스스로를 다시 부르는 루프와
    # 다른 AI 봇과 서로 주고받는 루프를 막습니다.
    if message.author.bot or message.is_system():
        return False
    # @everyone/@here나 역할 멘션은 제외하고, 봇을 직접 멘션했을 때만 답합니다.
    if not any(user.id == bot_user.id for user in message.mentions):
        return False
    if allowed_guild_ids and (
        message.guild is None or message.guild.id not in allowed_guild_ids
    ):
        return False
    return True


class AICommand(CustomCommand):
    def init(self, bot: DiscordBot):
        limiter = AIRateLimiter(
            user_cooldown=Config.AI_USER_COOLDOWN_SECONDS,
            daily_limit=Config.AI_DAILY_LIMIT,
        )

        @bot.event
        async def on_message(message: discord.Message):
            if not should_answer(bot.user, message, Config.AI_ALLOWED_GUILD_IDS):
                return
            if limiter.acquire(message.author.id) is not None:
                # 한도에 걸린 요청마다 답장을 쓰면 그것도 도배가 되므로 반응만 남깁니다.
                with contextlib.suppress(discord.HTTPException):
                    await message.add_reaction("⏳")
                return
            assert bot.user is not None
            async with message.channel.typing():
                answer = await prompt(clean_prompt(message.content, bot.user.id))
            await message.reply(answer)

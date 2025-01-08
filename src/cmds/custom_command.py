from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.discord.discord_bot import DiscordBot


class CustomCommand(Protocol):
    def init(self, bot: "DiscordBot"): ...

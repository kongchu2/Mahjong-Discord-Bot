from src.cmds.coin.command import CoinCommand
from src.cmds.mahjong.command import MahjongCommand
from src.cmds.pick.command import PickCommand
from src.cmds.sutda.command import SutdaCommand
from src.core.config import Config
from src.discord.discord_bot import DiscordBot

Config.print_config()

if Config.DISCORD_BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN cannot be NULL")

bot = DiscordBot(
    Config.DISCORD_BOT_TOKEN, [CoinCommand, PickCommand, SutdaCommand, MahjongCommand]
)

bot.run()

from cmds.coin.command import CoinCommand
from cmds.mahjong.command import MahjongCommand
from cmds.pick.command import PickCommand
from cmds.sutda.command import SutdaCommand
from config import Config
from discord_bot import DiscordBot

Config.print_config()

if Config.DISCORD_BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN cannot be NULL")

bot = DiscordBot(
    Config.DISCORD_BOT_TOKEN, [CoinCommand, PickCommand, SutdaCommand, MahjongCommand]
)

bot.run()

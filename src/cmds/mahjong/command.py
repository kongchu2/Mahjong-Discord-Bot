import io

import discord
from src.cmds.custom_command import CustomCommand
from src.cmds.mahjong.service import (
    create_image,
    parse_cards,
    pick_card,
    sort_cards,
    to_string_cards,
    translater,
)
from src.cmds.sutda.service import remove_not_except
from src.discord.discord_bot import DiscordBot


class MahjongCommand(CustomCommand):
    def init(self, bot: DiscordBot):
        @bot.tree.command(name="마작", description="이미지를 전송합니다.")
        async def command(interaction: discord.Interaction):
            with io.BytesIO() as image_binary:
                filename, image = create_image()
                image.save(image_binary, "PNG")
                image_binary.seek(0)
                await interaction.response.send_message(
                    file=discord.File(fp=image_binary, filename=filename)
                )

        @bot.event
        async def on_message(message: discord.Message):
            await _on_message(bot, message)


async def _on_message(bot: DiscordBot, message: discord.Message):
    if (
        message.author == bot.user
        or message.is_system()
        or message.type == discord.MessageType.thread_starter_message
    ):
        return

    if message.reference:
        try:
            referenced_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            if referenced_message.author == bot.user:
                await send_majak(message, referenced_message, True)
                return
        except discord.errors.NotFound:
            pass

    if isinstance(message.channel, discord.Thread):
        thread = message.channel
        last_ref_message = None
        async for msg in thread.history(limit=10):  # 최근 10개의 메시지 가져오기
            if msg.author.id == bot.user.id and msg.attachments:
                last_ref_message = msg
                break
        if not last_ref_message:
            last_ref_message = await thread.parent.fetch_message(thread.id)
        if last_ref_message.author.id != bot.user.id:
            return
        await send_majak(message, last_ref_message, False)
        return


async def send_majak(
    message: discord.Message, referenced_message: discord.Message, failed_message=True
):
    if referenced_message.attachments:
        for attachment in referenced_message.attachments:
            if attachment.filename.endswith("jpg"):
                filename = attachment.filename.replace(".jpg", "")
                cards = parse_cards(filename)
                cards = sort_cards(cards)
                msg = message.content.lower().strip()
                remove_cards = []
                giri_history = []
                if referenced_message.content:
                    giri_history = parse_cards(referenced_message.content)
                if giri_history:
                    remove_cards = giri_history + cards
                else:
                    remove_cards = cards
                giri = msg
                remove_not_except(cards, giri)
                if len(cards) == 14:
                    if len(msg) == 2:
                        giri = f"{msg[-1]}{msg[0]}"
                        remove_not_except(cards, giri)
                if len(cards) == 14:
                    try:
                        giri = translater(msg)
                        remove_not_except(cards, giri)
                    except:
                        pass
                if len(cards) == 14:
                    if failed_message:
                        await message.reply("타패에 실패했습니다.")
                    return
                giri_history.append(giri)
                tsumo = pick_card(remove_cards)
                cards.append(tsumo)
                with io.BytesIO() as image_binary:
                    filename, image = create_image(cards)
                    image.save(image_binary, "PNG")
                    image_binary.seek(0)

                    await message.reply(
                        f"{to_string_cards(giri_history)}",
                        file=discord.File(fp=image_binary, filename=filename),
                    )

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import requests
import io
import mj


load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f'Logged in as {bot.user}')
    print(f'Bot is ready and logged in as {bot.user.name}')
    await bot.tree.sync()

def remove_not_except(list, key):
    try:
        list.remove(key)
    except:
        pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        if referenced_message.author == bot.user:
            if referenced_message.attachments:
                for attachment in referenced_message.attachments:
                    if attachment.filename.endswith('jpg'):
                        filename = attachment.filename.replace(".jpg", "")
                        cards = mj.parse_cards(filename)
                        cards = mj.sort_cards(cards)
                        msg = message.content.lower().strip()
                        try:
                            remove_cards = []
                            if referenced_message.content:
                                remove_cards = referenced_message.content.split(' ')
                            if remove_cards:
                                remove_cards = remove_cards + cards
                            else:
                                remove_cards = cards
                            giri = msg
                            remove_not_except(cards, giri)
                            if len(cards) == 14:
                                if len(msg) == 2:
                                    giri = f'{msg[-1]}{msg[0]}'
                                    remove_not_except(cards, giri)
                            if len(cards) == 14:
                                    giri = mj.translater(msg)
                                    remove_not_except(cards, giri)
                            if len(cards) == 14:
                                await message.reply("조패에 실패했습니다.")
                                return
                            tsumo = mj.pick_card(remove_cards)
                            cards.append(tsumo)
                            with io.BytesIO() as image_binary:
                                filename, image = mj.create_image(cards)
                                image.save(image_binary, 'PNG')
                                image_binary.seek(0)
                                
                                await message.reply(f"{referenced_message.content} {giri}", file=discord.File(fp=image_binary, filename=filename))
                        except Exception as e:
                            await message.reply("타패에 실패했습니다.")
                            raise e

@bot.tree.command(name="마작", description="이미지를 전송합니다.")
async def send_image(interaction: discord.Interaction):
    with io.BytesIO() as image_binary:
        filename, image = mj.create_image()
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await interaction.response.send_message(file=discord.File(fp=image_binary, filename=filename))


bot.run(TOKEN)
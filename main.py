import asyncio

import discord
from discord.ext import commands
import clashroyale
import brawlstats

from const import *

bot = commands.Bot(command_prefix='$', description='Бот для MGC', command_not_found='Команды {} не существует', command_has_no_subcommands='У команды {} нет подкоманд')

cr_client = clashroyale.official_api.Client(CR_TOKEN, is_async=False)
brawlstats_client = brawlstats.Client(BRAWL_STARS_TOKEN, is_async=True)

@bot.group()
async def clashroyale():
    pass

@clashroyale.command()
async def cards():
    c = cr_client.get_all_cards()
    await bot.say(c)

bot.run(TOKEN)
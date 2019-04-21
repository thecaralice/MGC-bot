import asyncio
import sys
import os
import random
from traceback import format_exception

import discord
from discord.ext import commands
import clashroyale
import brawlstats

from logger import *
from const import INITIAL_EXTENSIONS
import keep_alive

if sys.platform == 'win32':
    import dotenv
    dotenv.load_dotenv(r'.\.env')

bot = commands.Bot(
    command_prefix='$',
    description='Бот для MGC',
    owner_id=426757590022881290)

devs = [426757590022881290, 308628182213459989]

TOKEN = os.environ['BOT_TOKEN']

async def is_dev(ctx):
    return ctx.author.id in devs

@bot.command()
async def info(ctx):
    await ctx.send(await bot.application_info())


@bot.command()
@commands.check(is_dev)
async def kill(ctx):
    await bot.logout()

@bot.event
async def on_command_error(ctx, e):
    logger.exception('A command exception occured:', exc_info=(type(e), e, e.__traceback__))

for i in INITIAL_EXTENSIONS:
    bot.load_extension(i)

#keep_alive.keep_alive()
bot.run(TOKEN)
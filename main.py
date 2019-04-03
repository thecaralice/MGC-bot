import asyncio
import sys
import os
from traceback import format_exception

import discord
from discord.ext import commands
import clashroyale
import brawlstats

from logger import * 
import keep_alive

if sys.platform == 'win32':
    import dotenv
    dotenv.load_dotenv(r'.\.env')

bot = commands.Bot(
    command_prefix='$',
    description='Бот для MGC',
    command_not_found='Команды {} не существует',
    command_has_no_subcommands='У команды {} нет подкоманд',
    owner_id=426757590022881290)

devs = [426757590022881290, 308628182213459989]
#import cogs.brawlstars
INITIAL_EXTENSIONS = ['cogs.rainbow',
                      'cogs.downloader',
                      'cogs.brawlstars']

TOKEN = os.environ['BOT_TOKEN']


async def is_dev(ctx):
    return ctx.author.id in devs


@clashroyale.command(enabled=False)
async def cards(ctx):
    c = await cr_client.get_all_cards()
    await ctx.send(c)


@bot.command()
async def info(ctx):
    await ctx.send(await bot.application_info())


@bot.command()
@commands.check(is_dev)
async def kill(ctx):
    await bot.logout()

@bot.event
async def on_command_error(ctx, e):
    print(1)
    logger.exception('A command exception occured:', exc_info=(type(e), e, e.__traceback__))


for i in INITIAL_EXTENSIONS:
    bot.load_extension(i)

keep_alive.keep_alive()
bot.run(TOKEN)

import asyncio
import sys
import os
from traceback import format_exc

import discord
from discord.ext import commands
import clashroyale
import brawlstats

import keep_alive
from const import *

class Sender:
    def __init__(self, ctx):
        self.ctx = ctx
        self.loop = bot.loop

    def write(self, s):
        self.loop.run_until_complete(asyncio.wait([self.loop.create_task(self.ctx.send(s))]))
        sys.stdout.write(s)
        return len(s)

bot = commands.Bot(command_prefix='$', description='Бот для MGC', command_not_found='Команды {} не существует', command_has_no_subcommands='У команды {} нет подкоманд', owner_id=426757590022881290)

cr_client = clashroyale.official_api.Client(CR_TOKEN, is_async=True)
bs_client = brawlstats.Client(BRAWL_STARS_TOKEN, is_async=True)

devs = [426757590022881290,
          308628182213459989]

async def is_dev(ctx):
    return ctx.author.id in devs

@bot.group()
async def clashroyale(ctx):
    pass

@bot.group()
async def brawlstars(ctx):
    pass

@brawlstars.command(name='get-club')
async def get_club(ctx: commands.Context, tag: str):
    try:
        club = await bs_client.get_club(tag)
    except brawlstats.errors.NotFoundError:
        await ctx.send('Такого клана не существует!')
    else:
        embed = discord.Embed(title=club.name, description=club.description, color=0xffff00)
        embed.set_thumbnail(url=club.badge_url)
        embed.add_field(name='Тег', value=club.tag)
        embed.add_field(name='Статус', value=club.status)
        embed.add_field(name='Количество участников', value=club.members_count)
        embed.add_field(name='Участников онлайн', value=club.online_members)
        embed.add_field(name='Трофеи', value=club.trophies)
        embed.add_field(name='Трофеев для вступления', value=club.required_trophies)

        await ctx.send(embed=embed)

@clashroyale.command(enabled=False)
async def cards(ctx):
    c = await cr_client.get_all_cards()
    print(c)
    await ctx.send(c)

@bot.command()
async def info(ctx):
    await ctx.send(await bot.application_info())

@bot.command()
@commands.check(is_dev)
async def kill(ctx):
    await bot.logout()

@bot.command(name='eval')
@commands.check(is_dev)
async def eval_(ctx, code: str):
    global print
    print_ = print
    def print(*a, **kwa):
        if 'file' not in kwa:
            kwa['file'] = Sender(ctx)
            print_(*a, **kwa)
    try:
        await ctx.send(eval(code))
    except SyntaxError:
        exec(code)
        await ctx.send('Код выполнен!')
    print = print_

@bot.event
async def on_command_error(event, *args, **kwargs):
    await bot.get_user(426757590022881290).send(''.join(format_exc()))
    
for i in INITIAL_EXTENSIONS:
    bot.load_extension(i)

keep_alive.keep_alive()
bot.run(TOKEN)
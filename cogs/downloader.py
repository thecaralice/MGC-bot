import os
import asyncio
import aiohttp

import discord
from discord.ext import commands

class Downloader(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.group()
    async def cogs(self, ctx):
        pass

    @cogs.group()
    async def git(self, ctx):
        pass

    @cogs.group()
    async def gist(self, ctx):
        pass

    @git.command()
    async def install(self, ctx, link: str, overwrite: bool = False):
        filename = link.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            text = await (await session.get(link.replace('blob/', '', 1).replace('github.com', 'raw.github.com'))).text()
        os.chdir('cogs')
        while (os.path.exists(filename) and not overwrite) or (set(filename) & set('\\/:*?"<>|')):
            await ctx.send('File with this filename already exists, type a new filename' if (os.path.exists(filename) and not overwrite) else 'A filename cannot contain any of the following characters: `\` `/` `:` `*` `?` `"` `<` `>` `|`')
            m: discord.Message = await self.bot.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
            filename = m.clean_content
        with open(filename, 'w' if overwrite else 'x') as f:
            f.write(text)
        os.chdir('..')
        await ctx.send('Successfully installed ' + link.split('/')[-1][:-3])

    @gist.command(name='install')
    async def gist_install(self, ctx: commands.Context, username: str, filename: str, overwrite: bool = False):
        if not filename.endswith('.py'): filename += '.py'
        origin_filename = filename
        os.chdir('cogs')
        ex = os.path.exists(filename) and not overwrite
        while (os.path.exists(filename) and not overwrite) or (set(filename) & set('\\/:*?"<>|')):
            await ctx.send('File with this filename already exists, type a new filename' if (os.path.exists(filename) and not overwrite) else 'A filename cannot contain any of the following characters: `\` `/` `:` `*` `?` `"` `<` `>` `|`')
            m: discord.Message = await self.bot.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
            filename = m.clean_content
            if not filename.endswith('.py'): filename += '.py'
        if ex: os.rename(origin_filename, origin_filename + '.tmp')
        with os.popen(f'getgist {username} {origin_filename} -y') as f:
            out = f.read()
            #await ctx.send(out)
            await ctx.send('```' + out.replace('Done!', 'Successfully installed ' + origin_filename[:-3]) + '```')
        if ex:
            os.rename(origin_filename, filename)
            os.rename(origin_filename + '.tmp', origin_filename)
        os.chdir('..')

    @cogs.command()
    async def uninstall(self, ctx, cog: str):
        if not cog.endswith('.py'): cog += '.py'
        try:
            os.remove('cogs/' + cog)
        except FileNotFoundError:
            await ctx.send('This cog is not installed')
        else:
            await ctx.send('Successfully uninstalled ' + cog[:-3])

    @cogs.command()
    async def list(self, ctx):
        for path, dname, fname in os.walk('cogs'):
            if path.endswith('__pycache__'): continue
            for i in fname:
                await ctx.send(path + '\\' + i[:-3] + '|' + dname)

def setup(bot):
    bot.add_cog(Downloader(bot))

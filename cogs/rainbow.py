import asyncio
from colorsys import hls_to_rgb

import discord
from discord.ext import commands

class Rainbow(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roles = set()
        self.on_low_role = 'Sorry, your role isn\'t high enough'
        self.speed = 7
        self.hue = 0
        self.bot.loop.create_task(self.loop())
    
    async def loop(self):
        print('Task created!')
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for i in self.roles:
                print(i.name, i.colour)
                self.hue = (self.hue + self.speed) % 360
                rgb = [int(x * 255) for x in hls_to_rgb(self.hue / 360, 0.5, 1)]
                clr = discord.Colour(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
                await i.edit(colour=clr, reason='Automatic rainbow color change')
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def start(self, ctx: commands.Context, role: discord.Role):
        if ctx.author.top_role > role:
            m: discord.Message = await ctx.send('Starting...')
            self.roles.add(role)
            await m.edit(content='Started!')
        else:
            await ctx.send(self.on_low_role)
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def stop(self, ctx: commands.Context, role: discord.Role):
        if ctx.author.top_role > role:
            m: discord.Message = await ctx.send('Stopping...')
            try:
                self.roles.remove(role)
            except KeyError:
                await m.edit('This role doesn\'t rainbowin\'')
            else:
                await m.edit('Started!')
        else:
            await ctx.send(self.on_low_role)

def setup(bot: commands.Bot):
    bot.add_cog(Rainbow(bot))
    
# There's no such text in gist
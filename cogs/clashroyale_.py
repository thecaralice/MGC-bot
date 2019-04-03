import os
import asyncio
import discord
from discord.ext import commands
import clashroyale

class BrawlStars(commands.Cog):
    def __init__(self, bot):
        self.client = clashroyale.Client(os.environ['CR_TOKEN'], is_async=True)
    
    @commands.group()
    async def clashroyale(self, ctx):
        pass
    
    @clashroyale.command(enabled=False)
    async def cards(ctx):
        await ctx.send(await self.client.get_all_cards())

#----------------------------------------------------------------------
def setup(bot):
    bot.add_cog(BrawlStars(bot))

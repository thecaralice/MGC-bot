import os
import asyncio
import discord
from discord.ext import commands
import brawlstats

class BrawlStars(commands.Cog):
    def __init__(self, bot):
        self.client = brawlstats.Client(os.environ['BRAWL_STARS_TOKEN'], is_async=True)
    
    @commands.group()
    async def brawlstars(self, ctx):
        pass
    
    @brawlstars.group(invoke_without_command=True, aliases=['bs', 'brawl'])
    async def club(self, ctx):
        return await ctx.send('Наш клан: https://link.brawlstars.com/invite/band/ru?tag=LUPURPJ&token=wkj7f67b')
    
    @club.command(name='get')
    async def get_club(self, ctx, tag: str):
        try:
            club = await self.client.get_club(tag)
        except brawlstats.errors.NotFoundError:
            await ctx.send('Такого клана не существует!')
        else:
            embed = discord.Embed(
                title=club.name, description=club.description, color=0xffff00)
            embed.set_thumbnail(url=club.badge_url)
            embed.add_field(name='Тег', value=club.tag)
            embed.add_field(name='Статус', value=club.status)
            embed.add_field(name='Количество участников', value=club.members_count)
            embed.add_field(name='Участников онлайн', value=club.online_members)
            embed.add_field(name='Трофеи', value=club.trophies)
            embed.add_field(
                name='Трофеев для вступления', value=club.required_trophies)
    
            await ctx.send(embed=embed)

#----------------------------------------------------------------------
def setup(bot):
    bot.add_cog(BrawlStars(bot))
    
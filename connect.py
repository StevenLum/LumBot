import discord
from discord.ext import commands

from modules.time import Time
from modules.postgresql import DEFAULT_VALUES, SELECT
from LumBot import CHIPS

class SQLTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def default_db(self, ctx):
        user = await self.bot.pg_con.fetchrow(DEFAULT_VALUES, ctx.message.author.id, ctx.message.guild.id)

        
        print(f"\n...DB update completed. Users were added to DB")

def setup(bot):
    bot.add_cog(SQLTest(bot))


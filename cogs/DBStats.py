import discord
from discord.ext import commands
from modules.postgresql import SELECT

class DBStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_stats(self, ctx):
        user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        await ctx.send(f'```Level: {user["level"]}\nExp: {user["exp"]}\nBalance: {user["coins"]}```')

    @commands.command(aliases=['balance'])
    async def bal(self, ctx):
        user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        await ctx.send(f'```Balance: {user["coins"]}```')


    @commands.command()
    async def profile(self, ctx):
        user = ctx.guild.get_member(ctx.author.id)
        pfp = user.avatar_url
        pfp = str(pfp)
        await ctx.send(pfp)
        #user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET background = $1
            WHERE user_id = $2 AND guild_id = $3
            """,
            pfp,
            ctx.author.id,
            ctx.guild.id
        )


def setup(bot):
    bot.add_cog(DBStats(bot))
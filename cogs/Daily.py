import discord
from discord.ext import commands
from discord.utils import get

from modules.time import Time
from modules.postgresql import SELECT
from LumBot import CHIPS


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DAILY_INTERVAL = 12*60*60
        self.DAILY_REWARD = 50
        self.time = Time()

    @commands.command(help='gives 50 coins')
    async def daily(self, ctx):
        user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        dif = self.time.subtract(user["daily"])

        if dif.total_seconds() >= self.DAILY_INTERVAL:
            daily = f'You got 50 {CHIPS}! Come back again in 12 hours.\nYou have {user["coins"]+self.DAILY_REWARD}{CHIPS}'
            await self.bot.pg_con.execute(
                """
                UPDATE users
                SET daily = $3, coins = $4
                WHERE user_id = $1 AND guild_id = $2
                """,
                ctx.author.id,
                ctx.guild.id,
                self.time.get_datetime(),
                user['coins']+self.DAILY_REWARD
            )
        else:
            daily = self.time.delta(dif)
            daily = f"Come back in {daily} for your reward"

        await ctx.channel.send(daily)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mod_money(self, ctx, amount, disc, *, name):
        user_id = await self.get_user_id(ctx, name, disc)
        user = await self.bot.pg_con.fetchrow(SELECT, user_id, ctx.guild.id)
        #new_user_amount = user['coins']+amount
        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET coins = $3
            WHERE user_id = $1 AND guild_id = $2
            """,
            user_id,
            ctx.guild.id,
            user['coins']+int(amount)
        )
        await ctx.send(f'Added {amount}{CHIPS} to {name}\'s balance.\n{name} has {user["coins"]+int(amount)}{CHIPS}.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mod_money2(self, ctx, amount, member: discord.Member = None):
        member = member or ctx.author
        print(member)
        user = await self.bot.pg_con.fetchrow(SELECT, member.id, ctx.guild.id)
        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET coins = $3
            WHERE user_id = $1 AND guild_id = $2
            """,
            member.id,
            ctx.guild.id,
            user['coins']+int(amount)
        )
        await ctx.send(f'Added {amount}{CHIPS} to {member.name}\'s balance.\n{member.name} has {user["coins"]+int(amount)}{CHIPS}.')

    async def get_user_id(self, ctx, name, disc):
        for member in ctx.guild.members:
            if member.name == name and member.discriminator == disc:
                return member.id
            if member.nick == name and member.discriminator == disc:
                return member.id


def setup(bot):
    bot.add_cog(Daily(bot))

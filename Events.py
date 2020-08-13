import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member == self.bot.user or member.bot:
            return

        user = await self.bot.pg_con.fetchrow(SELECT, member.id, member.guild.id)

        if not user:
            await self.bot.pg_con.fetchrow(DEFAULT_VALUES, member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            if not (member == self.bot.user or member.bot):
                user = await self.bot.pg_con.fetchrow(SELECT, member.id, guild.id)

                if not user:
                    await self.bot.pg_con.fetchrow(DEFAULT_VALUES, member.id, guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
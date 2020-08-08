import discord
from discord.ext import commands

from modules.postgresql import DEFAULT_VALUES, SELECT


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update_db(self, ctx):
        print(f"\nDB update started...\nServers: {len(self.bot.guilds)}")
        await ctx.channel.send(f"DB update started...\nServers: {len(self.bot.guilds)}")
        users = 0

        for guild in self.bot.guilds:
            for member in guild.members:
                if not (member == self.bot.user or member.bot):
                    user = await self.bot.pg_con.fetchrow(SELECT, member.id, guild.id)

                    if not user:
                        await self.bot.pg_con.fetchrow(
                            DEFAULT_VALUES, member.id, guild.id
                        )
                        users += 1

        print(f"\n...DB update completed\n{users} users were added to DB")
        await ctx.channel.send(
            f"...DB update completed\n{users} users were added to DB"
        )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx):
        await ctx.channel.send(f"Servers: {len(self.bot.guilds)}")


def setup(bot):
    bot.add_cog(Admin(bot))
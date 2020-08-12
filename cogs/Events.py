import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            #if not member.bot:
            print(member)


def setup(bot):
    bot.add_cog(Events(bot))
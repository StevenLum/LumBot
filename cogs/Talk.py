import discord
from discord.ext import commands

class Talk(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def authID(self, ctx):
        await ctx.send(ctx.message.author.id)

    @commands.command()
    async def guildID(self, ctx):
        await ctx.send(ctx.message.guild.id)

    


def setup(bot):
    bot.add_cog(Talk(bot))
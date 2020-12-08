import discord
from discord.ext import commands
from multiprocessing import Process
import queue
from discord.utils import get
from cogs.Emote import Emote
# I dont know how to do threads.


class Talk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='sends your user ID')
    async def authID(self, ctx):
        await ctx.send(ctx.message.author.id)

    @commands.command(help='sends the server ID')
    async def guildID(self, ctx):
        await ctx.send(ctx.message.guild.id)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def talk(self, ctx, guildID, channelName):

        def findChannel(guildID, channelName):
            for guild in self.bot.guilds:
                if guild.id == int(guildID):
                    for channel in guild.text_channels:
                        if str(channel) == channelName:
                            return (guild, channel)
            return (-1, -1)

        channel = findChannel(guildID, channelName)
        if -1 in channel:
            await ctx.send("Can't find channel")
            return
        await ctx.send(f"Talking in {channel[0].name}: {channel[1]}")

        while True:
            inp = await input()
            if inp == '.exit' or inp == '.e' or inp == '.quit' or inp == '.q':
                break
            if inp.split()[0] == '.nitro':
                inp = inp[6:]
                inp = Emote.emote(ctx, inp)
                if inp == '':
                    continue
            await channel[1].send(inp)

    @ commands.command()
    async def mock(self, ctx, member: discord.Member = None):

        def check(m):
            return m.author == member

        member = member or ctx.author
        await self.bot.wait_for("message", check=check)
        # if ctx.message.author == member:
        await ctx.send(ctx.message.content)
        # print(ctx.message.author, member)

    @ commands.command(hidden=True)
    @ commands.is_owner()
    async def getServers(self, ctx):
        guilds = [guild for guild in self.bot.guilds]
        text_channels = []
        for guild in guilds:
            await ctx.send(str(guild.id) + ' ' + guild.name + '\n')
            text_channels = []
            for i in range(len(guild.text_channels)):
                text_channels.append(guild.text_channels[i].name)
            await ctx.send(text_channels)


def setup(bot):
    bot.add_cog(Talk(bot))

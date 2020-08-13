import discord
from discord.ext import commands

class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [emoji for guild in self.bot.guilds for emoji in guild.emojis]
        self.emojinames = [emoji.name for emoji in self.emojis]
    @commands.command(help='shows every emote this bot knows')
    async def nitrolist(self, ctx):  
        await ctx.send(" ".join(map(str, self.emojis)))
        '''
        self.emojii = []
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                #await ctx.send(emoji)
                self.emojis += [emoji]
        await ctx.send(" ".join(map(str, self.emojis)))
        '''


    @commands.command(help='a worse version of jasonbots !nitro')
    async def nitro(self, ctx, *, emojiname):
        #for emoji in ctx.guild.emojis:
        #    print(emoji)
        for emojiname in emojiname.split():
            if emojiname in self.emojinames:
                index = self.emojinames.index(emojiname)
                await ctx.send(self.emojis[index])
            else:
                await ctx.send(':poop:')


def setup(bot):
    bot.add_cog(Emote(bot))
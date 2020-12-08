import discord
from discord.ext import commands


class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [
            emoji for guild in self.bot.guilds for emoji in guild.emojis]
        self.emojinames = [emoji.name for emoji in self.emojis]

    @commands.command(help='shows every emote this bot knows')
    async def nitrolist(self, ctx):
        # await ctx.send(" ".join(map(str, self.emojis)))
        send_list = []
        for i in range(len(self.emojis)):
            if i % 16 == 0 and i != 0:
                await ctx.send("".join(map(str, send_list)))
                send_list = []
            send_list += [self.emojis[i]]
        await ctx.send("".join(map(str, send_list)))

        '''
        self.emojii = []
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                #await ctx.send(emoji)
                self.emojis += [emoji]
        await ctx.send(" ".join(map(str, self.emojis)))
        '''

    def emote(self, emoteName):
        emoteList = []
        for emote in emoteName.split():
            emoji = discord.utils.get(self.bot.emojis, name=emote)
            if emoji == None:
                continue
            emoteList.append(emoji)
        return ''.join(map(str, emoteList))

    @commands.command(help='a worse version of jasonbots !nitro')
    async def nitro(self, ctx, *, emoteName):
        emotes = self.emote(emoteName)
        await ctx.send(emotes)


def setup(bot):
    bot.add_cog(Emote(bot))

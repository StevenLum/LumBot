import discord
from discord.ext import commands
import random

class Fortune(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['eightball', '8ball'], name='8ball|eightball', help='magic 8 ball')
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
            
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @_8ball.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Usage: [.8ball | eightball] [question]')


def setup(bot):
    bot.add_cog(Fortune(bot))
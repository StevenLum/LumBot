import discord
from discord.ext import commands
from LumBot import COMMAND_PREFIX
import random
import asyncio

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='[number of dice] [number of sides]')
    async def roll(self, ctx, num_dice=1, num_sides=6):
        dice = []
        for i in range(int(num_dice)):
            number = random.randint(1, int(num_sides))
            dice += [number]
        await ctx.send(f'{" ".join(map(str, dice))}')

    @commands.command()
    async def guess(self, ctx):
        await ctx.send("Guess a number between 1 and 10.\nEnter your guess by doing 'guess [number]'")
        number = random.randint(1, 10)
        def check(m):
            #print(m.content)
            return m.content.startswith('guess')
        try:
            guess = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long it was {}.'.format(number))
        return await ctx.send(f'The answer was {number}, your guess was {guess.content.split(" ")[1]}')

    #@commands.Cog.listener()
    #async def on_message(self, message):
    #    if message.author.id != 740554991189885019:
    #        if message.content.startswith(f"{COMMAND_PREFIX}guess"):
    #            await message.channel.send('ddwadwa')
               
def setup(bot):
    bot.add_cog(Roll(bot))
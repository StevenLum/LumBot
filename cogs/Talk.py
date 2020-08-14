import discord
from discord.ext import commands
import threading
import queue

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
    async def talk(self, ctx):
        inputQueue = queue.Queue()
        EXIT_COMMAND = 'exit'
        def read_kbd_input(inputQueue):
            print('Ready for input: ')
            while True:
                input_str = input()
                inputQueue.put(input_str)
        inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue), daemon=True)
        inputThread.start()
        while True:
            if (inputQueue.qsize() > 0):
                input_str = inputQueue.get()
                if input_str == EXIT_COMMAND:
                    break
                await ctx.send(input_str)

        

    


def setup(bot):
    bot.add_cog(Talk(bot))
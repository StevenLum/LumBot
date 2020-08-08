import discord
from discord.ext import commands
import random

class Farkle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.players = []
    
    @commands.command()
    async def player(self, ctx):
        self.players = ctx.message
        await ctx.send(self.players)
        
    #@client.event
    #async def on_message(self, message):
    #    return message

                


    

def setup(client):
    client.add_cog(Farkle(client))
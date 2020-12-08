import discord
from discord.ext import commands
import random

class Farkle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.players = []
        self.dice_list = [':dice1:741866832373350481', ':dice2:741866727700168734', ':dice3:741866734201339934', ':dice4:741866740853768224', ':dice5:741866748235743293', ':dice6:741866765159628890']

    
    @commands.command()
    async def player(self, ctx):
        self.players = ctx.message
        await ctx.send(self.players)
    
    @commands.command()
    async def farkle(self, ctx):
        self.embed = discord.Embed()
        self.embed.set_footer(text="REACT ME")
        self.msg = await ctx.send(embed=self.embed)
        #await self.msg.add_reaction(':dice1:741866832373350481')

    #@commands.Cog.listener()
    #async def on_reaction_add(self, ctx, reaction, user):
    #    for emoji in ctx.guild.emojis:
    #        print(emoji)



    

def setup(client):
    client.add_cog(Farkle(client))
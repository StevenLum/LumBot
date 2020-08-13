import discord
from discord.ext import commands
from discord.utils import get
import urllib.request
import json
from datetime import datetime
#import requests


class Internet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        #r = requests.get("https://meme-api.herokuapp.com/gimme")
        data = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme").read()
        data = data.decode('utf-8')
        data = json.loads(data)     

        embed = (discord.Embed(title=f":speech_balloon: r/{data['subreddit']} :", color=ctx.author.color, description=f"Meme: {data['postLink']}")
                .set_image(url=data['url']))
                #.add_field(description=data['postLink']))
        await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, city='Auckland'):
        data = urllib.request.urlopen(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID=fb9df86d9c484eba8a69269cfb0beac9").read()
        data = data.decode('utf-8')
        data = json.loads(data)

        #await ctx.send(data['coord']['lon'])

        weather = data['weather'][0]
        temps = data['main']
        wind = data['wind']
        sunrise = data['sys']['sunrise'] + data['timezone']
        sunrise = datetime.utcfromtimestamp(sunrise).strftime('%H:%M:%S')  
        sunset = data['sys']['sunset'] + data['timezone']
        sunset = datetime.utcfromtimestamp(sunset).strftime('%H:%M:%S')
        #await ctx.send(f"{wind['speed']}\n{wind['deg']}")
        #await ctx.send(f"{weather[0]['main']}")

        embed = (discord.Embed(title=f"Weather for {city} in {data['sys']['country']} | {weather['description'].title()}")
                .add_field(name='Temperature', value=f"Real: {temps['temp']}\nFeels like: {temps['feels_like']}")
                #.add_field(name='Weather', value=f"{weather['description'].title()}")
                .add_field(name='Sunrise and Sunset', value=f"Sunrise: {sunrise}\nSunset: {sunset}")
                #.add_field(name='Coordinates',value=f"Longitude: {data['coord']['lon']}\nLatitide: {data['coord']['lat']}")
                #.set_thumbnail(url='')
                )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Internet(bot))
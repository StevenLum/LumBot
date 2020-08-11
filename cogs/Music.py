import discord
from discord.ext import commands
import youtube_dl
import nacl
import asyncio

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = {}
        self.players = {}
        self.queues = {}
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        self.voice_client[channel] = await channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        channel = ctx.author.voice.channel
        #await self.voice_client[channel].disconnect()
        #del self.voice_client[channel]
        #await ctx.send(self.bot.voice_clients)
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.message.guild:
                del self.voice_client[channel]
                await vc.disconnect()

    @commands.command()
    async def yt(self, ctx, *, url):
        if ctx.author.voice:
            try:
                self.voice_client[ctx.author.voice.channel]
            except:
                await self.join(ctx)
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            self.players[ctx.message.guild.id] = player
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send('Not connected to a voice channel.')
        ctx.voice_client.source.volume = volume / 100

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def play(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await self.leave(ctx)

    @commands.command()
    async def show(self, ctx):
        await ctx.send(f'{self.voice_client}\n{self.players}')
    
    
    '''
    @commands.command()
    async def queue(self, ctx, url):

        def check_queues(id):
            if self.queues[id] != []:
                player = self.queues[id].pop(0)
                self.players[id] = player
                player.start()
    
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        channel = ctx.author.voice.channel
        guild = ctx.message.guild
        if guild.id in self.queues:
            self.queues[guild.id].append(player)
        else:
            self.queues[guild.id] = [player]
        ctx.voice_client.play(player, after=lambda: check_queues(guild.id))
        await ctx.send(f'{player.title} queued.')
    '''


def setup(bot):
    bot.add_cog(Music(bot))

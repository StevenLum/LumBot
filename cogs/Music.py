import discord
from discord.ext import commands
import youtube_dl
import nacl
import asyncio
from discord.utils import get

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
    def __init__(self, source, *, data, volume=0.3):
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

    @commands.command(hidden=True)
    async def yt2(self, ctx, *, url):
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

    def play_next(self, ctx):
        channel = ctx.author.voice.channel
        self.voice_client[channel]
        if self.queues[ctx.guild] != []:
            player = self.queues[ctx.guild].pop(0)
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))

            
    @commands.command()
    async def yt(self, ctx, *, url):
        channel = ctx.author.voice.channel
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

        if ctx.author.voice:
            try:
                self.voice_client[channel]
            except:
                await self.join(ctx)
        if not self.voice_client[channel].is_playing():
            self.queues[ctx.guild] = [player]
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
        else:
            self.queues[ctx.guild].append(player)
    


    @commands.command(breif='[number]')
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send('Not connected to a voice channel.')
        ctx.voice_client.source.volume = volume / 100

    @commands.command(help='pauses the song')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            if voice.is_playing(): voice.pause()
            else: voice.resume()

    @commands.command(help='leaves the VC and drops the playlist')
    async def stop(self, ctx):
        ctx.voice_client.stop()
        self.queues[ctx.guild] = []
        await self.leave(ctx)

    @commands.command(help='skips to the next song in the playlist')
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        self.play_next(ctx)

    @commands.command(help='show the playlist')
    async def playlist(self, ctx):
        c=1
        playlist = []
        if self.queues[ctx.guild] != []:
            for song in self.queues[ctx.guild]:
                playlist.append(f'{c}. {song.title}')
                c+=1
            await ctx.send(" \n".join(map(str, playlist)))
        else: await ctx.send("Playlist is empty")
    
    @commands.command(help='removes the song in the playlist')
    async def remove(self, ctx, *, number: int):
        del self.queues[ctx.guild][number]
    
    @commands.command(hidden=True)
    async def show(self, ctx):
        await ctx.send(self.queues[ctx.guild])
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

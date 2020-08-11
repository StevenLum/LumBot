import discord
#import random
import os
from discord.ext import commands
from settings import load_bot_token, load_db_password, load_db_host, load_db_port
import asyncpg

COMMAND_PREFIX = '.'
DESCRIPTION = 'A Bot for discord.'

CHIPS = "\U0001F4B0"
TICKETS = "\U0001F3AB"


'''===========================================================
config_file = 'LumBot_cfg.ini'
try:
    with open(config_file, 'r') as f:
        token = f.read()
except (OSError, IOError, FileNotFoundError):
        print('Bot config file \'{}\' not found.'.format(filename))
except ValueError:
    print('Invalid config file.')
==========================================================='''
#client = commands.Bot(command_prefix = COMMAND_PREFIX)

INITIAL_EXTENSIONS = [
    "cogs.Hello",
    "cogs.8ball",
    "cogs.Farkle",
    "cogs.Talk",
    "cogs.Admin",
    "cogs.Daily",
    "cogs.DBStats",
    "cogs.Roll",
    "cogs.Music"
]


class LumBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            description=DESCRIPTION,
            pm_help=None,
            fetch_offline_members=False,
            heartbeat_timeout=150.0
        )

        self.token = load_bot_token()

        for extension in INITIAL_EXTENSIONS:
            self.load_extension(extension)
        '''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
        '''



    async def on_ready(self):
        print('Bot is ready.')
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name='.help')   
        )

    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(
            host=load_db_host(),
            port=load_db_port(),
            user="postgres",
            database="Discord",
            password=load_db_password(),
        )

    

    def run(self):
        super().run(self.token)

    
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')
'''

client = LumBot()

'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command doesnt exist. Type ".help" for commands.')
    elif isinstance(error, commands.NotOwner):
        await ctx.send('You do not own this bot.\nSit down.')
    else:
        raise error
'''

@client.command(hidden=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, *args):
    for extension in args:
        try:
            client.load_extension(f'cogs.{extension}')
            print(f'Loaded {extension}.')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{extension} is already loaded.')
        except commands.ExtensionNotFound:
            await ctx.send(f'{extension} not found.')

@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, *args):
    for extension in args:
        try:
            client.unload_extension(f'cogs.{extension}')
            print(f'Unloaded {extension}.')
        except commands.ExtensionNotFound:
            await ctx.send(f'{extension} not found.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{extension} is not loaded.')
    
@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, *args):
    for extension in args:
        try:
            client.reload_extension(f'cogs.{extension}')
            print(f'Reloaded {extension}.')
        except commands.ExtensionNotFound:
            await ctx.send(f'{extension} not found.')
        except commands.ExtensionNotLoaded:
            client.load_extension(f'cogs.{extension}')
            print(f'Loaded {extension}.')
        



@client.command(hidden=True)
@commands.is_owner()
async def find_loaded(ctx):
    loaded = []
    not_loaded = []
    for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    client.load_extension(f'cogs.{filename[:-3]}')
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    not_loaded += [str(filename)]
                    #await ctx.send(f'{filename} not loaded')
                except commands.ExtensionAlreadyLoaded:
                    #await ctx.send(f'{filename} is loaded.')
                    loaded += [str(filename)]
                #except:
                    #await ctx.send(f'{filename}')
                    #await ctx.send('Extension not found.')
    for ext in loaded:
        await ctx.send(f'{ext} is loaded.')
    for ext in not_loaded:
        await ctx.send(f'{ext} is not loaded')
    #await ctx.send(f'{loaded}\n {not_loaded}')
    await ctx.send("No more extensions found.")

@client.command(aliases=['quit', 'close', 'q'], hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await client.close()
    print('Bot closed.')

@client.command(hidden=True)
@commands.is_owner()
async def restart(ctx):
    await client.close()
    os.startfile("D:\Desktop\Bot\LumBot.bat")



@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.loop.run_until_complete(client.create_db_pool())
client.run()


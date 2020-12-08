import discord
from discord.ext import commands
from LumBot import COMMAND_PREFIX, CHIPS
from modules.postgresql import SELECT, COINS
import random
import asyncio
import threading


class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        thread = threading.Thread(target=self.slots)
        thread.start()

        self.symbols_dict = {
            "\U0001F34C": [0.5, 1.5, 3.5],  # :banana:
            "\U0001F347": [0.5, 1.5, 4.0],  # :grapes:
            "\U0001F352": [0.5, 2.0, 5.0],  # :cherries:
            "\U0001F34B": [0.5, 2.5, 6.5],  # :lemon:
            "\U0001F349": [1.5, 5.0, 20.0],  # :watermelon:
            "\U0001F95D": [2.0, 8.0, 35.0],  # :kiwi:
            "\U0001F353": [3.0, 15.0, 60.0],  # :strawberry:
            "\U0001F351": [4.0, 25.0, 80.0],  # :peach:
            "\U0001F48E": [0],  # wild     # :gem:
        }

        self.symbols = [symbol for symbol in self.symbols_dict]
        self.SPIN = "\U0001F1F8"

    @commands.command(aliases=['slot'], help='Casino slots')
    async def slots(self, ctx, bet=None):
        if not bet:
            return await ctx.send(f":x: You must enter your bet! Usage: {COMMAND_PREFIX}slots [bet]")

        if not bet.isdigit():
            return await ctx.send(f":x: A bet must be a number! Usage: {COMMAND_PREFIX}slots [bet]")

        self.bet = int(bet)

        self.author_id = ctx.author.id
        self.guild_id = ctx.guild.id

        self.user = await self.bot.pg_con.fetchrow(SELECT, self.author_id, self.guild_id)

        if self.bet > self.user['coins']:
            return await ctx.send(f":x: You don't have enough chips! Your balance is {self.user['coins']}{CHIPS}\nEnter a different amount or use {COMMAND_PREFIX}daily for more coins")

        self.highlighted = []
        self.lines = self.generate_line() + self.generate_line() + self.generate_line()
        self.embed = await self.update_ui(ctx, True)
        self.msg = await ctx.send(embed=self.embed)
        await self.msg.add_reaction(self.SPIN)
        await self.msg.edit(embed=self.embed)

        def check_reaction(reaction, user):
            return (
                str(reaction.message) == str(self.msg)
                and user == ctx.author
                and str(reaction.emoji) == self.SPIN
            )

        while True:
            try:
                reaction = await self.bot.wait_for("reaction_add", check=check_reaction, timeout=60.0)
            except asyncio.TimeoutError:
                await self.msg.delete()
                return

            if reaction:
                if self.bet > self.user['coins']:
                    return await ctx.send(f":x: Not enough chips. Your balance is {self.user['coins']} {CHIPS}")
                await self.bot.pg_con.execute(COINS, self.author_id, self.guild_id, self.user['coins'] - self.bet)
                self.DELAY = 0.15
                for i in range(3):
                    self.lines = self.generate_sequence()
                    self.embed = await self.update_ui(ctx)
                    await self.msg.edit(embed=self.embed)
                    self.DELAY += self.DELAY / 10
                    await asyncio.sleep(self.DELAY)
                self.embed = await self.update_ui(ctx, False, True)
                await self.msg.edit(embed=self.embed)
                await self.msg.remove_reaction(self.SPIN, ctx.author)

    def generate_sequence(self):
        del self.lines[10:15]
        return self.generate_line() + self.lines

    def generate_line(self):
        line = []
        for i in range(5):
            line.append(random.choice(self.symbols))
        return line

    async def update_ui(self, ctx, opening=False, ending=False):
        embed = discord.Embed(title=self.show_reels(), color=ctx.author.color)
        embed.set_author(name='Slots', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Bet', value=f"{self.bet} {CHIPS}", inline=True)

        if opening:
            embed.set_footer(text='Press S\nto spin',
                             icon_url=self.bot.user.avatar_url)
        else:
            if ending:
                mul = self.get_multiplier() * self.bet
                await self.bot.pg_con.execute(COINS, self.author_id, self.guild_id, self.user['coins'] + mul)

                embed.set_footer(
                    text=f"WIN\n {mul} {CHIPS}", icon_url=self.bot.user.avatar_url)
                embed.title = self.show_highlighted_reels()
                for i, n in enumerate(self.lines):
                    self.lines[i] = self.lines[i].replace('`', '')
            else:
                embed.set_footer(text=f"WIN\n\u2060",
                                 icon_url=self.bot.user.avatar_url)

        self.user = await self.bot.pg_con.fetchrow(SELECT, self.author_id, self.guild_id)
        embed.add_field(
            name='Balance', value=f"{self.user['coins']} {CHIPS}", inline=True)
        return embed

    def show_highlighted_reels(self):
        space = '\n** ** '
        beauty_lines = ''
        inspace = '\u2060'
        highlight = '`'
        breaker = ' '

        for i in self.highlighted:
            if self.lines[i][0] != highlight:
                self.lines[i] = highlight + self.lines[i] + highlight + inspace
        for i in range(15):
            if i % 5 == 0:
                beauty_lines += space
            if self.lines[i][0] == highlight:
                beauty_lines += self.lines[i]
            else:
                beauty_lines += self.lines[i] + breaker

        del self.highlighted[:]
        return beauty_lines

    def check_line(self, reel1, reel2, reel3, reel4, reel5):
        result = 0
        symbol_main = ''
        lines_copy = self.lines.copy()
        wild_score = 0
        wild_symbol = ''

        for i in [reel1, reel2, reel3, reel4, reel5]:
            if self.lines[i] != self.symbols[8]:
                symbol_main = i
                wild_symbol = self.lines[i]
                break

        for i in [reel1, reel2, reel3, reel4, reel5]:
            if self.lines[i] == self.symbols[8]:
                self.lines[i] = wild_symbol

        if self.lines[reel1] == self.lines[reel2] == self.lines[reel3]:
            if self.lines[reel3] == self.lines[reel4]:
                if self.lines[reel4] == self.lines[reel5]:
                    result += self.symbols_dict.get(self.lines[symbol_main])[2]
                    self.highlighted.extend(
                        [reel1, reel2, reel3, reel4, reel5])
                else:
                    result += self.symbols_dict.get(self.lines[symbol_main])[1]
                    self.highlighted.extend([reel1, reel2, reel3, reel4])
            else:
                result += self.symbols_dict.get(self.lines[symbol_main])[0]
                self.highlighted.extend([reel1, reel2, reel3])

        self.lines = lines_copy

        return result + wild_score

    def get_multiplier(self):
        result = self.check_line(0, 1, 2, 3, 4)
        result += self.check_line(0, 6, 12, 8, 4)
        result += self.check_line(0, 6, 7, 8, 4)
        result += self.check_line(0, 1, 7, 3, 4)
        result += self.check_line(0, 6, 2, 8, 4)
        result += self.check_line(0, 11, 12, 13, 4)

        result += self.check_line(5, 6, 7, 8, 9)
        result += self.check_line(5, 2, 3, 8, 9)
        result += self.check_line(5, 1, 2, 3, 9)
        result += self.check_line(5, 11, 12, 13, 9)
        result += self.check_line(5, 6, 2, 8, 9)
        result += self.check_line(5, 6, 12, 8, 9)
        result += self.check_line(5, 1, 7, 3, 9)
        result += self.check_line(5, 11, 7, 13, 9)

        result += self.check_line(10, 11, 12, 13, 14)
        result += self.check_line(10, 6, 2, 8, 14)
        result += self.check_line(10, 6, 7, 8, 14)
        result += self.check_line(10, 11, 7, 13, 14)
        result += self.check_line(10, 6, 12, 8, 14)
        result += self.check_line(10, 1, 2, 3, 14)
        result += self.check_line(10, 11, 2, 13, 14)

        return result

    def show_reels(self):
        space = '\n** ** '
        beauty_lines = ''
        breaker = ' '

        for i in range(15):
            if i % 5 == 0:
                beauty_lines += space
            beauty_lines += self.lines[i] + breaker


def setup(bot):
    bot.add_cog(Slots(bot))

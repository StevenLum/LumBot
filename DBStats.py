import discord
from discord.ext import commands
from modules.postgresql import SELECT
from datetime import datetime

class DBStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='idk what to do with this yet')
    async def gameprofile(self, ctx):
        user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        await ctx.send(f'```Level: {user["level"]}\nExp: {user["exp"]}\nBalance: {user["coins"]}```')

    @commands.command(help='IDENTIFICATION PLEASE')
    async def profile(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        embed = (discord.Embed(title=f'Information about {member}')
                .set_thumbnail(url=f'{member.avatar_url}')
                .add_field(name='Username:', value=f'{member.name}')
                .add_field(name='ID:', value=f'{member.id}')
                .add_field(name='Nickname:', value=f'{member.nick}')
                .add_field(name='Join Date:', value=f'{member.joined_at.strftime("%A %d %B %Y")}')
                .add_field(name='Creation Date:', value=f'{member.created_at.strftime("%A %d %B %Y")}')
                )
        await ctx.send(embed=embed)
    @commands.command(aliases=['balance'], help='shows balance')
    async def bal(self, ctx):
        user = await self.bot.pg_con.fetchrow(SELECT, ctx.author.id, ctx.guild.id)
        await ctx.send(f'```Balance: {user["coins"]}```')

    @commands.command(help='shows profile picture')
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member=None):
        member = member or ctx.author

        embed = discord.Embed(color=member.color)
        embed.set_author(name=member)
        embed.set_image(url=member.avatar_url)
        #embed.set_author(name="Balance", icon_url=member.avatar_url)
        #embed.add_field(name='test', value=1, inline=True)
        #embed.add_field(name='test', value='test', inline=False)
        #embed.add_field(name='test', value='test', inline=False)
        await ctx.send(embed=embed)
        #await ctx.send(f'{member.id}, {member.guild.id}')
        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET background = $1
            WHERE user_id = $2 AND guild_id = $3
            """,
            str(member.avatar_url),
            member.id,
            member.guild.id
        )

def setup(bot):
    bot.add_cog(DBStats(bot))
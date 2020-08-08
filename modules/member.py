import discord
from discord.ext import commands



class Member:

    def get_guild_info(self, ctx): #info of users in guild
        self.user_name = []
        self.user_nickname = []
        self.user_id = []
        for member in ctx.guild.members:
            self.user_name += [member.name]
            self.user_nickname += [member.nick]
            self.user_id += [member.id]
        return self.user_name, self.user_nickname, self.user_id

    def test(self, ctx):
        ctx.send('member test')

    #Finds the discord tag ex: .get_author CP gets 'Captain Peanuts #9031'
    def get_author(self, ctx, name):
        #print(name)
        author = discord.utils.find(lambda m: m.name == name or m.nick == name, ctx.guild.members)
        #print(author)
        return author

    def find_all_users(self, ctx):
        print(ctx.guild.members)

    def get_user_id(self, ctx, name):
        print(self.user_name)

    def get_guild_id(self, ctx, name):
        pass


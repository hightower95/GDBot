import discord
from discord.ext import commands

'''
Just some fun bot commands and functions
'''


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, *args):
        """ Pong! """
        await self.bot.say(":ping_pong: Pong!")

    @commands.command()
    async def stupid(self, member: discord.Member):
        """ Says that a user is stupid """

        me = discord.utils.get(member.server.members, name='King-Pie')
        ht = discord.utils.get(member.server.members, name='hightower')

        if member == me:
            await self.bot.say('{0.mention}'.format(member) + " is really smart!")
        elif member == ht:
            await self.bot.say('{0.mention}'.format(member) + " is really stupid!")
        else:
            await self.bot.say('{0.mention}'.format(member) + " is stupid!")

    @stupid.error
    async def lookup_error(self, ctx, error):
            await self.bot.say("Who's stupid? (the format should be !stupid username)")


def setup(bot):
    bot.add_cog(Fun(bot))

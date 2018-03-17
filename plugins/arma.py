import discord
from discord.ext import commands


'''
Placeholder cog for future development
'''


class Arma:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mods(self, *args):
        """ Reply with mod info """
        await self.bot.say('Read about our mods in this steam discussion: \n'
                           'http://steamcommunity.com/groups/generallydangerous/discussions/0/3182216552774815858/ \n'
                           'Or download them directly, find our mod collection here: \n'
                           'http://steamcommunity.com/sharedfiles/filedetails/?id=869295651')

    @commands.command()
    async def server(self, *args):
        """ Reply with TS and Arma server info """
        await self.bot.say('**Teamspeak** \n'
                           'IP: ts.generallydangerous.com \n'
                           '**A3 Server** \n'
                           'IP: a3.generallydangerous.com:2302 \n'
                           'Password: GD')

def setup(bot):
    bot.add_cog(Arma(bot))

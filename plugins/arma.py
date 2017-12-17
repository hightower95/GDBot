import discord
from discord.ext import commands


'''
Placeholder cog for future development
'''


class Arma:

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Arma(bot))

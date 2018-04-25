#!/usr/bin/env python

"""
Plugin providing some fun commands
"""

import discord
from discord.ext import commands


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, *args):
        """ Pong! """
        await self.bot.say(":ping_pong: Pong!")

    @commands.command(pass_context=True)
    async def stupid(self, ctx, member: discord.Member, *args):
        """Insult another user"""

        me = discord.utils.get(member.server.members, name='King-Pie')
        ht = discord.utils.get(member.server.members, name='hightower')
        bot = discord.utils.get(member.server.members, name='GDBot')

        author = ctx.message.author

        if member == me:
            await self.bot.say('{0.mention}'.format(member) + " is really smart!")
        elif member == ht:
            await self.bot.say('{0.mention}'.format(member) + " is really stupid!")
        elif member == bot:
            await self.bot.say('{0.mention}'.format(author) + " is stupid!")
        else:
            await self.bot.say('{0.mention}'.format(member) + " is stupid!")

    @stupid.error
    async def lookup_error(self, ctx, error):
            await self.bot.say("Who's stupid? (the format should be !stupid username)")


def setup(bot):
    bot.add_cog(Fun(bot))

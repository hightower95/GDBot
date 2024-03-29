#!/usr/bin/env python

"""
Plugin providing a selection of useful commands and functions
"""

from config import Config

from discord.ext import commands
from datetime import datetime
from pytz import timezone


# Load the configuration file
config = Config('../config/config.ini')


class Utility:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def suggestion(self, ctx, *, message):
        """Give any feedback/suggestions you have for the bot"""

        time_now = datetime.now(tz=timezone('Europe/London')).strftime('%c')
        author = ctx.message.author

        stripped_message = message.encode('ascii', 'ignore').decode("utf-8")
        write_string = time_now + ' | ' + str(author) + ' | ' + str(stripped_message)

        with open('../data/suggestions.txt', 'a') as suggestions_file:
            suggestions_file.write(write_string+'\n')

        suggestions_file.close()

        await self.bot.say('{0.mention}'.format(author) + " Your suggestion has been saved: \n" +
                           '"' + message + '"')


def setup(bot):
    bot.add_cog(Utility(bot))

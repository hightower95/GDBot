from discord.ext import commands


'''
Plugin currently for providing information about the Generally Dangerous Arma 3 server
Future plans for this plugin involve interaction with the server itself
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
                           '**Arma 3 Server** \n'
                           'IP: a3.generallydangerous.com:2302 \n'
                           'Password: GD')

    @commands.command()
    async def missions(self, *args):
        """ Reply with links to our mission spreadsheets """
        await self.bot.say("Here are links to the Master and Seeder Mission spreadsheets. If you have a new mission, "
                           "add it to seeder spreadsheet first so it can be checked over. \n \n"
                           "**Missions Spreadsheet Master:** \n "
                           "https://docs.google.com/spreadsheets/d/"
                           "1mEhDKRgxhWuS7dCICNBW41zPeD7fcYft3Wb4fGeceRI/edit?usp=sharing \n"
                           "**Missions Spreadsheet Seeder** \n"
                           "https://docs.google.com/spreadsheets/d/"
                           "1_txOtbOIbEZFMsIJjjZrAVtgn8L7o0P4kkEinOpsck4/edit?usp=sharing")


def setup(bot):
    bot.add_cog(Arma(bot))

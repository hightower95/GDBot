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
        """Get links to our mod collection"""
        await self.bot.say('Read about our mods in this steam discussion: \n'
                           'http://steamcommunity.com/groups/generallydangerous/discussions/0/3182216552774815858/ \n'
                           'Or download them directly, find our mod collection here: \n'
                           'http://steamcommunity.com/sharedfiles/filedetails/?id=869295651')

    @commands.command()
    async def server(self, *args):
        """Get TeamSpeak and Arma server info"""
        await self.bot.say('**Teamspeak** \n'
                           'IP: ts.generallydangerous.com \n'
                           '**Arma 3 Server** \n'
                           'IP: a3.generallydangerous.com:2302 \n'
                           'Password: GD')

    @commands.command()
    async def missions(self, *args):
        """Get links to our mission spreadsheets"""
        await self.bot.say("Here are links to the Master and Seeder Mission spreadsheets. If you have a new mission, "
                           "add it to seeder spreadsheet first so it can be checked over. \n \n"
                           "**Missions Spreadsheet Master:** \n "
                           "https://docs.google.com/spreadsheets/d/"
                           "1mEhDKRgxhWuS7dCICNBW41zPeD7fcYft3Wb4fGeceRI/edit?usp=sharing \n"
                           "**Missions Spreadsheet Seeder** \n"
                           "https://docs.google.com/spreadsheets/d/"
                           "1_txOtbOIbEZFMsIJjjZrAVtgn8L7o0P4kkEinOpsck4/edit?usp=sharing")

    @commands.command()
    async def mission_idea(self, *args):
        """Get a randomly generated mission idea"""

        import json
        data_dictionary = json.load(open('../data/mission_generator.json'))

        def generate_random_mission(data):
            import random
            import re

            def randomly_generated(nt):
                template = random.choice(data[nt])

                def replace(match):
                    return randomly_generated(match.group(1))

                return re.sub(r'\$\{(\w+)\}', replace, template)

            mission_string = randomly_generated('template')

            return mission_string

        await self.bot.say(generate_random_mission(data_dictionary))


def setup(bot):
    bot.add_cog(Arma(bot))

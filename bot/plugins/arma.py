from config import Config

import discord
from discord.ext import commands
import os
try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])
    import requests


'''
Plugin currently for providing information about the Generally Dangerous Arma 3 server
Future plans for this plugin involve interaction with the server itself
'''

# TODO Check the necessary roles exist and warn/create them if they don't
# TODO Group the info commands

# Load the configuration file
config = Config('../config/config.ini')
# Define the holding area register path
ha_register_path = '../data/holding_area_register.json'
# Define the log path
ha_log_path = '../logs/holding_area_log.txt'


def add_ha_log_entry(author, message):
    from datetime import datetime
    from pytz import timezone

    stripped_message = message.encode('ascii', 'ignore').decode("utf-8")
    time_now = datetime.now(tz=timezone('Europe/London')).strftime('%c')

    log_string = time_now + ' | ' + str(author) + ' | ' + str(stripped_message)

    # Creates path if it doesn't already exist
    if not os.path.exists('../logs/'):
        os.makedirs('../logs/')

    with open(ha_log_path, 'a+') as log_file:
        log_file.write(log_string+'\n')


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

    # --------------------------#
    # Mission managing commands #
    # --------------------------#

    # Upload

    @commands.command(pass_context=True)
    @commands.has_any_role(config.admin_role, config.mission_upload_role)
    async def upload(self, ctx):
        """
        Upload an attached mission file to the server
        :param ctx:
        :return:
        """

        author = ctx.message.author

        # If available, gets the mention string for the mission manager role, otherwise sets to role name
        manage_role = discord.utils.get(ctx.message.server.roles, name=config.mission_manage_role)
        if manage_role.mention is None:
            mention_manage_role = manage_role.name
        else:
            mention_manage_role = manage_role.mention

        download_path = config.holding_area_path
        await verify_mission_register()

        # Checks if the channel the command is being used in is correct and directs the user to right channel
        if str(ctx.message.channel.id) != str(config.mission_upload_channel_id):
            upload_channel = discord.utils.get(ctx.message.server.channels, id=config.mission_upload_channel_id)

            if upload_channel is None:
                await self.bot.say("You must upload mission files in the correct channel in the right server")
            else:
                await self.bot.say("You must upload mission files in " + upload_channel.mention)
            return

        if ctx.message.attachments:
            for pic in ctx.message.attachments:
                url_split = str(pic['url']).split('/')
                url = str(pic['url'])
                file_name, file_extension = os.path.splitext(url_split[-1])

                # Checks the file is a .pbo
                if file_extension != '.pbo':
                    await self.bot.say("**Upload failed!** \n" 
                                       "You need to upload your mission as a .pbo \n"
                                       "If you don't know how to convert your mission into a .pbo, follow this link "
                                       "for a handy tool! \n"
                                       "http://www.armaholic.com/page.php?id=16369")
                else:

                    # Checks if the file has a duplicate in the holding area or server
                    if await check_duplicates(file_name+file_extension):
                        await self.bot.say("**Upload Failed** \n"
                                           "There is already a mission with that name uploaded. "
                                           "Please add a version number to distinguish it.")
                        return

                    assigned_mission_id = await assign_id(file_name + file_extension)
                    await self.bot.say('Uploading your file **' + file_name + file_extension + '** to the mission'
                                       ' holding area with Mission ID: ' + str(assigned_mission_id) + '. \n'
                                       + mention_manage_role + ' can approve this upload using the command `'
                                       + config.command_prefix + "approve " + str(assigned_mission_id) + "`")
                    await download_file(url, file_name, file_extension, download_path)

                    # Add log entry for mission upload
                    log_string = 'Uploaded mission: ' + file_name + file_extension
                    add_ha_log_entry(author, log_string)

        # Triggers if no attachment is found - explains how to use the command properly
        else:
            await self.bot.say("No attachment found. To upload a mission file, select the :heavy_plus_sign: symbol "
                               'next to the message box and upload your .pbo as an attachment with "'
                               + config.command_prefix + 'upload" in the comments.')

    @upload.error
    async def upload_error(self, error, *args):

        if isinstance(error, commands.CheckFailure):
            await self.bot.say("You do not have the required role to upload missions.")

    # Approve

    @commands.command(pass_context=True)
    @commands.has_any_role(config.admin_role, config.mission_manage_role)
    async def approve(self, ctx, mission_id):
        """
        Approve a mission file uploaded to the holding area
        :param ctx:
        :param mission_id:
        :return:
        """
        import json

        author = ctx.message.author

        await verify_mission_register()
        download_path = config.holding_area_path
        server_missions_path = config.server_missions_path
        mission_register = json.load(open(ha_register_path))

        # Checks if the channel the command is being used in is correct and directs the user to right channel
        if str(ctx.message.channel.id) != str(config.mission_upload_channel_id):
            upload_channel = discord.utils.get(ctx.message.server.channels, id=config.mission_upload_channel_id)

            if upload_channel is None:
                await self.bot.say("You can only approve missions in the correct channel in the right server")
            else:
                await self.bot.say("You must approve mission in " + upload_channel.mention)
            return

        # searching for the corresponding mission name
        mission_file_name = ''
        for mission_name, iden in mission_register.items():
            if iden == int(mission_id):
                mission_file_name = mission_name

        await self.bot.say("The mission: **" + mission_file_name + "** has been approved and moved onto the "
                           "live server.")

        # moving the mission to the server folder and removing the mission from the register
        os.rename(download_path+mission_file_name, server_missions_path+mission_file_name)
        await remove_id(int(mission_id))

        # add log entry
        log_string = 'Approved mission: ' + mission_file_name
        add_ha_log_entry(author, log_string)

    @approve.error
    async def approve_error(self, ctx, error):
            await self.bot.say("You must give me the mission ID of the mission you wish to approve.")

    # Reject

    @commands.has_any_role(config.admin_role, config.mission_manage_role)
    @commands.command(pass_context=True)
    async def reject(self, ctx, mission_id: int, *, rejection_message):
        """
        Reject a mission file uploaded to the holding area
        :param ctx:
        :param mission_id:
        :param rejection_message:
        :return:
        """
        import json

        author = ctx.message.author

        await verify_mission_register()
        mission_register = json.load(open(ha_register_path))

        # Checks if the channel the command is being used in is correct and directs the user to right channel
        if str(ctx.message.channel.id) != str(config.mission_upload_channel_id):
            upload_channel = discord.utils.get(ctx.message.server.channels, id=config.mission_upload_channel_id)

            if upload_channel is None:
                await self.bot.say("You can only reject missions in the correct channel in the right server")
            else:
                await self.bot.say("You must reject mission in " + upload_channel.mention)
            return

        # searching for the corresponding mission name
        mission_file_name = ''
        for mission_name, iden in mission_register.items():
            if iden == int(mission_id):
                mission_file_name = mission_name

        # delete the rejected mission and remove the mission from the register
        os.remove(config.holding_area_path + mission_file_name)
        await remove_id(int(mission_id))

        await self.bot.say("The mission: **" + mission_file_name + "** has been rejected by "
                           + str(author.display_name) +
                           " for the reason:\n \n" + rejection_message)

        # add log entry
        log_string = 'Rejected mission: ' + mission_file_name + ' with rejection message: ' + rejection_message
        add_ha_log_entry(author, log_string)

    @reject.error
    async def reject_error(self, ctx, error):
            await self.bot.say("You must give me the mission ID and a reason for rejecting the mission. \n"
                               "e.g. `" + config.command_prefix + "reject 1 Mission has no briefing`")

    # Holding area

    @commands.has_any_role(config.admin_role, config.mission_manage_role)
    @commands.command(pass_context=True)
    async def holding_area(self, ctx):
        """
        List the mission files in the holding area
        :param ctx:
        :return:
        """
        import json

        await verify_mission_register()
        mission_register = json.load(open(ha_register_path))

        # Check if command is in a private message and advise where to upload instead
        if "Direct Message" in str(ctx.message.channel):
            await self.bot.say("Missions cannot be approved via direct message - use this command in the "
                               "mission upload channel.")
            return

        # Checks if the channel the command is being used in is correct and directs the user to right channel
        if str(ctx.message.channel.id) != str(config.mission_upload_channel_id):
            upload_channel = discord.utils.get(ctx.message.server.channels, id=config.mission_upload_channel_id)

            if upload_channel is None:
                await self.bot.say("You must upload mission files in the correct channel in the right server")
            else:
                await self.bot.say("You must upload mission files in " + upload_channel.mention)
            return

        await self.bot.say("Here are the missions in the holding area:\n"
                           "**ID** : **Mission Name**\n")

        for m, i in mission_register.items():
            await self.bot.say(" **"+str(i)+"** : " + m)

    # -------------- #
    # Admin commands #
    # -------------- #

    # Clear holding area

    @commands.command(pass_context=True)
    @commands.has_role(config.admin_role)
    async def admin_clear_holding_area(self, ctx):
        """
        Admin command - clears all files from the holding area
        :param ctx:
        :return:
        """

        import json
        import os
        import shutil

        author = ctx.message.author

        # Deletes all files in a folder
        folder = config.holding_area_path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        # Clears the mission register
        mission_register = {}
        with open(ha_register_path, 'w') as file:
            file.write(json.dumps(mission_register))

        await self.bot.say("Holding area cleared.")

        # add log entry
        log_string = 'Admin cleared the holding area'
        add_ha_log_entry(author, log_string)

    @admin_clear_holding_area.error
    async def admin_clear_holding_area_error(self, ctx, error):
        pass

    @commands.command(pass_context=True, hidden=True)
    async def test(self, ctx, *, message):

        author = ctx.message.author
        message_string = "A message was sent: " + message
        add_ha_log_entry(author, message_string)


async def download_file(url, file_name, file_extension, download_path):
    """
    Downloads a file from a given URL
    """

    # Creates path if it doesn't already exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
    r = requests.get(url, headers=headers, stream=True)

    with open(str(download_path)+str(file_name)+str(file_extension), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


async def check_duplicates(file_name):

    import re

    # TODO specify whether duplicate is in the holding area or on the server

    # Creates path if it doesn't already exist
    if not os.path.exists(config.holding_area_path):
        os.makedirs(config.holding_area_path)

    # Creates path if it doesn't already exist
    if not os.path.exists(config.server_missions_path):
        os.makedirs(config.server_missions_path)

    holding_path = config.holding_area_path
    server_path = config.server_missions_path

    stripped_holding_path_files = [re.sub(r'[^a-zA-Z0-9.]', '', i.lower()) for i in os.listdir(holding_path)]
    stripped_server_path_files = [re.sub(r'[^a-zA-Z0-9.]', '', i.lower()) for i in os.listdir(server_path)]
    stripped_file_name = re.sub(r'[^a-zA-Z0-9.]', '', file_name.lower())

    duplicate_bool = False

    if stripped_file_name in stripped_holding_path_files or stripped_file_name in stripped_server_path_files:
        duplicate_bool = True

    return duplicate_bool


async def verify_mission_register():
    """
    Verifies that the holding area register is there and that the register matches the files in
    the holding area folder.
    :return:
    """
    import json
    import os

    download_path = config.holding_area_path

    # Creates path if it doesn't already exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Read the holding area register, if it isn't there then create it
    try:
        mission_register = json.load(open(ha_register_path))
    except FileNotFoundError:
        with open(ha_register_path, 'w+') as file:
            file.write(json.dumps({}))

        mission_register = json.load(open(ha_register_path))

    key_list = mission_register.keys()
    file_list = os.listdir(download_path)

    for key in key_list:
        if key in file_list:
            pass
        else:
            await remove_id(mission_register[key])


async def assign_id(file_name):
    import json

    # ha_register_path = '../data/holding_area_register.json'
    mission_register = json.load(open(ha_register_path))
    id_list = mission_register.values()

    # Horrible way for finding the lowest id which isn't already taken
    i = 1
    while True:
        if i in id_list:
            i += 1
        else:
            mission_id = i
            break

    # Adding the new mission and saving the updated register
    mission_register[file_name] = mission_id
    with open(ha_register_path, 'w') as file:
        file.write(json.dumps(mission_register))

    return mission_id


async def remove_id(mission_id):
    import json

    mission_register = json.load(open(ha_register_path))

    # searching for the corresponding mission name
    absent_mission = ''
    for mission_name, iden in mission_register.items():
        if iden == mission_id:
            absent_mission = mission_name

    try:
        del mission_register[absent_mission]
    except:
        pass

    with open(ha_register_path, 'w') as file:
        file.write(json.dumps(mission_register))


def setup(bot):
    bot.add_cog(Arma(bot))

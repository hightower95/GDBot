#!/usr/bin/env python

"""
Main file for GDBot - loads the configuration and any plugins in the ./plugins/ folder and starts the bot
"""

from config import Config

import discord
from discord.ext.commands import Bot
import platform
import glob
import os
import shutil


if __name__ == "__main__":

    # TODO raise an error if the config file is not configured properly

    config_path = '../config/config.ini'
    config_template_path = '../config/config.ini.template'
    # Check if the config file exists
    if os.path.isfile(config_path):
        # Load the configuration file
        config = Config(config_path)
    else:
        # Copy the config template and rename - then load default
        shutil.copy2(config_template_path, config_path)
        config = Config(config_path)

    # Here you can modify the bot's prefix and description and whether it sends help in direct messages
    # or not.
    bot = Bot(description="chat_bot by King-Pie#8803", command_prefix=config.command_prefix, pm_help=True)

    # This is what happens every time the bot launches. In this case, it prints information like
    # server count, user count the bot is connected to, and the bot id in the console.

    @bot.event
    async def on_ready():
        print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ') | Connected to ' + str(
            len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
        print('--------')
        print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                                   platform.python_version()))
        print('--------')
        print('Use this link to invite {}:'.format(bot.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
        print('--------')
        print('Github Link: https://github.com/King-Pie/GDBot')
        print('Based on Basic Bot by Habchy#1665 - https://github.com/Habchy/BasicBot/')
        print('--------')
        print('Created by King-Pie#8803')
        print('--------')

        load_cogs()


    def load_cogs():
        cogs = list_cogs()
        for cogs in cogs:
            try:
                print("Load {}".format(cogs))
                bot.load_extension(cogs)
            except Exception as e:
                print(e)


    def list_cogs():
        cogs = glob.glob("plugins/*.py")
        clean = []
        for c in cogs:
            c = c.replace("/", "\\")  # Linux fix
            if "__init__" in c:
                continue
            clean.append("plugins." + c.split("\\")[1].replace(".py", ""))
        return clean


    # Finally run the bot with token from config file
    bot.run(config.login_token)

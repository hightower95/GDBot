import discord
from discord.ext.commands import Bot
import platform
import glob

from bot.config import Config, ConfigDefaults

# Loading the configuration file
config = Config('../config/config.ini')

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
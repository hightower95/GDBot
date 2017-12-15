import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Here you can modify the bot's prefix and description and whether it sends help in direct messages or not.
client = Bot(description="GDBot by King-Pie#8803", command_prefix="!", pm_help=True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count
# the bot is connected to, and the bot id in the console.


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
        len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Github Link: https://github.com/King-Pie/GDBot')
    print('Based on Basic Bot by Habchy#1665 - https://github.com/Habchy/BasicBot/')
    print('--------')
    print('Created by King-Pie#8803')


# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):
    await client.say(":ping_pong: Pong!")


@client.command()
async def stupid(user):
    await client.say(user + ' is stupid')

client.run('YOUR TOKEN HERE')

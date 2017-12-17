from discord.ext import commands
import discord
import asyncio
from datetime import datetime, timedelta


class Events:

    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.schedule_check_loop = self.loop.create_task(self.check_schedule())

    # async def event_testing(self):
    #     await self.bot.wait_until_ready()
    #     channel = discord.Object(id='391599892755120153')
    #
    #     while not self.bot.is_closed:
    #
    #         time_now = datetime.utcnow()
    #         dow = time_now.isoweekday()
    #         minute = time_now.minute
    #
    #         if minute % 2 == 0:
    #             await asyncio.sleep(10)
    #             # await self.bot.send_message(channel, "Testing an announcement every 5 minutes "
    #             #                             + datetime.strftime(time_now, '%X'))
    #             print(datetime.strftime(time_now, '%X'))
    #             await asyncio.sleep(120)
    #         else:
    #             await asyncio.sleep(10)  # task runs every 10 seconds

    async def check_schedule(self):

            while True:

                await asyncio.sleep(5)

                path = './plugins/data/calendar.csv'
                for line in open(path, 'r'):
                    lines = str.split(line, ',')

    @commands.command()
    async def add_repeating_event(self, day, time, *, message=''):

        print(day, time, message)


def setup(bot):

    events = Events(bot)
    bot.add_cog(events)

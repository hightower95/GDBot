from discord.ext import commands
import discord
import asyncio
import datetime
import calendar


class Events:

    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.schedule_check_loop = self.loop.create_task(self.check_schedule())

        self.schedule = []
        self.update_schedule()

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

    def update_schedule(self):

        path = './plugins/data/mission_night_schedule.csv'
        for line in open(path, 'r'):

            day, time, message = line.strip().split(',')

            print(day, time, message)
            self.schedule.append([day, time, message])

            day_dict = dict(zip(calendar.day_abbr, range(7)))

            def next_weekday(d, weekday):
                days_ahead = weekday - d.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return d + datetime.timedelta(days_ahead)

            d = datetime.datetime.utcnow()
            next_date = next_weekday(d, day_dict[day])  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            print(next_date)

    async def check_schedule(self):

            while True:
                await asyncio.sleep(5)
                path = './plugins/data/mission_night_schedule.csv'
                for line in open(path, 'r'):
                    lines = str.split(line, ',')

    @commands.command()
    async def event_list(self, *args):

        for i in self.schedule:
            print(i)
            await self.bot.say(i)


    @commands.command()
    async def add_repeating_event(self, day, time, *, message=''):

        print(day, time, message)



def setup(bot):

    events = Events(bot)
    bot.add_cog(events)

import discord
import asyncio
from datetime import datetime
import calendar
from pytz import timezone

from config import Config, ConfigDefaults

'''
Plugin which sends reminders to a discord server's announcements channel
'''

# Load the configuration file
config = Config('../config/config.ini')


class Reminder:

    def __init__(self, day, time):

        # time to set reminder before event starts
        reminder_offset = '01:00'
        offset_hour, offset_minute = map(int, reminder_offset.split(':'))

        self.day = day
        self.time = time

        day_dict = dict(zip(calendar.day_abbr, range(1, 8)))

        self.dow = day_dict[day]
        self.hour, self.minute = map(int, time.split(':'))

        self.reminder_hour = self.hour - offset_hour
        self.reminder_minute = self.minute - offset_minute

        self.message = '@everyone Arma 3 Mission night starting @' + time + ' GMT!'

    def __repr__(self):

        return self.day + self.time


class ReminderManager:

    def __init__(self, bot):

        # channel to post announcements to
        self.channel = discord.Object(id=config.announcement_channel_id)

        self.bot = bot
        self.loop = asyncio.get_event_loop()

        self.reminder_list = self.update_schedule()

        print('Scheduled Mission nights:')
        print(self.reminder_list)

        self.test_loop = self.loop.create_task(self.check_schedule())

    def update_schedule(self):

        schedule = []
        path = '../data/mission_night_schedule.csv'
        for line in open(path, 'r'):
            day, time = line.strip().split(',')

            reminder = Reminder(day, time)
            schedule.append(reminder)

        return schedule

    async def check_schedule(self):

        await self.bot.wait_until_ready()

        while not self.bot.is_closed:

            reminder_time = '18:52'
            reminder_hour, reminder_minute = map(int, reminder_time.split(':'))

            # Current time in the UK
            time_now = datetime.now(tz=timezone('Europe/London'))
            dow = time_now.isoweekday()  # 1 = Monday, 2=Tuesday, 3=Wednesday...
            hour_now = time_now.hour
            minute_now = time_now.minute

            for reminder in self.reminder_list:

                    if dow == reminder.dow and \
                            hour_now == reminder.reminder_hour and \
                            minute_now == reminder.reminder_minute:

                        print('Sending an announcement now!')

                        await self.bot.send_message(self.channel, reminder.message)
                        print('Pausing')
                        await asyncio.sleep(60)
                        print('Resuming')

            await asyncio.sleep(30)


def setup(bot):

    events = ReminderManager(bot)
    bot.add_cog(events)

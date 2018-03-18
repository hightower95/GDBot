import datetime
import calendar
import pytz
from pytz import timezone



day_dict = dict(zip(calendar.day_abbr, range(1, 8)))

print(pytz.all_timezones)

time = datetime.datetime.utcnow()

time2 = datetime.datetime.now(tz=timezone('Europe/London'))

print(time)
print(time2)




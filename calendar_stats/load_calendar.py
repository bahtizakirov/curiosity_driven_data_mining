import my_google_calendar
from datetime import datetime
#script to debug my_google_calendar instantiation
date_min = datetime(2013, 3, 1).isoformat() + 'Z' # 'Z' indicates UTC time
date_max = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
my_calendar = my_google_calendar.GoogleCalendar('iborukhovich@remedypartners.com',date_min,date_max)

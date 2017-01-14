from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd
import datetime


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = './oauth_calendar_stats.json'
APPLICATION_NAME = 'Python'

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

#except ImportError:
#    flags = None

class GoogleCalendar:
    def get_credentials(self):

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __init__(self,calendar_email, number_of_events):


        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime(2013, 3, 1).isoformat() + 'Z' # 'Z' indicates UTC time
        status = 'Getting the upcoming 10 events'
        eventsResult = service.events().list(
            calendarId=calendar_email, timeMin=now, maxResults=number_of_events, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            status = 'No upcoming events found.'
        all_events_df = pd.DataFrame()
        print("loading events into dataframe")
        event_num = 0
        for event in events:
            event_num += 1
            print(event_num)
            event_properties = []
            for property in event:
                if property == "start":
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    start = start.replace('-05:00',"")
                    start = start.replace('-04:00',"")
                    event['start'] = start
                    try:
                        event['start'] = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
                    except:
                        event['start'] = datetime.datetime.strptime(start, '%Y-%m-%d')
                event_properties.append(event[property])
            temp_series = pd.DataFrame([event_properties], columns=event.keys())
            if all_events_df.empty:
                all_events_df = temp_series
            else:
                all_events_df = all_events_df.append(temp_series)

        self.events_df = all_events_df
        self.status = status
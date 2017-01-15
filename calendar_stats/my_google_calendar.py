from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd
import datetime

#Core code from https://developers.google.com/google-apps/calendar/quickstart/python

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = './oauth_calendar_stats.json'
APPLICATION_NAME = 'Python'

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

    def __init__(self,calendar_email, date_min, date_max):


        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        eventsResult = service.events().list(
            calendarId=calendar_email,
            timeMin=date_min,
            timeMax=date_max,
            singleEvents=True,
            maxResults=1000000,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            status = 'No upcoming events found.'
        else:
            status = str(len(events)) + " events found"
        all_events_df = pd.DataFrame()
        print("loading events into dataframe")
        event_num = 0
        for event in events:
            event_num += 1
            if event_num % 100 == 0:
                print(str(event_num) + " events processed")
            event_properties = []
            for property in event:
                if property == "start":
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    start = start.replace('-05:00',"")
                    start = start.replace('-04:00',"")
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
            all_events_df["start"] = pd.to_datetime(all_events_df["start"])
            all_events_df["startDate"] = all_events_df["start"].dt.date

        self.events_df = all_events_df
        self.status = status
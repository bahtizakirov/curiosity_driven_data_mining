import my_google_calendar
from datetime import datetime
#script to debug my_google_calendar instantiation

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas
# default plot params
params = {'legend.fontsize': 'large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'axes.facecolor': 'white'}
plt.rcParams.update(params)




def plot_meeting_counts(raw_counts, raw_counts_color, smooth_counts, smooth_counts_color):
    color_look_up = {
        "red": "r",
        "blue": "b",
        "black": "k"
    }
    raw_counts.plot(
        rot=90,
        color=color_look_up[raw_counts_color],
        label='raw counts'
    )
    smooth_counts.plot(
        rot=90,
        color=color_look_up[smooth_counts_color],
        label='7 week average',
        linewidth=3.0
    )
    raw_counts_line = mlines.Line2D([], [], color='blue', label='1 day count')
    smooth_counts_line = mlines.Line2D([], [], color='red', label='7 day average')

    plt.legend(handles=[raw_counts_line, smooth_counts_line])
    plt.xlabel('Meeting Date')
    plt.ylabel('# Meetings')
    plt.grid(True)
    fig = plt.gcf()
    fig.set_size_inches(16, 10.5)

    # plt.show()

def label_significant_events(significant_events, counts):
    significant_events["event_date"] = significant_events["event_date"].dt.date
    axes = plt.gca()
    for index, row in significant_events.iterrows():
        axes.annotate(row["event_name"], xy=(row["event_date"], counts[row["event_date"]]+1 ), xytext=(row["event_date"], counts[row["event_date"]]+2),
                                  arrowprops=dict(facecolor='black', shrink=0.05)
                                  )
    print("stop")


date_min = datetime(2016, 12, 20).isoformat() + 'Z' # 'Z' indicates UTC time
date_max = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
my_calendar = my_google_calendar.GoogleCalendar('iborukhovich@remedypartners.com',date_min,date_max)

events = my_calendar.events_df
meeting_counts_by_date = events[:-120].groupby("startDate")["startDate"].count()
smooth_meeting_counts_by_date = meeting_counts_by_date.rolling(window=7).mean()
meeting_counts_by_date = events[:-120].groupby("startDate")["startDate"].count()
smooth_meeting_counts_by_date = meeting_counts_by_date.rolling(window=7).mean()

meeting_count_plot = plot_meeting_counts(
        meeting_counts_by_date,
        'red',
        smooth_meeting_counts_by_date,
        'black'
    )
counts_plot_axes = plt.gca()
significant_events = pandas.DataFrame(
        [["first day of work\nas a junior developer", datetime(2016, 12, 20 )]], columns=["event_name", "event_date"]
)
label_significant_events(significant_events, meeting_counts_by_date )

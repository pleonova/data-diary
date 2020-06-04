import requests
import json
import arrow
from datetime import datetime
from requests.auth import HTTPBasicAuth

import numpy as np
import pandas as pd 
from datetime import date, datetime, timedelta as td



def get_activities(url, start_date, end_date, period,  level):
    # Configuration for Query
    # SEE: https://www.rescuetime.com/apidoc
    payload = {
        'perspective':'interval',
        'resolution_time': period, #1 of "month", "week", "day", "hour", "minute"
        'restrict_kind': level, #'overview', #'document', #'category'
        'restrict_begin': start_date,
        'restrict_end': end_date,
        'format':'json' #csv
    }
    
    # Setup Iteration - by Day
    d1 = pd.to_datetime(payload['restrict_begin'])
    d2 = pd.to_datetime(payload['restrict_end'])

    delta = d2 - d1
    
    activities_list = []
        
    # Iterate through the days, making a request per day
    for i in range(delta.days + 1):
        # Find iter date and set begin and end values to this to extract at once.
        d3 = d1 + td(days=i) # Add a day
        if d3.day == 1: print('Pulling Monthly Data for ', d3)

        # Update the Payload
        payload['restrict_begin'] = str(d3) # Set payload days to current
        payload['restrict_end'] = str(d3)   # Set payload days to current

        # Request
        try: 
            r = requests.get(url, payload) # Make Request
            iter_result = r.json() # Parse result
            # print("Collecting Activities for " + str(d3))
        except: 
            print("Error collecting data for " + str(d3))
    
        for i in iter_result['rows']:
            activities_list.append(i)
            
    device_df = pd.DataFrame.from_dict(activities_list)

    # Update column headers based on the level
    if level == 'document':
        device_df.columns = ['Date', 'Seconds', 'NumberPeople', 'Activity', 'Document', 'Category', 'Productivity']
    elif level == 'overview':
        device_df.columns = ['Date', 'Seconds', 'NumberPeople', 'Overview']
    else: # level == 'cateogry'
        device_df.columns = ['Date', 'Seconds', 'NumberPeople', 'SubCategory']

    # Convert to date stamp
    device_df['Date'] = pd.to_datetime(device_df['Date'])

    # Data is recorded every 5 minutes, but there is a timer second so we can re-create a more accurrate start/end date
    device_df['Seconds Sum Per 5Min'] = device_df.groupby(['Date'])['Seconds'].apply(lambda x: x.cumsum())

    device_df['Date End'] = device_df['Date'] + pd.to_timedelta(device_df['Seconds Sum Per 5Min'], unit='s')
    device_df['Date Start'] = device_df['Date End'] - pd.to_timedelta(device_df['Seconds'], unit='s')

    return device_df
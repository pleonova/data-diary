
import requests
import json
import arrow
from datetime import datetime
from requests.auth import HTTPBasicAuth

import numpy as np
import pandas as pd 
from datetime import date, datetime, timedelta as td


#######################
#### aTimeLogger #####
######################
# Modified from https://github.com/YujiShen/TimeReport/blob/master/time_api.py


def get_types(auth_header):
    """
    Retrieve types data from aTimeLogger.
    :param auth_header: auth header for request data.
    :return: A dataframe for types data.
    """
    r_type = requests.get("https://app.atimelogger.com/api/v2/types",
                      auth=auth_header)

    types = json.loads(r_type.text)
    tdf = pd.DataFrame.from_dict(types['types'])
    
    return tdf

def get_intervals(auth_header, start_date, end_date, timezone):
    """
    Retrieve new intervals data from aTimeLogger. New intervals is defined by start and end.
    :param auth_header: auth header for request data.
    :return: A dataframe for intervals data.

    Limited to 100 entries regardless of date range
    """
    start_datetime = arrow.get(pd.to_datetime(start_date), timezone)
    end_datetime = arrow.get(pd.to_datetime(end_date), timezone)
    
    r_interval = requests.get("https://app.atimelogger.com/api/v2/intervals",
                              params={'from': str(start_datetime.timestamp), 'to': str(end_datetime.timestamp)},
                              auth=auth_header)
    intervals = json.loads(r_interval.text)
    edf = pd.DataFrame.from_dict(intervals['intervals'])

    # Convert to times
    edf['from'] = edf['from'].apply(lambda x : datetime.fromtimestamp(float(x)))
    edf['to'] = edf['to'].apply(lambda x : datetime.fromtimestamp(float(x)))

    edf['type'] = edf['type'].astype(str)
    edf['type_id'] = edf['type'].str.extract(r": \'(.*?)\'")

    return edf

def get_all_intervals(auth_header, INTERVAL_MAX):
    """
    Retrieve new intervals data from aTimeLogger. Number of entries is limited by INTERVAL_MAX.
    :param auth_header: auth header for request data.
    :return: A dataframe for intervals data.
    """

    r_interval = requests.get("https://app.atimelogger.com/api/v2/intervals",
                              params={'limit': INTERVAL_MAX, 'order': 'asc'},
                              auth=auth_header)
    intervals = json.loads(r_interval.text)
    edf = pd.DataFrame.from_dict(intervals['intervals'])

    # Convert to times
    edf['from'] = edf['from'].apply(lambda x : datetime.fromtimestamp(float(x)))
    edf['to'] = edf['to'].apply(lambda x : datetime.fromtimestamp(float(x)))

    edf['type'] = edf['type'].astype(str)
    edf['type_id'] = edf['type'].str.extract(r": \'(.*?)\'")

    return edf
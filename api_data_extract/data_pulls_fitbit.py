import requests
import json
import arrow
from requests.auth import HTTPBasicAuth
import datetime

import numpy as np
import pandas as pd 


def get_sleep(auth2_client, start_date, end_date):

	# list of dates to check
	dates_list = []
	start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
	step = datetime.timedelta(days=1)

	while start <= end:
	    dates_list.append(start.date().strftime("%Y-%m-%d"))
	    start += step

	sleep_daily = [auth2_client.sleep(date) for date in dates_list]


 #    # Start of in-bed
	# date_start = [value['startTime'] for sleep_entry in sleep_daily for value in sleep_entry['sleep']]
	# # End of in-bed
	# date_end = [value['endTime'] for sleep_entry in sleep_daily for value in sleep_entry['sleep']]
	# # in-bed minutes 'timeInBed'
	# inbed_minutes = [value['timeInBed'] for sleep_entry in sleep_daily for value in sleep_entry['sleep']]

	# sleep_data = pd.DataFrame({'Date Start': date_start, 'Date End': date_end, 'InBed Minutes': inbed_minutes, 'Category': 'inBed'})
	# sleep_data['Date Start'] = pd.to_datetime(sleep_data['Date Start'])
	# sleep_data['Date End'] = pd.to_datetime(sleep_data['Date End'])
	# sleep_data['Date Abr'] = sleep_data['Date Start'].dt.date

	sleep_dateOfSleep = [feature['dateOfSleep'] 
                         for sleep_entry in sleep_daily 
                         for feature in sleep_entry['sleep']
                         for time_detail in feature['minuteData']
                        ]

	sleep_minuteData_dateTime = [time_detail['dateTime'] 
	                         for sleep_entry in sleep_daily 
	                         for feature in sleep_entry['sleep']
	                         for time_detail in feature['minuteData']
	                        ]

	sleep_minuteData_value = [time_detail['value'] 
	                     for sleep_entry in sleep_daily 
	                     for feature in sleep_entry['sleep']
	                     for time_detail in feature['minuteData']
	                    ]


	bd = pd.DataFrame({'Date': sleep_dateOfSleep, 'Time': sleep_minuteData_dateTime, 'InBed Value': sleep_minuteData_value})

	bd['InBed Value'] = bd['InBed Value'].astype(int)
	bd['Date Abr'] = pd.to_datetime(bd['Date'])
	bd['Date Start'] = pd.to_datetime(bd['Date'] + ' ' + bd['Time'])
	# hack (every entry is a minute long)
	bd['Seconds'] = 59
	bd['Date End'] = bd['Date Start'] + pd.to_timedelta(bd['Seconds'], unit='s')

	# bd['Time'] = pd.to_datetime(bd['Time'], format='%H:%M:%S').dt.time

	bd['Sleep Stage'] = np.where(bd['InBed Value'] == 1, 'asleep',
	                                np.where(bd['InBed Value'] == 2, 'restless',
	                                         'awake'
	                                        )
	                               )
	bd['Date Start Min'] = bd['Date Start'].values.astype('<M8[m]')
	bd['Date End Min'] = bd['Date End'].values.astype('<M8[m]')

	return bd



def get_steps(auth2_client, start_date, end_date):

	# list of dates to check
	dates_list = []
	start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
	step = datetime.timedelta(days=1)

	while start <= end:
	    dates_list.append(start.date().strftime("%Y-%m-%d"))
	    start += step

	activity_daily = [auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='1min') for date in dates_list]

	# ad = activity_daily[:2]

	# for tmp in ad:
	#     for dt in (tmp['activities-steps-intraday']['dataset']):
	#         for dat in tmp['activities-steps']:
	#             a = (dat['dateTime'])

	steps_dateTime = [date_event['dateTime'] 
                     for step_entry in activity_daily 
                     for feature in step_entry['activities-steps-intraday']['dataset']  # 'activities-steps-intraday': {'dataset': [{'time': '00:00:00', 'value': 0}
                     for date_event in step_entry['activities-steps']
                    ]

	steps_dataset_time = [feature['time'] 
                         for step_entry in activity_daily 
                         for feature in step_entry['activities-steps-intraday']['dataset']  # 'activities-steps-intraday': {'dataset': [{'time': '00:00:00', 'value': 0}
                        ]

	steps_minuteData_value = [feature['value'] 
                         for step_entry in activity_daily 
                         for feature in step_entry['activities-steps-intraday']['dataset']  # 'activities-steps-intraday': {'dataset': [{'time': '00:00:00', 'value': 0}
                        ]                        


	bd = pd.DataFrame({'Date': steps_dateTime, 'Time': steps_dataset_time, 'Step Value': steps_minuteData_value})

	bd['Step Value'] = bd['Step Value'].astype(int)
	bd['Date Abr'] = pd.to_datetime(bd['Date'])
	bd['Date Start'] = pd.to_datetime(bd['Date'] + ' ' + bd['Time'])
	# hack (every entry is a minute long)
	bd['Seconds'] = 59
	bd['Date End'] = bd['Date Start'] + pd.to_timedelta(bd['Seconds'], unit='s')

	# bd['Time'] = pd.to_datetime(bd['Time'], format='%H:%M:%S').dt.time

	bd['Step Activity'] = np.where(bd['Step Value'] >= 10, 'active',
	                                np.where(bd['Step Value'] >= 1, 'movement',
	                                         'sedentary'
	                                        )
	                               )

	bd['Date Start Min'] = bd['Date Start'].values.astype('<M8[m]')
	bd['Date End Min'] = bd['Date End'].values.astype('<M8[m]')

	return bd

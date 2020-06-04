#### Sleep (everything below works!)
sleep_daily = [auth2_client.sleep(date) for date in dates_list]

sleep_dateOfSleep = [feature['dateOfSleep'] 
                     for sleep_entry in sleep_daily 
                     for feature in sleep_entry['sleep']
                     for time_detail in feature['minuteData']
                    ]

sleep_dateOfSleep[:5]
# ['2019-12-15', '2019-12-15', '2019-12-15', '2019-12-15', '2019-12-15']


sleep_minuteData_dateTime = [time_detail['dateTime'] 
                         for sleep_entry in sleep_daily 
                         for feature in sleep_entry['sleep']
                         for time_detail in feature['minuteData']
                        ]
sleep_minuteData_dateTime[:5]
['22:39:00', '22:40:00', '22:41:00', '22:42:00', '22:43:00']


sleep_minuteData_value = [time_detail['value'] 
                     for sleep_entry in sleep_daily 
                     for feature in sleep_entry['sleep']
                     for time_detail in feature['minuteData']
                    ] 
sleep_minuteData_value[:5]
['2', '2', '1', '1', '1']






##### Steps
activity_daily = [auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='15min') for date in dates_list]

# Works
steps_dateTime = [feature['dateTime'] # Final Value
                     for step_entry in activity_daily 
                     for feature in step_entry['activities-steps'] # First Layer
                    ]

steps_dateTime[:5]
#['2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18', '2019-12-19']



# Does not work :(
steps_dataset_time = [time_detail['time'] # Final Value
                     for step_entry in activity_daily 
                     for feature in step_entry['activities-steps-intraday'] # First Layer
                     for time_detail in feature['dataset']
                    ]






#### Akshay's help
ad = activity_daily

for tmp in ad:
   for dt in (tmp['activities-steps-intraday']['dataset']):
       a = (dt['time'])
        
[dt['time'] for tmp in activity_daily for dt in (tmp['activities-steps-intraday']['dataset'])]


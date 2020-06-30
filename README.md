# My Data Diary

## Goals
1. Automatically upload data from various sources through APIs (RescueTime, Fitbit, aTimeLogger etc)
2. Visualize data in an meaningful manner
3. Change behavior
4. Maintain a timecapsule of my life
5. Predict future behavior


## Motivation
I used to actively journal when I was a kid. Those entries are a timecapsule of my life; those memories would have mostly been forgotten had I no record of them. That is the motivation for this project, a more automated and perhaps more objective approach to journaling - for me and for anyone else who wants to use my templates. 

I often believe I spent x time on something or didn't do y, but my data can tell me otherwise. It's through the **active** process of revisiting my data and idenitifying anomolies and finding interesting patterns, that I am able to tell a more cohesive story about different periods of my life and perhaps even make some changes in behavior. It's also helped me realize how finite time truly is.


## Overview
- API connection to 3 data streams: Fitbit (Movement and Sleep), RescueTime (Device and Applications) and aTimeLogger (Easy data logging)
- Data aggregation 
- Helper functions for visualizing data in Python
- Adaptation of the stacked bar plot for visualizing daily minutes on different activities
- Lots of charts!

## Related Posts
- June 29, 2020: Makery - External Article Mention -[Open Source Body: Small data, self-research, open humans](https://www.makery.info/en/2020/06/29/open-source-body-small-data-self-research-open-humans/)
- June 24, 2020: OpenHumans - Python Code - [RescueTime Integrated Notebook](https://exploratory.openhumans.org/notebook/161/)
- June 16, 2020: Quantified Self - Slides - [Impact of sheltering-in-place on me](https://docs.google.com/presentation/d/18iMgvHUPvdCHqEDE6oVgQ54_x5wOM0_vIWGZxnDz4Yo/edit#slide=id.p) *Recording coming soon*
- May 16, 2020: My Site - Blog Post - [How has my life changed since shelter-in-place (in charts)?](https://pleonova.github.io/shelter-in-place/)
- Feb 15, 2020: OpenHumans - Self Research Post - [Where did my time go? Expectations vs Reality](https://forums.openhumans.org/t/where-did-my-time-go-expectations-vs-reality/243)
- Feb 14, 2020: OpenHumans - Self Research Post - [How do you learn X?](https://forums.openhumans.org/t/how-do-you-learn-x/231)
- June 10, 2017: Product School/San Jose University - Invited Speaker - [Presentation](https://pleonova.github.io/visualization-tableau/) on [My Data Dashboards in Tableau](https://public.tableau.com/profile/paula#!/)


## Sample Visualizations

<img src="https://github.com/pleonova/data-diary/blob/master/images/daily_sleep_device_active.png" width="700">
A two week chart of my sleep, device and active time, by the minute.
<br/>
<br/>

<img src="https://github.com/pleonova/data-diary/blob/master/images/device_daily_rolling_prepost_shelter.png" width="900">
My screen time before and during the shelter-in-place (total 4 months worth of data).
<br/>
<br/>

<img src="https://github.com/pleonova/data-diary/blob/master/images/device_distributions.png" width="500">
Differences between the two time periods.

*Running a Welch's t-test results in a pvalue of .001, meaning I am spent a lot more time on a device during shelter-in-place.*
<br/>

## Next Steps
- [ ] Add a more detailed section in the Readme about the different files
- [ ] Incorporate heartrate data
- [ ] Extract GPS data from Google Maps
- [ ] Clean up helper function files
- [ ] Append mobile app usage with search history (RescueTime no longer captures website data)
- [ ] Store data more permanently in a database (postgres)
- [ ] Optimize helper functions for visualizations
- [ ] Move more of data prep steps into a separate .py file

*If anyone has suggestions for the above steps, especially the GPS one, I would greatly appreciate your input!*


## Acknowledgements
I wanted to thank those who had documented/shared with me their API syntax for extracting data:
- RescueTime Fitbit API: [markwk/qs_ledger](https://github.com/markwk/qs_ledger/tree/master/rescuetime)
- Fitbit API: [markwk/qs_ledger](https://github.com/markwk/qs_ledger/tree/master/fitbit) & [amandasolis/Fitbit](https://github.com/amandasolis/Fitbit/blob/master/1DayFitbit.ipynb)
- aTimeLogger API: [YujiShen/TimeReport](https://github.com/YujiShen/TimeReport/blob/master/time_api.py)

I also wanted to give a special shout out to [Mad](https://www.openhumans.org/member/madprime/) and [Bastian](https://www.openhumans.org/member/gedankenstuecke/) for creating the [OpenHumans](https://www.openhumans.org/about/) platform, a rich community for self research which served as continued inspiration to keep chipping away at this passion project of mine. 


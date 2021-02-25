import requests
import os
from datetime import date, datetime, timedelta as td
import matplotlib.dates as mdates

import pandas as pd
import numpy as np
import random



############ Data Munging ############
def time_dataframe_prep(df, start_date, end_date, start_date_column, end_date_column, category_column):
    """    
    Returns an exploded dataframe, with every minute labeled with the event name or 'no entry'.
    
    Parameters
    ----------
        df : dataframe
            A dataframe that contains tagged timstamps
        start_date : str
            Date of first entry 
        end_date :str 
            Date of last entry
        start_date_column : datetime
            Column that contains when the event started
        end_date_column : datetime 
            Column that contains when the event ended
        category_column : str
            Column that contains the event tag name

    
    Returns
    -------
        df_minutes_se : dataframe
            Table with every minute tagged
    
    
    """
    ########################    
    ## Step 1: Create a dataframe of just the end dates
    ########################
    df_end = df[[end_date_column]].copy()
    # Add a column for 'no entry'
    df_end[category_column] = 'no entry'

    # If there is no gap in data (as in there is an entry immediately following the previous),
    # remove the record from the df_end dataframe
    start_date_pt_list = list(df[start_date_column].unique())
    df_end = df_end[~df_end[end_date_column].isin(start_date_pt_list)]

    ########################
    ## Step 2: Combine End and Start Dates into single dataframe
    ########################
    # Create a two column data frame with the start date and the category
    df_start = df[[start_date_column, category_column]].copy()

    # Update column names to match that of df_start
    df_end.rename(columns = {end_date_column: start_date_column}, inplace = True)
    # Append the df_end dataframe to the bottom
    df_entries = pd.concat([df_start, df_end])

    ########################
    ## Step 3: Expand Dataset - Every Second
    ########################
    # Create a dataframe of second intevals between two dates   
    time_range = pd.date_range(start_date, end_date, freq= '1s')
    time_range_df = pd.DataFrame(time_range).rename(columns = {0: 'date_time'})
    # Convert to time
    time_range_df['date_time'] = pd.to_datetime(time_range_df['date_time'])
    
    ########################
    ## Step 4: Add our time stamps to the expanded time dataframe
    ########################
    df_seconds = pd.merge(time_range_df, df_entries, how = 'left',  
                      left_on = 'date_time', right_on = start_date_column)
    # Find the first date_time with a category entry
    date_of_first_entry = df_seconds[(df_seconds[category_column] != 'no entry')  
                                     & (~df_seconds[category_column].isna())  
                                    ]['date_time'].min()
    # Find the index of the first entry
    index_of_first_entry = df_seconds.index[df_seconds['date_time'] == date_of_first_entry][0]
    # Reduce the dataframe to begin with the first entry
    df_seconds2 = df_seconds[index_of_first_entry:].copy()
    
    ########################
    ## Step 5: Label every minute
    ########################
    # Forward fill the category until next entry
    df_seconds2[category_column] = df_seconds2[category_column].ffill()
    df_seconds2[start_date_column] = df_seconds2[start_date_column].ffill()

    ########################
    ## Step 6: Pick the end of a minute entry (at 58 seconds)
    ########################
    # Expand the time stamp into the relevant time components
    
    # df_seconds2[['hour','minute','second']] = pd.to_timedelta(
    #     df_seconds2['date_time']).dt.components.iloc[:, 1:4]
    df_seconds2['hour'] = df_seconds2['date_time'].dt.hour
    df_seconds2['minute'] = df_seconds2['date_time'].dt.minute
    df_seconds2['second'] = df_seconds2['date_time'].dt.second

    # Select the entries at specified second interval (otherwise the frequency is too much for the chart)
    df_minutes = df_seconds2[df_seconds2['second'] == 58].reset_index()
    df_minutes['date_time_min'] = df_minutes['date_time'].values.astype('<M8[m]')

    ########################
    ## Step 7: Add duration columns
    ########################
    df_minutes['duration_minutes'] = 1

    # Find the index of the latest entry
    latest_date = df_minutes[df_minutes[category_column] != 'no entry']['date_time'].max()
    index_of_last_entry = df_minutes.index[df_minutes['date_time'] == latest_date][0]

    # Reduce the dataframe to begin with the first entry
    df_minutes_se = df_minutes[0:index_of_last_entry].copy()

    return df_minutes_se


import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

fsize = 18
params = {
    'axes.labelsize': fsize, 
    'axes.titlesize':fsize, 
    'axes.titlepad': 20,
    'xtick.labelsize':fsize,
    'xtick.major.pad': 5, 
    'ytick.labelsize':fsize,
    'axes.labelpad': 20,
    'lines.linewidth' : 3,
    'figure.titlesize': fsize *1.5,
    'figure.figsize' : (16,8),
    'legend.title_fontsize': fsize,
    'legend.fontsize': fsize #*0.925, 
} 
plt.rcParams.update(params) 
plt.close('all')


color_palette_p = [
    "#e8bca7",
    '#911eb4',
    '#8b88cc', 
    '#d1952e',
    "#88ccbf",
    "#D2D179",
    "#4084BF", 
    '#e6194b', 
    '#52965b', 
    '#fbcc11', 
    '#4363d8', 
    '#f58231',
    "#5cb569",
    "#88ccbf",
    '#c45748',
    '#b7b1b0',
    '#8ba3dd',
    '#b7a519',
    '#b27c62',
    '#e0c8a6'
]

my_color_schema = {'asleep': '#783f04ff', 
                    'device': '#70a1f5', 
                    'active': '#f1c232ff',
                    'movement': '#e58829', 
                    'restless': '#ffccf2',
                    'awake': '#00ff3f', ##7fffd4',
                    'no entry': '#ffffff',
                    'other': '#e8e8e8',
                    'project': '#05A9CA',
                    'coursework': '#CBA54F',
                    'Software Development': '#295ce5',
                    'Communication & Scheduling': '#c87d93',
                    'Utilities': '#66ff99',
                    'Reference & Learning': '#66ccff',
                    'Social Networking': '#22db35',
                    'Entertainment': '#e52962',
                    'Uncategorized': '#0b0a0a',
                    'Design & Composition': '#b734f2',
                    'Shopping': '#d4ea20',
                    'News & Opinion': '#f9dfc9',
                    'Business': '#4f9618',


                    }
my_color_categories = [key for (key, value) in sorted(my_color_schema.items())]                    
my_color_palette = [value for (key, value) in sorted(my_color_schema.items())]



def organize_categories_colors(d, category_column, colors, specified_category_list):
    ### Colors & Categories
    category_list = list(d[category_column].unique())
    
    ## Which categories have not yet been assigned a color in the my_color_schema
    unknown_category_list = list(set(category_list) - set(my_color_categories))

    # Generate color pallete if no color list was provided
    r = lambda: random.randint(0,255)
    long_color_list = []
    if colors == None:
        for i in range(0, len(unknown_category_list)):
            long_color_list.append('#%02X%02X%02X' % (r(),r(),r()))
        color_list = long_color_list
    else:
        color_list = colors
        
    # Zip colors
    color_pairs_new = dict(zip(unknown_category_list, color_list))

    # Add the category/color pairs already defined in my_color_schema dictionary
    known_category_list = list(set(category_list) & set(my_color_categories))
    modified_my_color_schema = {x: my_color_schema[x] for x in known_category_list}


    # Combine new 
    color_pairs = {**color_pairs_new, **modified_my_color_schema}


    # Focus only a subset of categories
    if specified_category_list != None:
        # Create a list where all but the specified entries are included
        category_list_remaining = category_list.copy()
        [category_list_remaining.remove(x) for x in specified_category_list]
        # Convert all the not specified entries to the same color (make it easier to visually inspect for patterns)
        color_pairs.update(dict.fromkeys(category_list_remaining, '#e8e8e8'))

    # Ordered categories and colors
    category_list_names_ordered = [key for (key, value) in sorted(color_pairs.items())]
    color_palette = [value for (key, value) in sorted(color_pairs.items())]
    
    return color_palette, category_list_names_ordered, color_pairs



def create_chart_xy_components(d, date_time_column, start_date, end_date, category_column):
    d = d[(d[date_time_column] >= start_date) & (d[date_time_column] <= end_date)].copy()

    ### X & Y Axis
    # x-axis time periods
    d['Date Abr'] = d['date_time'].dt.date
    
    # Add day of week
#     d['day_of_week'] = d['date_time'].dt.dayofweek
#     d['day_of_week'] = d['date_time'].dt.strftime('%a')
#     d['date_week'] = d['Date Abr'].astype(str) +', ' + d['day_of_week'].astype(str)
    d['date_week'] = d['date_time'].dt.strftime('%Y-%m-%d, %a')

    # y-axis scaled for 24 hour period
    d['time_from_day_start'] = (d[date_time_column] - d[date_time_column].dt.normalize()).dt.total_seconds().fillna(0)/(60*60)
    
    return d


def daily_chart_24_hours(d, category_column, category_list_names_ordered, color_palette, 
    add_reference_lines, top_line, bottom_line, 
    legend_on, turn_xaxis_on,
    new_yaxis_labels = False,
    new_ref_line_text = False
):
    
    plt.style.use('fivethirtyeight')

    v_val	= 0
    h_val	= 200
    verts	= list(zip([-h_val,h_val,h_val,-h_val],[-v_val,-v_val,v_val,v_val]))

    fig, ax = plt.subplots()

    for i in range(len(category_list_names_ordered)):
        plt.scatter(d[d[category_column] == category_list_names_ordered[i]]['Date Abr'], 
                    d[d[category_column] == category_list_names_ordered[i]]['time_from_day_start'], 
                    s = 1800,
                    c = color_palette[i],
                    marker = (verts),
                )
    plt.yticks(np.arange(0, 25, step=6))
    if new_yaxis_labels:
    	plt.yticks(np.arange(0, 25, step=6), new_yaxis_labels) 


    xstart = d['Date Abr'].min() - pd.DateOffset(days=1)
    xend = d['Date Abr'].max() + pd.DateOffset(days=1)
    plt.xlim(xstart, xend)

    # Add labels with Day of the week at the end, ordered
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %-d, %a'))

    # Remove the extra date at the front and end
    locs, labels = plt.xticks() 
    date_label_list = list(d['date_time'].dt.strftime('%b %-d, %a').unique())
    plt.xticks(np.arange(locs[0] - 1, locs[0] + len(date_label_list) + 1, step =1), 
        [""] + [""] + date_label_list, 
        rotation=90)

    if turn_xaxis_on == False:
        ax.tick_params(labelbottom=False)    


    if legend_on == True:
        leg = plt.legend(category_list_names_ordered, bbox_to_anchor=(1.11,0.5), 
                   loc="center", title = (r"$\bf{" + category_column + "}$"), fancybox=True)

        for i in leg.legendHandles:
            i.set_linewidth(7)
    else:
        plt.legend('')

    plt.ylabel('Time of Day')
    plt.gca().invert_yaxis()
    plt.xlabel('Date')
    plt.title(r"$\bf{" + 'Recorded' + "}$" + ' ' + r"$\bf{" + 'Daily' + "}$" + ' ' + r"$\bf{" + 'Minutes' + "}$" +
        f"\nDate Range: {str(xstart.strftime('%Y-%m-%d'))} to {str(xend.strftime('%Y-%m-%d'))}")
    # plt.title(f'Daily Activities \n Date Range: {str(xstart.strftime("%Y-%m-%d"))} to {str(xend.strftime("%Y-%m-%d"))}', fontweight = 'bold')


    ## Reference Lines
    if add_reference_lines == True:

        # Alternative titles
    	if new_ref_line_text:
    		top_line_text = new_ref_line_text[0]
    		bottom_line_text = new_ref_line_text[1]
    	else:
    		top_line_text = '  Start: {}'.format(top_line)
    		bottom_line_text = '  End: {}'.format(bottom_line)

    	plt.axhline(y=top_line, linewidth=2, color='black', linestyle = '--')
    	plt.text(x=xend, y=top_line, s=top_line_text, alpha=0.7, color='#334f8d')
    	plt.axhline(y=bottom_line, linewidth=2, color='black', linestyle = '--')
    	plt.text(x=xend, y=bottom_line, s=bottom_line_text, alpha=0.7, color='#334f8d')



    plt.show()


def pivot_data_with_missing_days(data, specified_category_list, remove_no_entry_category,
     values_column_name, values_hour_conversion, category_column):

  # If you don't want the "no entry" in the list of categories, remove it
    if remove_no_entry_category == 1:
        ## Using a set loses the order and switches the colors to no longer match original
        # specified_category_entries = list(set(specified_category_list) - set(['no entry']))  
        specified_category_entries = specified_category_list.copy()
        specified_category_entries.remove('no entry')
    else:
        specified_category_entries = specified_category_list

    # List of all dates, ordered
    date_list = list(data['Date Abr'].unique())
    date_list.sort()
    
    # Aggregate data
    d2_alt = data[data[category_column].isin(specified_category_entries)].groupby([category_column, 'Date Abr'])[values_column_name].sum().reset_index()
    d2_alt['hours'] = d2_alt[values_column_name]/(values_hour_conversion)
    # total_time = round(d2_alt['hours'].sum(),2)
    
    # Create a pivot table in order to create a stacked bar chart
    pivot_d21 = d2_alt.pivot(index='Date Abr', columns=category_column, values='hours')

    # Add any missing dates to the table
    missing_dates = set(date_list) - set(list(pivot_d21.index))
    pivot_d2 = pivot_d21.reindex(pivot_d21.index.tolist() + list(missing_dates)).sort_index()

    return pivot_d2 #, total_time #, specified_category_entries



def stacked_bar_chart_categories(pivot_data, color_pairs, legend_on, ymax, ystep):
    
    # List of dates
    dates = pivot_data.reset_index()['Date Abr']
    # date_list = list(pd.to_datetime(dates).dt.strftime('%Y-%m-%d, %a'))
    date_list = list(pd.to_datetime(dates).dt.strftime('%b %-d, %a'))
    # date_list.sort()

    # Categories and the matching colors
    specified_category_entries	= list(pivot_data.T.index)
    cat_color_pairs_alt 		= {item: color_pairs.get(item) for item in specified_category_entries}
    colors_alt 					= list(cat_color_pairs_alt.values())

    # Create x-axis names and tick positions
    objects = date_list
    pos = np.arange(len(date_list))

    #### Plot ####
    plt.style.use('fivethirtyeight')

    pivot_data.plot.bar(stacked=True, 
                  color = colors_alt, 
                  figsize=(12,6),
                  edgecolor = 'black', 
                  linewidth = 1)

    plt.xticks(pos, objects )
    # locs, labels = plt.xticks(pos, objects)           # Get locations and labels
    # plt.xticks(locs, [""] + list(d['date_time'].dt.strftime('%Y-%m-%d, %a').unique()) + [""], rotation=90)

    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, ymax, step=ystep)) 


    if legend_on == True:
        plt.legend(specified_category_entries , bbox_to_anchor=(1.25,0.5), loc="center")
    else:
        plt.legend('')
     

    plt.ylabel('Hours')
    plt.xlabel('Week Start')
    plt.title('Total Time Spent: ' + r"$\bf{" + str(round(pivot_data.sum().sum(),2)) + "}$" + ' Hours' )


    plt.show()


def horizontal_bar_chart_totals(pivot_data, num_categories, color_pairs, category_column, ytick_labels_on):
    color_df = pd.DataFrame.from_dict(color_pairs.items())
    color_df.rename(columns = {0: category_column, 1: 'Color'}, inplace = True)

    cat_totals_df = pivot_data.sum().reset_index()
    cat_totals_df.rename(columns = {0: 'Total Time'}, inplace = True)
    cat_totals_df['Total Time'] = round(cat_totals_df['Total Time'],2)

    cat_totals_df = pd.merge(cat_totals_df, color_df, how = 'left', on = category_column)
    cat_totals_df.sort_values('Total Time', ascending = False, inplace = True)

    plt.style.use('fivethirtyeight')

    cdata = cat_totals_df.head(num_categories)
    ax = sns.barplot(x='Total Time', y=category_column, hue=category_column, 
                     data=cdata, palette=list(cat_totals_df['Color']), 
                     dodge=False, edgecolor=".2")
    # ax.legend(bbox_to_anchor=(1.35,0.5), loc="center")
    ax.legend_.remove()

    # Add total sum values at the end of the bar
    for i, v in enumerate(cdata['Total Time']):
        ax.text(v, i, " " + str(v), color=list(cat_totals_df['Color'])[i], va='center', fontweight='bold')

    plt.title('Total Time Spent: ' + r"$\bf{" + str(round(pivot_data.sum().sum(),2)) + "}$" + ' Hours' )
    plt.xlabel('Hours')

    if ytick_labels_on == False:
        ax.tick_params(labelleft=False)    


    plt.show()



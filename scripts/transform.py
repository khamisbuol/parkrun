import pandas as pd
import numpy as np
from scrape import get_html_table

###################################################################################################
#                                                                                                 #
# This module contains a series of functions that are used to process parkrun                     #
# data. Data may be for global results, country specific, or location specific.                   #
#                                                                                                 #
###################################################################################################


###################################################################################################
#                                                                                                 #
# Function list:                                                                                  #
#   - get_first_finishers()       : Retrieves first place finishers                               #
#   - get_sub_seventeen_runners() : Retrieves athletes who've finished in less than 17 mins       #
#   - get_top_age_grade()         : Retrieves atheletes with highest age categories               #
#   - get_new_category_records()  : Retrieves age group category records                          #
#   - get_course_records()        : Retrieves course records for Parkrun locations                #
#   - get_freedom_finishers()     : Retrieves data for athletes who have run freedom Parkrun      #
#   - get_attendance_records()    : Retrieves attendance records for Parkrun locations            #
#   - get_most_events()           : Retrieves athletes with most events attendend                 #
#   - get_most_first_finishes()   : Retrieves atheletes with most first place finishes            #
#   - get_largest_clubs()         : Retrieves clubs with largest number of atheletes              #
#   - get_latest_results()        : Retrieves the latest results of a Parkrun location            #
#   - get_not_parkrunners()       : Retrieves athletes who have run (not)parkruns !!DEPRECATED!!  #
#                                                                                                 #
###################################################################################################


def get_first_finishers(url):

    df = get_html_table(url)

    # Assign names to columns
    columns = ['Event', 'Athlete ID', 'Athlete Name', 'Club']

    # Split df into two
    df1 = df.iloc[:, :4]
    df2 = df.drop(df.columns[1:4], axis=1)

    # Assign column names to split dfs
    df1.columns = columns
    df2.columns = columns

    # Assign unknown if athlete name is blank, otherwise assign gender
    df1['Gender'] = np.where(df1['Athlete Name'] == '', 'Unknown', 'Male')
    df2['Gender'] = np.where(df2['Athlete Name'] == '', 'Unknown', 'Female')

    # Concatenate both dataframes together
    df = pd.concat([df1, df2])

    # Reorder columns
    col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 'Club']
    df = df[col_reorder]

    #
    # Replace any Unattached values with blanks. This occurs in the global
    # parkrun results
    #
    df['Club'] = df['Club'].str.replace('Unattached', '')
    return df


def get_sub_seventeen_runners(url):
    df = get_html_table(url)

    df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 'Club']

    df['Club'] = df['Club'].str.replace('Unattached', '')

    return df

def get_top_age_grade(url):
    df = get_html_table(url)

    df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 
                  'Age Group', 'Age Grade', 'Club']
    
    col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 
                   'Age Range', 'Age Group', 'Age Grade', 'Time', 'Club']
    
    df['Age Range'] = df['Age Group'].str.extract(r'(\d+-\d+|\d+)')
    df['Gender']    = df['Age Group'].str.extract(r'([A-Z]{2})').apply(lambda x: x.str[-1])
    
    df['Gender'] = df['Gender'].replace('', 'Unknown')

    df['Gender'] = np.where(df['Gender'] == 'M', 'Male', 'Female')

    df['Club'] = df['Club'].str.replace('Unattached', '')

    # Reorder columns
    df = df[col_reorder]

    return df


def get_new_category_records(url):

    df = get_html_table(url)

    df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 
                  'Age Group', 'Age Grade', 'Club']
    
    col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 
                   'Age Range', 'Age Group', 'Age Grade', 'Time', 'Club']
    
    df['Age Range'] = df['Age Group'].str.extract(r'(\d+-\d+|\d+)')
    df['Gender']    = df['Age Group'].str.extract(r'([A-Z]{2})').apply(lambda x: x.str[-1])
    
    df['Gender'] = df['Gender'].replace('', 'Unknown')

    df['Gender'] = np.where(df['Gender'] == 'M', 'Male', 'Female')

    df['Club'] = df['Club'].str.replace('Unattached', '')

    # Reorder columns
    df = df[col_reorder]

    return df

def get_course_records(url):

    df = get_html_table(url)

    # Split df into two
    df1 = df.iloc[:, :5]
    df2 = df.drop(df.columns[1:5], axis=1)

    columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 'Date']

    col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 'Time', 'Date']

    df1.columns = columns
    df2.columns = columns
    df1['Gender'] = np.where(df1['Athlete Name'] == '', 'Unknown', 'Female')
    df2['Gender'] = np.where(df2['Athlete Name'] == '', 'Unknown', 'Male')

    df = pd.concat([df1, df2])

    df = df[col_reorder]
    return df

def get_freedom_finishers(url):
    '''
    Deprecated for some countries, and may soon get deprecated for others 

    '''

    df = get_html_table(url)
    df.columns = ['Athlete ID', 'Athlete Name', 'Date', 'Location', 'Time']
    return df


def get_attendance_records(url):
    df = get_html_table(url)
    df.columns = ['Event', 'Record Attendance', 'Record Week', 'This Week']

    # Assign the no. athletes of 'Record Week' to 'This Week' if New record 
    # was set this week
    df.loc[df['This Week'].str.contains('New'), 'This Week'] = df['Record Attendance']

    return df

def get_most_events_attended(url):
    '''
    Current implementation does not include 'Home Country' of an Athlete, i.e.,
    where they initially signed up with Parkrun. 
    
    This can be integrated and would involve modifying the 'scrape.py' script such 
    that we can identify the country based on athlete url. 
    
    E.g., https://www.parkrun.com.au/parkrunner/12345 implies the athlete is 
    from Australia. 

    '''

    def assign_milestone(no_runs):
        '''
        This function assigns a milestone for based on number of runs done 
        by a parkrunner.

        Current no clubs assigned for less than 25 runners, and for runners 
        who've ran more than 1000 parkruns. 

        '''
        if no_runs >= 25 and no_runs < 50:
            return 25
        elif no_runs >= 50 and no_runs < 100:
            return 50
        elif no_runs >= 100 and no_runs < 250:
            return 100
        elif no_runs >= 250 and no_runs < 500:
            return 250
        elif no_runs >= 500 and no_runs < 1000:
            return 500
        else:
            return
    
    df = get_html_table(url)

    #
    # For global results
    #
    if len(df.columns) == 5:
        df.columns = ['Athlete ID', 'Athlete Name', 
                      'Parkrun Club', 'No. Unique Events (Global)', 
                      'Total Runs Worldwide']
    
    #
    # For country specific
    #
    if len(df.columns) == 6:
        df.columns = ['Athlete ID', 'Athlete Name', 
                      'Parkrun Club', 'No. Unique Events (in Home Country)', 
                      'Total Parkruns (in Home Country)', 'Total Runs Worldwide']

    # Convert 'Total Runs Worldwide' to int
    df['Total Runs Worldwide']   = df['Total Runs Worldwide'].astype(int)

    # Assign milestones
    df['Parkrun Club'] = df['Total Runs Worldwide'].apply(assign_milestone)

    return df

def get_most_first_finishes(url):
    df = get_html_table(url)
    df.columns = ['Athlete ID', 'Athlete Name', 'No. First Place Finishes']
    return df

def get_largest_clubs(url):
    df = get_html_table(url)
    
    # Remove links column
    df = df.drop(df.columns[3], axis=1)

    # Assign column names
    df.columns = ['Club Name', 'No. Athletes', 
                    'No. Runs']
    return df

def get_latest_results(url):
    df = get_html_table(url)
    return df

def get_not_parkrunners(url):
    '''

    !!! CURRENTLY DEPRECATED !!!

    - Location - The Location (event or country) with (not)parkrun representations.
    - parkrunners - the number of unique participants who have recorded a (not)parkrun.
    - (not)parkruns - the total number of (not)parkruns recorded for the given time period.
    - Average Time - the average time submitted for the given (not)parkruns.

    '''

    columns = ['Location', 'No. Athletes', 'Total No. Runs', 'Average Time']

    df = get_html_table(url)

    #
    # Remove all the country data extracted from 'Australia' onwards
    #
    i = df[df.iloc[:,1] == 'https://www.parkrun.com.au/results/notparkrun'].index[0]
    df = df.iloc[:i]
    # df = df.drop(df.columns[1], axis=1)

    # Assign column names
    df.columns = columns

    return df

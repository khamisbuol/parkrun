import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from get_data import get_html_table, get_response


class Parkrun:
    
    COUNTRIES_URL           = 'https://www.parkrun.com/countries/'
    FIRST_FINISHERS_URL     = 'https://www.parkrun.com/results/firstfinishers/'
    # NEW_AGE_CATEGORY_URL    = 'https://www.parkrun.com/results/newcategoryrecords/'
    SUB_SEVENTEEN_URL       = 'https://www.parkrun.com/results/sub17/'
    TOP_AGE_CATEGORY_URL    = 'https://www.parkrun.com/results/topagegrade/'
    NEW_CAT_RECORDS_URL     = 'https://www.parkrun.com/results/newcatrecords/'
    COURSE_RECORDS_URL      = 'https://www.parkrun.com/results/courserecords/'
    FREEDOM_URL             = 'https://www.parkrun.com/results/freedom/'
    ATTENDACE_RECORDS_URL   = 'https://www.parkrun.com/results/attendancerecords/'
    MOST_EVENTS_URL         = 'https://www.parkrun.com/results/mostevents/'
    MOST_FIRST_FINISHES_URL = 'https://www.parkrun.com/results/mostfirstfinishes/'
    LARGEST_CLUBS_URL       = 'https://www.parkrun.com/results/largestclubs/'

    def __init__(self) -> None:

        self.countries_dict, self.countries_list = Parkrun.__get_countries()

        pass
    
    @staticmethod
    def __get_countries():
        """
        This function reads 
        """
        try:

            response = get_response(Parkrun.COUNTRIES_URL)

            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the divs with the class 'section-wrap'
            country_sections = soup.find_all('div', class_="section-wrap")
            countries_dict = {}
            for country_section in country_sections:

                # Retrieve name, info and url from section
                name = country_section.h2.string
                info = country_section.p.string
                url  = country_section.a['href']
                
                # Add info and url for each country to dictionary
                countries_dict[name] = {'info': info, 'url': url}
        
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        countries_list = list(countries_dict.keys())
        return countries_dict, countries_list
    
    def get_first_finishers(self) -> pd.DataFrame:

        # Get unprocess dataframe
        df = get_html_table(Parkrun.FIRST_FINISHERS_URL)

        # Assign names to columns
        columns = ['Event', 'Athlete ID', 'Athlete Name', 'Club']

        # Column reorder
        col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 'Club']
        
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

        # Reorder column names
        df = df[col_reorder]

        return df
    
    def get_sub_17_finishers(self) -> pd.DataFrame:
        """
        Limitation: cannot locate gender from url page. 
        
        Could potentially utilise runner url to find recent runs which contain 
        their gender. 

        """
        df = get_html_table(Parkrun.SUB_SEVENTEEN_URL)
        df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 'Club']
        return df
    
    def get_top_age_category(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.TOP_AGE_CATEGORY_URL)
        df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 
                      'Age Group', 'Age Grade', 'Club']
        
        # col_reorder = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 
        #                'Age Range', 'Age Group', 'Age Grade', 'Time', 'Club']
        
        df['Age Range'] = df['Age Group'].str.extract(r'(\d+-\d+|\d+)')
        df['Gender']    = df['Age Group'].str.extract(r'([A-Z]{2})').apply(lambda x: x.str[-1])
        
        df['Gender'] = df['Gender'].replace('', 'Unknown')

        df['Gender'] = np.where(df['Gender'] == 'M', 'Male', 'Female')

        # df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Gender', 
        #                'Age Range', 'Age Group', 'Age Grade', 'Time', 'Club']
        
        return df
    
    def get_new_category_records(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.NEW_CAT_RECORDS_URL)
        df.columns = ['Event', 'Athlete ID', 'Athlete Name', 'Time', 
                      'Age Group', 'Age Grade', 'Club']
        
        df['Age Range'] = df['Age Group'].str.extract(r'(\d+-\d+|\d+)')
        df['Gender']    = df['Age Group'].str.extract(r'([A-Z]{2})').apply(lambda x: x.str[-1])

        df['Gender'] = df['Gender'].replace('', 'Unknown')

        df['Gender'] = np.where(df['Gender'] == 'M', 'Male', 'Female')
        
        
        return df

    def get_course_records(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.COURSE_RECORDS_URL)

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
    
    def get_freedom_finishers(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.FREEDOM_URL)
        df.columns = ['Athlete ID', 'Athlete Name', 'Date', 'Location', 'Time']
        return df
    
    def get_attendance_records(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.ATTENDACE_RECORDS_URL)
        df.columns = ['Event', 'Record Attendance', 'Record Week', 'This Week']

        # Assign the no. athletes of 'Record Week' to 'This Week' if New record 
        # was set this week
        df.loc[df['This Week'].str.contains('New'), 'This Week'] = df['Record Attendance']

        return df
    
    def get_runners_with_most_events(self) -> pd.DataFrame:

        def assign_milestone(no_runs):
            """
            This function assigns a milestone for based on number of runs done 
            by a parkrunner.

            Current no clubs assigned for less than 25 runners, and for runners 
            who've ran more than 1000 parkruns. 

            """
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
        
        df = get_html_table(Parkrun.MOST_EVENTS_URL)

        df.columns = ['Athlete ID', 'Athlete Name', 'Parkrun Club', 
                      'No. Events', 'Total Runs']

        # Convert 'Total Runs' to int
        df['Total Runs']   = df['Total Runs'].astype(int)

        # Assign milestones
        df['Parkrun Club'] = df['Total Runs'].apply(assign_milestone)

        return df
    
    def get_most_first_finishers(self) -> pd.DataFrame:
        df = get_html_table(Parkrun.MOST_FIRST_FINISHES_URL)
        df.columns = ['Athlete ID', 'Athlete Name', 'No. First Place Finishes']
        return df
    
    def get_largest_clubs(self) -> pd.DataFrame:
        # Get HTML data of column
        df = get_html_table(Parkrun.LARGEST_CLUBS_URL)
        
        # Assign column names
        df.columns = ['Club Name', 'No. Athletes', 
                      'No. Runs', 'Club Home Page (External Links)']

        # Remove ' home page' from the last column
        df[df.columns[-1]] = df[df.columns[-1]].str.replace(' home page', '')

        return df



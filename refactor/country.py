import parkrun
import difflib
import pandas as pd
from get_data import get_html_tables, get_response

class Country:
    #
    # Attributes of a country
    # - Get attendance records: https://www.parkrun.co.at/results/attendancerecords/
    # - Get locations: from attendance records
    # - Get parkrunners who have run the most events: https://www.parkrun.co.at/results/mostevents/
    # - Get largest clubs: https://www.parkrun.co.at/results/largestclubs/
    # - Get club 100 parkrunners (parkrunners who've recently reached 100 parkruns): https://www.parkrun.co.at/results/100clubbers/
    # - Get not parkrun history: https://www.parkrun.co.at/results/notparkrun/
    # - Get freedom runners: https://www.parkrun.co.at/results/freedom/ 
    # - Get most first finishes: https://www.parkrun.co.at/results/mostfirstfinishes/
    # - Get first finishers of the week: https://www.parkrun.co.at/results/firstfinishers/
    # - Get sub 17 runners of the week: https://www.parkrun.co.at/results/sub17/
    # - Top Age grade of the week: https://www.parkrun.co.at/results/topagegrade/
    # - New Age Category set this week: https://www.parkrun.co.at/results/newcategoryrecords/
    # - Course records: https://www.parkrun.co.at/results/courserecords/

    ATTENDANCE_RECORDS   = 'results/attendancerecords'
    MOST_EVENTS          = 'results/mostevents'
    LARGEST_CLUBS        = 'results/largestclubs'
    HUNDRED_CLUBBERS     = 'results/100clubbers'
    NOT_PARKRUN          = 'results/notparkrun'
    FREEDOM_RUNNERS      = 'results/freedom'
    MOST_FIRST_FINISHES  = 'results/mostfirstfinishes'
    FIRST_FINISHES       = 'results/firstfinishers'
    SUB_SEVENTEEN        = 'results/sub17'
    TOP_AGE_GRADE        = 'results/topagegrade'
    NEW_CATEGORY_RECORDS = 'results/newcategoryrecords'
    COURSE_RECORDS       = 'results/courserecords'
    

    def __init__(self, name) -> None:

        self.pr   = parkrun.Parkrun()
        self.name = name \
                    if name in self.pr.countries \
                    else difflib.get_close_matches(name, self.pr.countries)[0]
        
        self.info = self.pr.countries_dict[self.name]['info']
        self.url  = self.pr.countries_dict[self.name]['url']

        pass

    def get_attendance_records(self):
        try:
            url = f"{self.url}{Country.ATTENDANCE_RECORDS}"
            # Get table data
            df = get_html_tables(url)

            # Drop unnamed column
            df = df.drop(df.columns[1], axis=1)
        except Exception as e:
            print(f"ERROR: {e}")
        return df
    
    def get_most_events(self):
        url = f"{self.url}{Country.MOST_EVENTS}"
        df = get_html_tables(url)
        return df
    
    def get_largest_clubs(self):
        url = f"{self.url}{Country.LARGEST_CLUBS}"
        df = get_html_tables(url)
        return df
    
    def get_not_parkrunners(self):
        url = f"{self.url}{Country.NOT_PARKRUN}"
        df = get_html_tables(url)
        return df
    
    def get_freedom_runners(self):
        url = f"{self.url}{Country.FREEDOM_RUNNERS}"
        df = get_html_tables(url)
        return df
    
    def get_most_first_finishers(self):
        url = f"{self.url}{Country.MOST_FIRST_FINISHES}"
        df = get_html_tables(url)
        return df
    
    def get_first_finishes(self):
        url = f"{self.url}{Country.FIRST_FINISHES}"
        df = get_html_tables(url)
        return df
    
    def get_sub_seventeen_runners(self):
        url = f"{self.url}{Country.SUB_SEVENTEEN}"
        df = get_html_tables(url)
        return df
    
    def get_top_age_grade(self):
        url = f"{self.url}{Country.TOP_AGE_GRADE}"
        df = get_html_tables(url)
        return df
    
    def get_new_category_records(self):
        url = f"{self.url}{Country.NEW_CATEGORY_RECORDS}"
        df = get_html_tables(url)
        return df
    
    def get_cource_records(self):
        url = f"{self.url}{Country.COURSE_RECORDS}"
        df = get_html_tables(url)
        return df



    
    
    pass
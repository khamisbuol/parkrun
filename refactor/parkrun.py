import pandas as pd
import scrape
import transform

class Parkrun:
    
    COUNTRIES_URL           = 'https://www.parkrun.com/countries/'
    FIRST_FINISHERS_URL     = 'https://www.parkrun.com/results/firstfinishers/'
    # NEW_AGE_CATEGORY_URL    = 'https://www.parkrun.com/results/newcategoryrecords/'
    SUB_SEVENTEEN_URL       = 'https://www.parkrun.com/results/sub17/'
    TOP_AGE_GRADE_URL       = 'https://www.parkrun.com/results/topagegrade/'
    NEW_CAT_RECORDS_URL     = 'https://www.parkrun.com/results/newcatrecords/'
    COURSE_RECORDS_URL      = 'https://www.parkrun.com/results/courserecords/'
    FREEDOM_URL             = 'https://www.parkrun.com/results/freedom/'
    ATTENDACE_RECORDS_URL   = 'https://www.parkrun.com/results/attendancerecords/'
    MOST_EVENTS_URL         = 'https://www.parkrun.com/results/mostevents/'
    MOST_FIRST_FINISHES_URL = 'https://www.parkrun.com/results/mostfirstfinishes/'
    LARGEST_CLUBS_URL       = 'https://www.parkrun.com/results/largestclubs/'

    def __init__(self):

        self.countries = scrape.get_countries()
        pass
    
    def get_first_finishers(self) -> pd.DataFrame:
        url = Parkrun.FIRST_FINISHERS_URL
        df  = transform.get_first_finishers(url)
        return df
    
    def get_sub_seventeen_runners(self) -> pd.DataFrame:
        url = Parkrun.SUB_SEVENTEEN_URL
        df  = transform.get_sub_seventeen_runners(url)
        return df
    
    def get_top_age_grade(self) -> pd.DataFrame:
        url = Parkrun.TOP_AGE_GRADE_URL
        df  = transform.get_top_age_grade(url)
        return df
    
    def get_new_category_records(self) -> pd.DataFrame:
        url = Parkrun.NEW_CAT_RECORDS_URL
        df  = transform.get_new_category_records(url) 
        return df

    def get_course_records(self) -> pd.DataFrame:
        url = Parkrun.COURSE_RECORDS_URL
        df  = transform.get_course_records(url) 
        return df
    
    def get_freedom_finishers(self) -> pd.DataFrame:
        url = Parkrun.FREEDOM_URL
        df  = transform.get_freedom_finishers(url)
        return df
    
    def get_attendance_records(self) -> pd.DataFrame:
        url = Parkrun.ATTENDACE_RECORDS_URL
        df  = transform.get_attendance_records(url)
        return df
    
    def get_most_events_attended(self) -> pd.DataFrame:
        url = Parkrun.MOST_EVENTS_URL
        df  = transform.get_most_events_attended(url)
        return df
    
    def get_most_first_finishes(self) -> pd.DataFrame:
        url = Parkrun.MOST_FIRST_FINISHES_URL
        df  = transform.get_most_first_finishes(url)
        return df
    
    def get_largest_clubs(self) -> pd.DataFrame:
        url = Parkrun.LARGEST_CLUBS_URL
        df  = transform.get_largest_clubs(url)
        return df

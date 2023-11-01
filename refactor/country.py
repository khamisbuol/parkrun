import scrape as gd
import transform

class Country:

    ATTENDANCE_RECORDS   = 'results/attendancerecords'
    MOST_EVENTS          = 'results/mostevents'
    LARGEST_CLUBS        = 'results/largestclubs'
    HUNDRED_CLUBBERS     = 'results/100clubbers'
    NOT_PARKRUN          = 'results/notparkrun'
    FREEDOM_FINISHERS    = 'results/freedom'
    MOST_FIRST_FINISHES  = 'results/mostfirstfinishes'
    FIRST_FINISHERS      = 'results/firstfinishers'
    SUB_SEVENTEEN        = 'results/sub17'
    TOP_AGE_GRADE        = 'results/topagegrade'
    NEW_CATEGORY_RECORDS = 'results/newcategoryrecords'
    COURSE_RECORDS       = 'results/courserecords'    

    def __init__(self, name) -> None:
        self.name = name
        self.url, \
        self.info = gd.get_country_details(name)

        # self.locations = get_locations(name) # To be used for retrieving all country data

        pass

    # def get_locations(self):
    #     url = f"{self.url}{Country.ATTENDANCE_RECORDS}"
    #         # Get table data
    #     df = gd.get_html_table(url)

    #     return df
    
    def get_attendance_records(self):

        url = f'{self.url}{Country.ATTENDANCE_RECORDS}'
        df  = transform.get_attendance_records(url)
        return df
    
    def get_most_events_attended(self):
        url = f'{self.url}{Country.MOST_EVENTS}'
        df  = transform.get_most_events_attended(url)
        return df
    
    def get_largest_clubs(self):
        url = f'{self.url}{Country.LARGEST_CLUBS}'
        df  = transform.get_largest_clubs(url)
        return df
    
    def get_freedom_finishers(self):
        '''
        This was initially for during covid, and in limited countries. No longer
        available in some countries, and may soon get deprecated. 

        Unavailable in Japan for example

        '''
        url = f'{self.url}{Country.FREEDOM_FINISHERS}'
        df  = transform.get_freedom_finishers(url)
        return df
    
    def get_most_first_finishes(self):
        url = f'{self.url}{Country.MOST_FIRST_FINISHES}'
        df  = transform.get_most_first_finishes(url)
        return df
    
    def get_first_finishers(self):
        url = f'{self.url}{Country.FIRST_FINISHERS}'
        df  = transform.get_first_finishers(url)
        return df
    
    def get_sub_seventeen_runners(self):
        url = f'{self.url}{Country.SUB_SEVENTEEN}'
        df  = transform.get_sub_seventeen_runners(url)
        return df
    
    def get_top_age_grade(self):
        url = f'{self.url}{Country.TOP_AGE_GRADE}'
        df  = transform.get_top_age_grade(url)

        return df
    
    def get_new_category_records(self):
        url = f'{self.url}{Country.NEW_CATEGORY_RECORDS}'
        df  = transform.get_new_category_records(url)
        return df
    
    def get_course_records(self):
        url = f'{self.url}{Country.COURSE_RECORDS}'
        df  = transform.get_course_records(url)
        return df
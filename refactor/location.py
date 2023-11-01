import transform
from scrape import get_location_url


class Location:


    LATEST_RESULTS        = 'latestresults'
    EVENT_HISTORY         = 'eventhistory'
    CLUB_LIST             = 'clublist'
    NOT_PARKRUN           = 'notparkrun'
    NOT_PARKRUN_HISTORY   = 'notparkrunhistory'
    MOST_FIRST_FINISHES   = 'firstfinishescount'
    AGE_CATEGORY_RECORDS  = 'agecategoryrecords'
    SUB_TWENTY_WOMEN      = 'sub20women'
    SUB_SEVENTEEN_MEN     = 'sub17'
    AGE_GRADE_LEADERBOARD = 'agegradedleague'
    FASTEST_FIVEHUNDRED   = 'fastest500'

    def __init__(self, country, name):
        self.country = country
        self.name = name
        self.url = get_location_url(country, name)
        pass

    def get_latest_results(self):
        url = f'{self.url}/{Location.LATEST_RESULTS}'
        df  = transform.get_latest_results(url)
        return df

    pass
import requests
import sys
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Event:

    #
    # Attributes of an event:
    # - has a country
    # - has a location
    # - has an event number
    #
    #

    #
    # - 
    #

    #
    # Static variables
    #
    USER_AGENT         = "Chrome/43.0.2357"
    LATEST_RESULTS     = "latest_results"
    ATTENDANCE_RECORDS = "attendance_records"
    EVENT_HISTORY      = "event_history"
    SINGLE_EVENT       = "single_event"

    def __init__(self, country: str, location: str, event_no: str = None) -> None:
        self.country  = country
        self.location = location
        self.event_no = event_no
        


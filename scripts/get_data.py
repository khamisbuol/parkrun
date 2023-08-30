import pandas as pd
import requests
import get_template_data as gtd
import numpy as np
import validate

parkrun_events_data = gtd.parkrun_events_data
countries_data = gtd.countries_data

# countries_list = countries_data.keys()

LATEST_RESULTS="latest_results"
ATTENDANCE_RECORDS="attendance_records"
EVENT_HISTORY="event_history"
SINGLE_EVENT="single_event"

def get_html_contents(url):
    """
    This function is used to fetch html content from a given url
    """
    if validate.url_exists(url):
        response = requests.get(url)
        tables = pd.read_html(response.content)
        return tables
    return None

def modify_parkrun_template_url(event_type, 
                                template_url, 
                                country_url, 
                                location, 
                                event_no):
    """
    This function modifies a given parkrun template url based on some certain
    parameters.
    -   event_type:     E.g., attendance_records, event_history
    -   template_url:   The url template we want to modify
    -   country_url:    I.e., the base_url component for individual countries. 
                        For example, parkrun.com.au
    -   location:       The location of a particular parkrun. E.g., parkville
    -   event_no:       The parkrun event number. For example, 123
    """
    modified_url = None
    if event_type == ATTENDANCE_RECORDS:
        modified_url = template_url.replace(
                    "BASE_URL", country_url)
    if event_type == LATEST_RESULTS or event_type == EVENT_HISTORY:
        modified_url = template_url.replace(
                    "BASE_URL", country_url).replace(
                    "LOCATION", location)
    if event_type == SINGLE_EVENT:
        modified_url = template_url.replace(
                    "BASE_URL", country_url).replace(
                    "LOCATION", location).replace(
                    "EVENT_NO", event_no)
    return modified_url



def get_html_tables(event_type, country, location, event_no):
    template_url = gtd.get_parkrun_url_template(event_type)
    country_url = gtd.get_country_url(country)

    modified_url = None

    match event_type:
        case "attendance_records":
            modified_url = modify_parkrun_template_url(ATTENDANCE_RECORDS,
                                                       template_url,
                                                       country_url)
        case "latest_results":
            modified_url = modify_parkrun_template_url(LATEST_RESULTS,
                                                       template_url,
                                                       country_url)
        case "event_history":
            modified_url = modify_parkrun_template_url(EVENT_HISTORY, 
                                                       template_url, 
                                                       country_url, 
                                                       location)
        case "single_event":
            modified_url = modify_parkrun_template_url(SINGLE_EVENT, 
                                                       template_url, 
                                                       country_url, 
                                                       location,
                                                       event_no)
        case _:
            modified_url = None

    #
    # Validate that modified url is valid, then get html tables
    #
    if validate.url_exists(modified_url):
        response = requests.get(modified_url)
        html_tables = pd.read_html(response.content)
        return html_tables
    return None



def get_attendance_records(country):
    # template_url = gtd.get_parkrun_url_template(ATTENDANCE_RECORDS)
    # country_url = gtd.get_country_url(country)

    # attendance_records_url = modify_parkrun_template_url(ATTENDANCE_RECORDS,
    #                                                      template_url,
    #                                                      country_url)
    
    #
    # TODO: Get HTML contents
    #       Return multiple HTML tables from attendance records page
    #
    # html_tables = get_html_contents(attendance_records_url)
    html_tables = get_html_tables(ATTENDANCE_RECORDS,
                                  country)

    return

#
# Get list of locations of a particular country
#
def get_locations_of_country(country):
    """
    We can use the EVENT table table returned by get_attendance_records to
    get locations of a given country. This is because the attendance records
    webpage contains results from all parkrun locartions for a country. 

    """
    #
    # TODO: Return events column outputted by get_attendance_records function
    #
    
    return


get_locations_of_country("Australia")


def get_latest_results_one(country, location):
    # template_url = gtd.get_parkrun_url_template(LATEST_RESULTS)
    # country_url = gtd.get_country_url(country)

    # latest_results_url = modify_parkrun_template_url(LATEST_RESULTS, 
    #                                                  template_url, 
    #                                                  country_url, 
    #                                                  location)
    
    #
    # TODO: Get HTML contents
    #       Return pandas dataframe
    #
    html_tables = get_html_tables(LATEST_RESULTS,
                                  country,
                                  location)

    return


#
# Get latest results for event data (and for all countries and locations)
#
def get_latest_results_all():

    #
    # TODO: Implement correct output pandas dataframe
    #
    latest_results_all = pd.array

    for country in countries_data.keys():
        # locations = get_locations_of_country(country)
        for location in get_locations_of_country(country):
            latest_results = get_latest_results_one(country, location)

            #
            # TODO: Append to all results
            #
            latest_results_all.add(latest_results)
    return latest_results_all

#
# Get event history (i.e., all the parkrun data) of a particular event
#
def get_event_history_summary(country, location):
    # template_url = gtd.get_parkrun_url_template(EVENT_HISTORY)
    # country_url  = gtd.get_country_url(country)

    # event_history_url = modify_parkrun_template_url(EVENT_HISTORY, 
    #                                                 template_url, 
    #                                                 country_url, 
    #                                                 location)
    
    #
    # TODO: Retrieve webpage content
    #       IMPORTANT, need to ensure event_no is returned so it can be used
    #       by the get_event_history
    #
    # html_tables = get_html_contents(event_history_url)
    html_tables = get_html_tables(EVENT_HISTORY,
                                  country,
                                  location)

    #
    # TODO: Return list of event numbers
    #
    event_numbers = None

    return

#
# Get event parkrun data of a particular location given an event number
#
def get_event_history_one(country, location, event_no):
    # template_url = gtd.get_parkrun_url_template(SINGLE_EVENT)
    # country_url  = gtd.get_country_url(country)

    # single_event_url = modify_parkrun_template_url(SINGLE_EVENT, 
    #                                                template_url, 
    #                                                country_url, 
    #                                                location,
    #                                                event_no)
    #
    # TODO: Retrieve webpage content
    #
    # html_tables = get_html_contents(single_event_url)
    html_tables = get_html_tables(SINGLE_EVENT,
                                  country,
                                  location,
                                  event_no)

    return

#
# Get all event histories for a particular location
#
def get_event_history_all():
    
    for country in countries_data.keys():
        for location in get_locations_of_country(country):
            event_no = None # TODO
            event_history = get_event_history_one(country, location, event_no)



            return

    #
    # TODO: use the event_no column returned by get_event_history_summary
    #       function. 
    #

    return


###############################################################################
#           TODO: Might put into its own module as a parkrunner object differs
#                 from parkrun object. 
###############################################################################
#
# Get parkrunner summary results
#
def get_parkrunner_summary(country, runner_id):
    # TODO
    return

#
# Get all the data of a particular parkrunner
#
def get_parkrunner_all_results(country, runner_id):
    # TODO
    return

#
# Get all the locations a particular runner has run in
#
def get_parkrunner_location_results(country, runner_id):
    # TODO
    return


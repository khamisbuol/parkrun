import pandas as pd
import requests
import get_template_data as gtd
import numpy as np
import validate
from bs4 import BeautifulSoup
import re

parkrun_events_data: dict = gtd.parkrun_events_data
countries_data: dict = gtd.countries_data

LATEST_RESULTS = "latest_results"
ATTENDANCE_RECORDS = "attendance_records"
EVENT_HISTORY = "event_history"
SINGLE_EVENT = "single_event"

latest_results_columns: list = ["Position", "Parkrunner",
                                "Gender", "Age", "Group", "Club", "Time"]

detailed_latest_results_columns: list = ["Position", "Parkrunner", "No. Parkruns",
                                         "Gender", "Gender Position", "Age Group",
                                         "Age Grade", "Club", "Time", "PB/FT?"]


def clean_name(s):
    # Extract parts using regular expressions
    match = re.match(r"^(.*?) (.*?)(\d+)(.*?) \|", s)
    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        no_parkruns = match.group(3) + match.group(4)
        cleaned_string = f"{first_name} {last_name} {no_parkruns}"
        return cleaned_string
    else:
        return s


def split_name(s):
    # Extract parts using regular expressions
    match = re.match(r"^(.*?) (.*?)(\d+)(.*?) \|", s)
    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        no_parkruns = f"{match.group(3)} {match.group(4)}"
        return pd.Series({
            "parkrunner": f"{first_name} {last_name}",
            "no_parkruns": no_parkruns
        })
    else:
        return pd.Series({
            "parkrunner": "",
            "no_parkruns": ""
        })


def split_gender(s):
    match = re.match(r"^(.*?) (\d+)$", s)
    if match:
        gender = match.group(1)
        gender_position = match.group(2)
        # print(f"gender: {gender}, gender_position: {gender_position}")
        return pd.Series({
            "gender": gender,
            "gender pos": gender_position
        })
    else:
        return pd.Series({
            "gender": "",
            "gender pos": ""
        })


def modify_parkrun_template_url(event_type: str,
                                template_url: str,
                                country_url: str = None,
                                location: str = None,
                                event_no: str = None) -> str:
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


def get_html_tables(event_type: str,
                    country: str = None,
                    location: str = None,
                    event_no: str = None) -> list:

    template_url = gtd.get_parkrun_url_template(event_type)
    country_url = gtd.get_country_url(country)

    match event_type:
        case "attendance_records":
            modified_url = modify_parkrun_template_url(ATTENDANCE_RECORDS,
                                                       template_url,
                                                       country_url,)
        case "latest_results":
            modified_url = modify_parkrun_template_url(LATEST_RESULTS,
                                                       template_url,
                                                       country_url,
                                                       location)
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

    # Validate that modified url is valid, then get html tables
    if validate.url_exists(modified_url) and validate.element_not_null(modified_url):

        response = requests.get(
            modified_url, headers={'user-agent': 'Chrome/43.0.2357'})

        html_tables = pd.read_html(response.content)
        print(f"MODIFIED_URL:{modified_url}")

    return html_tables


def get_attendance_records(country: str) -> pd.DataFrame:
    """
    Retreieve attendance records of a given country. This will call the
    get_html_tables() function.

    Args:
        country (string):   A string value of a valid country. Note this gets
                            capitalised. E.g., uNited Kingdom becomes United
                            Kingdom. 
    Returns:
        Pandas dataframe:   A dataframe containing attendance records of the
                            given country. 
    """

    # Get html tables
    html_tables = get_html_tables(ATTENDANCE_RECORDS, country)

    # Verify there are tables and that there's only one of them returned
    if validate.element_not_null(html_tables) and len(html_tables) == 1:

        # Get the only html table that should have been processed
        df = html_tables[0]

        # Remove any 'Unnamed' columns and any duplicate rows
        attendance_records_df = df.loc[:, ~df.columns.str.startswith(
            "Unnamed:")].drop_duplicates()

    return attendance_records_df


def get_locations_of_country(country: str) -> list:
    """
    Retrieve all the locations of a given country that have parkruns. 

    Args:
        country (string):   A string value of a valid country.

    Returns:
        list:               A list of locations that host parkruns for the
                            given country. 
    """

    # Get attendance records dataframe
    country_attendance_records = get_attendance_records(country)

    # Convert the Event column into a list
    list_of_locations = country_attendance_records["Event"].values.tolist()

    return list_of_locations


def get_latest_results_location(country: str, location: str) -> pd.DataFrame:
    """
    Retrieve the latest parkrun results, given a country and location

    Args:
        country (string):   A string value of a valid country. E.g., United Kingdom
        location (string):  A valid location. E.g., Aberdeen

    Returns:
        Pandas dataframe:   Dataframe containing lates results of the given location. 
    """

    # Get html tables
    html_tables = get_html_tables(LATEST_RESULTS, country, location)

    # Verify there are tables and that only one of them is returned
    if validate.element_not_null(html_tables) and len(html_tables) == 1:
        df = html_tables[0]
        # 6 indexes returned
        # print(df.iloc[:, 0].head())  # Position (Clean)

        # Parkrunner, No. Parkruns: rest redundant Gender, Gender Position
        # print(df.iloc[:, 1].head(15))

        # df[["parkrunner", "no_parkruns"]
        #    ] = df["parkrunner"].apply(split_name)

        df[["gender", "gender pos"]
           ] = df["Gender"].apply(split_gender)

        print(df.head(15))

        # print(df.iloc[:, 2].head(15))  # Gender, Gender Position (Semi-clean)
        # print(df.iloc[:, 3].head(15))  # Age Group, Age Grade (Semi-clean)
        # print(df.iloc[:, 4].head(15))  # Club (Clean)
        # Time, PB/FT (Semi-clean): char(1-5) = time
        # print(df.iloc[:, 5].head(15))
        #

    return


get_latest_results_location("Australia", "tuggeranong")


def get_latest_results_country(country: str) -> pd.DataFrame:
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
        for location in get_locations_of_country(country):
            latest_results = get_latest_results_location(country, location)

            #
            # TODO: Append to all results
            #
            latest_results_all.add(latest_results)
    return latest_results_all

#
# Get event history (i.e., all the parkrun data) of a particular event
#


def get_event_history_summary(country, location):

    #
    # TODO: Retrieve webpage content
    #       IMPORTANT, need to ensure event_no is returned so it can be used
    #       by the get_event_history
    #
    html_tables = get_html_tables(EVENT_HISTORY, country, location)

    #
    # TODO: Return list of event numbers
    #
    event_numbers = None

    return

#
# Get event parkrun data of a particular location given an event number
#


def get_event_history_one(country, location, event_no):
    #
    # TODO: Retrieve webpage content
    #
    html_tables = get_html_tables(SINGLE_EVENT, country, location, event_no)

    return

#
# Get all event histories for a particular location
#


def get_event_history_all():

    for country in countries_data.keys():
        for location in get_locations_of_country(country):
            event_no = None  # TODO
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

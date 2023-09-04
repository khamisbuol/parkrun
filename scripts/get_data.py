import pandas as pd
import requests
import get_template_data as gtd
import transform_data as td
import validate

# from bs4 import BeautifulSoup

parkrun_events_data: dict = gtd.parkrun_events_data
countries_data: dict = gtd.countries_data

LATEST_RESULTS = "latest_results"
ATTENDANCE_RECORDS = "attendance_records"
EVENT_HISTORY = "event_history"
SINGLE_EVENT = "single_event"


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

    # print(
    #     f"ARGS: event_type: {event_type}, country: {country}, location: {location}\n")
    # print(
    #     f"TEMP: template_url: {template_url}, country_url: {country_url}, modified_url: {modified_url}")

    # Validate that modified url is valid, then get html tables
    if validate.url_exists(modified_url) and validate.element_not_null(modified_url):

        response = requests.get(
            modified_url, headers={'user-agent': 'Chrome/43.0.2357'})

        html_tables = pd.read_html(response.content)
        # print(f"MODIFIED_URL:{modified_url}")

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
    list_of_locations = country_attendance_records.iloc[:, 0].values.tolist()

    return list_of_locations


def get_latest_results_location(country: str,
                                location: str,
                                detailed: bool = False
                                ) -> pd.DataFrame:
    """
    Retrieve the latest parkrun results, given a country and location

    Args:
        country (string):   A string value of a valid country. E.g., United Kingdom
        location (string):  A valid location. E.g., Aberdeen
        detailed (Boolean): A boolean condition that if true returns detailed results

    Returns:
        Pandas dataframe:   Dataframe containing latest results of the given location. 
    """

    # location = td.transform_location(location)

    # Get html tables
    html_tables = get_html_tables(LATEST_RESULTS, country, location)

    # Verify there are tables and that only one of them is returned
    if validate.element_not_null(html_tables) and len(html_tables) == 1:
        df = html_tables[0]

        # Transform data of latest results
        df = td.transform_latest_results(df, detailed)

        # Add location column
        df["Location"] = location

    return df


# latest_results = get_latest_results_location("Canada", "averybeach", True)
# print(latest_results.head())


def get_latest_results_country(country: str,  detailed: bool = False) -> pd.DataFrame:
    latest_results_country: list = []
    list_of_locations = get_locations_of_country(country)
    for location in list_of_locations:
        try:
            location = td.transform_location(location)
            latest_location_results = get_latest_results_location(
                country, location, detailed)
            latest_results_country.append(latest_location_results)
        except:
            print(
                f"ERROR: Could not get latest results for {country}, {location}.")

        latest_results = pd.concat(latest_results_country)

        # Add country column to dataframe
        latest_results["Country"] = country
        latest_results = latest_results.reset_index(drop=True)
    return latest_results


# austria_results = get_latest_results_country("Austria")
# austria_results.to_csv("austria.csv")

australia_results = get_latest_results_country("Australia")
australia_results.to_csv("australia.csv")

#
# Get latest results for event data (and for all countries and locations)
#


def get_latest_results_all(detailed: bool = False):

    latest_results_all: list = []

    for country in countries_data.keys():
        for location in get_locations_of_country(country):
            latest_results = get_latest_results_location(
                country, location, detailed)
            latest_results_all.append(latest_results)
    latest_global_results = pd.concat(latest_results_all)
    latest_global_results = latest_global_results.reset_index(drop=True)
    return latest_global_results


def get_event_history_summary(country: str, location: str):
    """
    Retrieve event history summary, given a country and location

    Args:
        country (string):   A string value of a valid country. E.g., United Kingdom
        location (string):  A valid location. E.g., Aberdeen

    Returns:
        Pandas dataframe:   Dataframe containing event history of the given location. 
    """
    #
    # TODO: Retrieve webpage content
    #       IMPORTANT, need to ensure event_no is returned so it can be used
    #       by the get_event_history
    #
    html_tables = get_html_tables(EVENT_HISTORY, country, location)

    # Verify there are tables and that only one of them is returned
    if validate.element_not_null(html_tables) and len(html_tables) == 1:
        df = html_tables[0]

        '''
        Output data frame needs to have the following columns:
            - Event No.
            - Date
            - No. Finishers
            - No. Volunteers
            - First Male Finisher
            - First Male Finisher Time
            - First Female Finisher
            - First Female Finisher Time
        '''
    #
    # TODO: Return list of event numbers
    #
    event_numbers = None

    return df

#
# Get event parkrun data of a particular location given an event number
#


def get_event_history_one(country: str, location: str, event_no: int) -> pd.DataFrame:
    #
    # TODO: Retrieve webpage content
    #
    html_tables = get_html_tables(SINGLE_EVENT, country, location, event_no)

    # Verify there are tables and that only one of them is returned
    if validate.element_not_null(html_tables) and len(html_tables) == 1:
        df = html_tables[0]

        '''
        Output data frame needs to have the following columns:
            - Position.
            - Gender
            - Age Group
            - Club
            - Time
            - PB/FT?
        '''

    return df

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

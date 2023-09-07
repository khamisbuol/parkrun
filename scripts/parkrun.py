# import get_template_data as gtd
import read_files as rf
import requests
import validate
import pandas as pd
import transform_data as td


class Parkrun:

    USER_AGENT = "Chrome/43.0.2357"

    LATEST_RESULTS = "latest_results"
    ATTENDANCE_RECORDS = "attendance_records"
    EVENT_HISTORY = "event_history"
    SINGLE_EVENT = "single_event"

    # countries = rf.countries_data
    # parkruns = rf.parkrun_events_data

    def __init__(self, country: str,
                 location: str = None, event_no: str = None) -> None:

        # self.event_type = event_type
        self.country = country
        self.location = location
        self.event_no = event_no

        self.country_url = rf.get_country_url(country)
        self.country_info = rf.get_country_info(country)
        # self.event_info = rf.get_parkrun_event_info(event_type)
        # self.url_template = rf.get_parkrun_url_template(event_type)

        # Set parkrun locations
        self.locations = self.get_attendance_records(
        ).iloc[:, 0].unique().tolist()

    def modify_url_template(self, event_type: str) -> str:
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
        url_template = rf.get_parkrun_url_template(event_type)
        url_location = td.transform_location(self.location)

        match event_type:
            case "attendance_records":
                modified_url = url_template.replace(
                    "BASE_URL", self.country_url)
            case "latest_results" | "event_history":
                modified_url = url_template.replace(
                    "BASE_URL", self.country_url).replace(
                    "LOCATION", url_location)
            case "single_event":
                modified_url = url_template.replace(
                    "BASE_URL", self.country_url).replace(
                    "LOCATION", url_location).replace(
                    "EVENT_NO", self.event_no)
            case _:
                modified_url = None
        return modified_url

    def get_html_tables(self, event_type: str):
        webpage_url = self.modify_url_template(event_type)
        print(f"Webpage url: {webpage_url}")
        response = requests.get(webpage_url, headers={
                                'user-agent': self.USER_AGENT})
        if response != None and response.status_code == 200:
            html_tables = pd.read_html(response.content)

            if html_tables != None and len(html_tables) == 1:
                df = html_tables[0]
            else:
                raise f"ERROR: Could not retreive data for country={self.country} with url={self.country_url}"
        else:
            raise f"ERROR: Could not to get data for country={self.country} with url={webpage_url}. Response code = {response.status_code}"

        if not df.empty:
            return df
        else:
            raise f"ERROR: Data returned is empty for country={self.country}"

    def get_attendance_records(self) -> pd.DataFrame:
        """
        Retreieve attendance records of a country object. 

        Returns:
            Pandas dataframe:   A dataframe containing attendance records of the
                                given country. 
        """
        # Get html tables
        df = self.get_html_tables(self.ATTENDANCE_RECORDS)

        # Remove any 'Unnamed' columns
        attendance_records = df.loc[:, ~df.columns.str.startswith(
            "Unnamed:")]
        if not attendance_records.empty:
            return attendance_records
        else:
            raise f"ERROR: Attendance record is empty for country={self.country}"

    def get_latest_results_location(self, detailed=False):
        print(f"Getting latest results for location={self.location}")
        """
        Retrieve the latest parkrun results, given a location

        Args:
            parkrun (Parkrun):  A parkrun object with valid event type
            detailed (Boolean): A boolean condition that if true returns detailed results

        Returns:
            Pandas dataframe:   Dataframe containing latest results of the given location. 
        """
        df = self.get_html_tables(self.LATEST_RESULTS)

        df = td.transform_latest_results(df, detailed)

        # Add location column
        df["Location"] = self.location

        return df

    def get_latest_results_country(self, detailed=False):
        print(f"Getting latest results for country={self.country}")
        latest_results_country: list = []
        for location in self.locations:
            print(f"location={location}")
            self.location = location
            try:
                latest_location_results = self.get_latest_results_location(
                    detailed)
                latest_results_country.append(latest_location_results)
            except:
                print(
                    f"ERROR: Could not get latest results for {self.country}, {location}.")

            latest_results = pd.concat(latest_results_country)

            # Add country column to dataframe
            latest_results["Country"] = self.country
            latest_results = latest_results.reset_index(drop=True)
        return latest_results

    def get_event_history_summary(self, country: str = None, location: str = None):
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
        df = self.get_html_tables(self.EVENT_HISTORY)

        '''
        Output data frame needs to have the following columns:
            - Event No. VALID as 'Event ##'
            - Date INVALID, contains date, finisher, their times etc (just take date from this)
            - No. Finishers (can retrieve from Date/First Finishers column)
            - No. Volunteers (Can retreive from "Finishers" column)
            - First Male Finisher (Volunteers column)
            - First Male Finisher Time (can retreive from 'Male First Finisher' column)
            - First Female Finisher
            - First Female Finisher Time (can retreive from Female First Finisher column)
        '''
        df = td.transform_event_summary_data(df)

        # print(df.iloc[2].head())
        #
        # TODO: Return list of event numbers
        #
        event_numbers = None

        return
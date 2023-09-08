import get_template_data as gtd
import requests
import validate
import pandas as pd


class Country:

    URL_TEMPLATE = "BASE_URL/results/attendancerecords"
    USER_AGENT = "Chrome/43.0.2357"

    def __init__(self, name: str) -> None:
        self.name = name

        self.url = gtd.get_country_url(self.name)
        self.info = gtd.get_country_info(self.name)

        self.attendace_records_url = self.URL_TEMPLATE.replace(
            "BASE_URL", self.url)

        # Set parkrun locations
        self.attendance_records = self.get_attendance_records()
        self.locations = self.attendance_records.iloc[:, 0].unique().tolist()

    def __get_attendance_records(self) -> pd.DataFrame:
        """
        Retreieve attendance records of a country object. 

        Returns:
            Pandas dataframe:   A dataframe containing attendance records of the
                                given country. 
        """

        # Get response from URL
        response = requests.get(self.attendace_records_url, headers={
            'user-agent': self.USER_AGENT})
        if response != None and response.status_code == 200:
            html_tables = pd.read_html(response.content)

            if html_tables != None and len(html_tables) == 1:
                df = html_tables[0]
                # Remove any 'Unnamed' columns
                attendance_records = df.loc[:, ~df.columns.str.startswith(
                    "Unnamed:")]
            else:
                raise f"ERROR: Could not retreive data for country={self.name} with url={self.url}"
        else:
            raise f"ERROR: Could not to get parkrun locations for country={self.name}. Response code = {response.status_code}"

        if not attendance_records.empty:
            return attendance_records
        else:
            raise f"ERROR: Attendance record is empty for country={self.name}"

import requests
import sys
import re
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
import unicodedata
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#
# This can be a script that processes a URL to get data.
#
# Would likely need to import the translate module. 
#

HEADERS = {'user-agent': 'Chrome/43.0.2357'}
SUCCESS = 200

COUNTRIES_URL = 'https://www.parkrun.com/countries/'

def get_response(url: str) -> bytes:
    try:
        print(f"Getting data from url = {url}")
        # Run a request to the url
        response = requests.get(url, headers=HEADERS, verify=False)

        # Raise exceptions for invalid response
        if response.status_code != SUCCESS:
            raise ValueError(f"Invalid response.\n"\
                             f"Response code = {response.status_code}, URL = {url}")
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    return response

def get_html_tables(url: str) -> pd.DataFrame:
    try:
        # Get content from provided url
        response = get_response(url)
        
        # Parse content for any html tables
        html_tables = pd.read_html(response.content, keep_default_na=False)

        # Verify that table data exists and that there's only one
        if html_tables == None or len(html_tables) != 1:
            raise ValueError(f"No table data or multiple tables returned from url={url}.\n"\
                             f"Expected length = 1, Actual length = {len(html_tables)}")
        
        #
        # Each webpage often contains just a single table, so get just
        # the first and only table
        #
        df = html_tables[0]
        
        # Verify that the dataframe is not empty
        if not df.empty or df != None:

            # Capitalise column names
            df.rename(columns=lambda x: x.title(), inplace=True)

        else:
            raise ValueError(f"Dataframe generated from url = {url} is empty.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    return df


def get_html_table(url: str, get_id: bool = False) -> pd.DataFrame:
    try:
        data = []
        
        # Get response from url
        response = get_response(url)

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get table from url (first table)
        table = soup.find('table', {'class': ['results', 'sortable']})
        # table = soup.find('table') # Get (first table)
        # Verify that table data was able to be extracted
        if not table:
            raise ValueError("Unable to find table data for class = 'result'")
        
        # Extract all the column names from the url and decode the names
        columns = [unicodedata.normalize("NFKD", col.string) \
                   for col in table.find_all('th')]
        
        # Add an Id column
        columns[:0] = ['Id'] if get_id else []

        # Add rows to data, prepending id generated from url
        for tr in table.find_all('tr'):
            row_list = []
            for row in tr.find_all('td'):
                
                # print(f'ROW: {row}')
                if 'athleteNumber' in str(row):
                    id = row.a['href'].split('=')[-1]
                    row_list.append(id)
                
                val = row.text
                row_list.append(val)

                # Add url column (for locations)
                if 'results' in str(row):
                    row_list.append(row.a['href'])
            
            if all(value == '' for value in row_list):
                    continue
            
            data.append(row_list)
                    # print(f'DEBUG: {id}')
                # print(f'VAL: {val}')
            # Create a list for row data
            # row = [td.text for td in tr.find_all('td')]
            # a_tag = tr.a

            # # Skip if row contains blanks
            # if all(value == '' for value in row):
            #     continue

            # Add id if get_id and hyperlink tag exists in row
            # if get_id and a_tag:
            #     athlete_url = a_tag['href']
            #     athlete_id  = athlete_url.split('=')[-1]
            #     row[:0]     = [athlete_id]
            # data.append(row)
        
        df = pd.DataFrame(data)

         # Upper case each words in column names
        # df.rename(columns=lambda x: x.title(), inplace=True)
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    
    return df

def get_countries():
    df = get_html_table(COUNTRIES_URL)
    
    return

# url = 'https://www.parkrun.com/results/mostfirstfinishes/'
# url = 'https://www.parkrun.com/results/mostevents/'
# url = 'https://www.parkrun.com/results/attendancerecords/'
url = 'https://www.parkrun.com/results/firstfinishers/'

# print(get_html_table(url))
from   bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import difflib
import traceback
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#
# This can be a script that processes a URL to get data.
#
# Would likely need to import the translate module. 
#

HEADERS    = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
SUCCESS    = 200
NO_SERVICE = 503

COUNTRIES_URL = 'https://www.parkrun.com/countries/'

def get_response(url: str) -> bytes:
    try:
        print(f'Getting data from url = {url}')
        # Run a request to the url
        response = requests.get(url, headers=HEADERS, verify=False)

        if response.status_code == NO_SERVICE:
            raise ValueError(f'Service unavailable for url = {url}')

        # Raise exceptions for invalid response
        if response.status_code != SUCCESS:
            raise ValueError(f'Invalid response.\n'\
                             f'Response code = {response.status_code}, URL = {url}')
    
    except Exception as e:
        print(f'ERROR: {e}')
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
            raise ValueError(f'No table data or multiple tables returned from url={url}.\n'\
                             f'Expected length = 1, Actual length = {len(html_tables)}')
        
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
            raise ValueError(f'Dataframe generated from url = {url} is empty.')

    except Exception as e:
        traceback.print_exc() 
        sys.exit(1)
    return df


# def extract_athlete_info(url):
#     try:
#         url = 'https://www.parkrun.com.au/parkrunner/1114599'
#         response  = get_response(url)
#         soup      = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         print(paragraphs)

#         pattern = re.compile(r'[A-Za-z]+\d{2}-\d{2}|[A-Za-z]+\d{2}')
        
#         # Athlete age group
#         match = re.search(pattern, paragraphs)
#         matches = [re.search(pattern, paragraph) for paragraph in paragraphs if paragraph]
#         print(matches)
#         sys.exit()
        
#         if match:
#             pattern = re.compile(r'([A-Z]+)(\d{2}(?:-\d{2})?)')
#             age_group = str(match.group(0))

#             match = re.match(pattern, age_group)
#             if match:
#                 gender = match.group(1)
#                 if gender or gender == '':
#                     # Extract the last field
#                     gender = gender[-1]
#                     gender = 'Male' if gender == 'M' else 'Female'
#                 else:
#                     gender = 'Unknown'
#                 age_range = match.group(2)
#                 print(f'gender: {gender}, age_range: {gender}, age_group: {age_group}')
#                 return gender, age_range

#     except Exception as e:
#         traceback.print_exc() 
#         # print(f'extract_athlete_info() ERROR: {e}')


def get_html_table(url: str, locations=False) -> pd.DataFrame:
    try:
        data = []
        
        # Get response from url
        response = get_response(url)

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get table from url (first table)
        # table = soup.find('table', {'class': ['results', 'sortable']})
        table = soup.find('table')

        # Verify that table data was able to be extracted
        if not table:
            raise ValueError("Unable to find table data for "\
                             "class = 'result' or class = 'sortable'")

        # Add rows to data, prepending id generated from url
        for tr in table.find_all('tr'):
            row_list = []

            # Ignore the spacer column
            for table_data in tr.find_all('td', class_=lambda x: x != 'bspacer'):
                
                #
                # If data contains a link, process it. It may contain Athlete ID
                #
                if table_data.a:
                    data_url = table_data.a['href']
                    if 'athleteNumber' in str(data_url):
                        id = data_url.split('=')[-1]
                        row_list.append(id)
                    if 'parkrunner' in str(data_url):
                        id = data_url.split('/')[-1]
                        row_list.append(id)

                    # Add url column (for locations)
                    if locations and str(data_url).split('/')[-1] == 'results':
                        row_list.append(data_url)
                
                # Add literal text value to the row
                val = table_data.text
                row_list.append(val)
            
            #
            # Do not add any blank rows
            #
            if all(val == '' for val in row_list):
                    continue
            
            data.append(row_list)
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f'get_html_table() ERROR: {e}')
        traceback.print_exc() 
        sys.exit(1)

def get_country_details(name):
    # Get countries 
    countries      = get_countries()
    countries_list = list(countries.keys())

    # Assign country name to closest match (if possible)
    c_name = name \
        if name in countries_list \
        else difflib.get_close_matches(name, countries_list)[0]
    
    if not c_name:
        raise KeyError(f'Unable to find {name} in {countries}')
    
    info = countries[c_name]['info']
    url  = countries[c_name]['url']

    if not url:
            raise KeyError(f'Unable to find url for {name} in {countries}')
    # if not info:
    #         raise KeyError(f'Unable to find info for {name} in {countries}')
    
    # Add a forward slash if it's not at the end the generated url
    if url[-1] != '/':
        url = f'{url}/'
    
    return url, info

def get_locations(country):
    try:
        url, _ = get_country_details(country)
        
        atttendance_records_url = f'{url}results/attendancerecords'

        #
        # Use attendance records to get names of locations and
        # transform dataframe to consist of just event names and urls
        #
        df = get_html_table(atttendance_records_url, True)

        df = df.iloc[:, :2]

        df.columns = ['events_url', 'event']

        # Create a dictionary of events and their urls
        locations = dict(zip(df['event'], df['events_url']))

    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)
    return locations

def get_location_url(country, name):
    locations = get_locations(country)
    location_list = list(locations.keys())
    l_name = name \
        if name in locations \
        else difflib.get_close_matches(name, location_list)[0]
    
    url = locations[l_name]
    return url

def get_countries():
    '''
    This function returns a dictionary of countries with their name, urls, and info
    '''
    try:

        response = get_response(COUNTRIES_URL)

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the divs with the class 'section-wrap'
        country_sections = soup.find_all('div', class_='section-wrap')
        countries = {}
        for country_section in country_sections:

            # Retrieve name, info and url from section
            name = country_section.h2.string
            info = country_section.p.string
            url  = country_section.a['href']

            # url =  f'{url}/' if url[-1] != '/' else url
            
            # Add info and url for each country to dictionary
            countries[name] = {'info': info, 'url': url}
    
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)
    
    return countries
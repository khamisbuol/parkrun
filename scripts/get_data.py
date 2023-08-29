from read_files import read_yaml_file
from os import path
import pandas as pd
import requests

base_path = path.dirname(__file__)
sources_path = path.abspath(path.join(base_path, "..", "sources"))
data_path = path.abspath(path.join(base_path, "..", "data"))

#
# YAML sources files
#
parkrun_events_data = read_yaml_file(sources_path, "parkruns.yaml")
countries_data = read_yaml_file(sources_path, "countries.yaml")

#
# Get list of locations of a particular country
#
def get_locations_of_country(country):

    #
    # Country exists, process data
    #
    if country in countries_data:
        pr_webpage = countries_data[country]["url"]

        #
        # Get HTML contents
        #
        return
    return


get_locations_of_country('Australia')

#
# Get latest results for event data (and for all events)
#

#
# Get event history (i.e., all the parkrun data) of a particular event
#

#
# Get event parkrun data of a particular location given an event number
#

#
# Get parkrunner summary results
#

#
# Get all the data of a particular parkrunner
#

#
# Get all the locations a particular runner has run in
#
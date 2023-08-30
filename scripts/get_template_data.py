from read_files import read_yaml_file
from os import path

base_path = path.dirname(__file__)
sources_path = path.abspath(path.join(base_path, "..", "sources"))
data_path = path.abspath(path.join(base_path, "..", "data"))

#
# YAML sources files
#
parkrun_events_data = read_yaml_file(sources_path, "parkruns.yaml")
countries_data = read_yaml_file(sources_path, "countries.yaml")

def get_country_url(country):
    if country in countries_data:
        return countries_data[country]['url']
    return None

def get_country_info(country):
    if country in countries_data:
        return countries_data[country]['info']
    return None

def get_parkrun_url_template(event_type):
    if event_type in parkrun_events_data:
        return parkrun_events_data[event_type]['template']
    return None

def get_parkrun_event_info(event_type):
    if event_type in parkrun_events_data:
        return parkrun_events_data[event_type]['info']
    return None

def get_parkrunner_template(result_type):
    if result_type in parkrun_events_data["parkrunner"]:
        match result_type:
            case "summary_results":
                return parkrun_events_data["parkrunner"][result_type]
            case "all_results":
                return parkrun_events_data["parkrunner"][result_type]
            case "location_results":
                return parkrun_events_data["parkrunner"][result_type]
            case _:
                return None
    return None


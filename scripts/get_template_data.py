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


def get_country_url(country: str) -> str:
    country = country.title()
    if country in countries_data:
        return countries_data[country]['url']
    return


def get_country_info(country: str) -> str:
    country = country.title()
    if country in countries_data:
        return countries_data[country]['info']
    return


def get_parkrun_url_template(event_type: str) -> str:
    event_type = event_type.lower()
    if event_type in parkrun_events_data:
        return parkrun_events_data[event_type]['template']
    return


def get_parkrun_event_info(event_type: str) -> str:
    event_type = event_type.lower()
    if event_type in parkrun_events_data:
        return parkrun_events_data[event_type]['info']
    return


def get_parkrunner_template(result_type: str) -> str:
    result_type = result_type.lower()
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
    return

from os import path
import yaml

#
# Paths
#
base_path = path.dirname(__file__)
sources_path = path.abspath(path.join(base_path, "..", "sources"))
data_path = path.abspath(path.join(base_path, "..", "data"))

def read_yaml_file(file_path, file_name):

    file_path = file_path.replace("\\", "/")
    yaml_file = file_path + "/" + file_name 

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    return data


parkrun_events_data = read_yaml_file(sources_path, "parkruns.yaml")
webpages_data = read_yaml_file(sources_path, "countries.yaml")

aus_url = webpages_data['Australia']['url']

latest_results = parkrun_events_data['latest_results']['template']

event_history = parkrun_events_data['event_history']['template']

single_event = parkrun_events_data['single_event']['template']

print("aus_url: {}\nlatest_results: {}".format(aus_url, latest_results))
print("event_history: {}\nsingle_event: {}".format(event_history, single_event))

tuggers_420 = single_event.replace("BASE_URL", 
                  aus_url).replace("LOCATION", 
            "tuggeranong").replace("EVENT_NO", "420")

print("tuggers_420: ", tuggers_420)
# print(parkrun_events_data.values())

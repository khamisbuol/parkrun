import event
import location
import parkrun
import parkrunner
import country
import requests

# tuggeranong = parkrun.Parkrun()

# pk_country = country.Country("Austria")

# print(pk_country.locations)
# print(pk_country.get_attendance_records())

count = "Austria"
loc = "Donaupark"
event_type = "latest_results"
event_no = "420"
# event_type = "latest_results"

# pr = parkrun.Parkrun(count, loc, event_no)
# print(pr.get_event_history_summary())
# print(pr.locations)

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
# url = "https://www.parkrun.co.at/results/attendancerecords"
# try:
#     response = requests.get(url, headers={
#                                     'user-agent': USER_AGENT})

#     print(response)
# except:
#     print(f"Could not connect to {url}")
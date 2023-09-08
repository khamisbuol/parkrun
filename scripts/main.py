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

count = "Australia"
loc = "Tuggeranong"
event_type = "latest_results"
event_no = "420"
# event_type = "latest_results"

pr = parkrun.Parkrun(count, loc, event_no)
print(pr.get_event_history_one())

# print(pr.locations)

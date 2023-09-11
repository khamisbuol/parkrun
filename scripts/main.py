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

count = "Denmark"
loc = "Brabrand"
event_type = "latest_results"
event_no = "627"
# event_type = "latest_results"

pr = parkrun.Parkrun(count, loc, event_no)
denmark = pr.get_latest_results_country()
denmark.to_csv("denmark.csv")

# print(pr.locations)

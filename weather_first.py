import requests

r = requests.get("https://wttr.in/foshan",params={"format":"j1"},timeout=15)
print(r.status_code)
data = r.json()
time_now = data["current_condition"][0]['observation_time']
city = data["nearest_area"][0]["areaName"][0]["value"]
Temp_now = data["current_condition"][0]["temp_C"]
print(f'佛山 现在{time_now} {Temp_now}度')
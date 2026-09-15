import requests
import sys
try:
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",params={"name": "Foshan", "count": 1, "language": "zh"},timeout=15,).json()
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather = requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude": lat,"longitude": lon,"daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode","timezone": "Asia/Shanghai","forecast_days": 3,},timeout=15,).json()
    today_time = weather["daily"]["time"][0]
    temp_max_tomorrow = weather["daily"]["temperature_2m_max"][1]
    temp_max = weather["daily"]["temperature_2m_max"][0]
    riqi = weather["daily"]["time"]
    zuigaowen = weather["daily"]["temperature_2m_max"]
    zuidiwen = weather["daily"]["temperature_2m_min"]
    jiangyugailv = weather["daily"]["precipitation_probability_max"]
    tianqima = weather["daily"]["weathercode"]
except requests.exceptions.RequestException as e:
    print('天气服务暂时不可用，请稍后重试')
    sys.exit()
for i in range(3):
    print(f"{riqi[i]}  最高 {zuigaowen[i]}  最低 {zuidiwen[i]}")
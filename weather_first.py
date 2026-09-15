import requests
import sys
try:
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",params={"name": "Foshan", "count": 1, "language": "zh"},timeout=15,).json()
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather = requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude": lat,"longitude": lon,"daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode","timezone": "Asia/Shanghai","forecast_days": 3,},timeout=15,).json()
except requests.exceptions.RequestException as e:
    print('天气服务暂时不可用，请稍后重试')
    sys.exit()

today_time = weather["daily"]["time"][0]
temp_max_tomorrow = weather["daily"]["temperature_2m_max"][1]
temp_max = weather["daily"]["temperature_2m_max"][0]
print(f'佛山{lat},{lon} 现在{today_time} {temp_max}度 明天{temp_max_tomorrow}度')
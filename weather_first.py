import requests
import sys
import json
import csv
from pathlib import Path
BASE = Path(__file__).parent
(BASE / "out").mkdir(exist_ok=True)


try:
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",params={"name": "Foshan", "count": 1, "language": "zh"},timeout=15,).json()
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather = requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude": lat,"longitude": lon,"daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode","timezone": "Asia/Shanghai","forecast_days": 3,},timeout=15,).json()
    riqi = weather["daily"]["time"]
    zuigaowen = weather["daily"]["temperature_2m_max"]
    zuidiwen = weather["daily"]["temperature_2m_min"]
    jiangyugailv = weather["daily"]["precipitation_probability_max"]
    tianqima = weather["daily"]["weathercode"]
except requests.exceptions.RequestException as e:
    print('天气服务暂时不可用，请稍后重试')
    sys.exit()
WMO_ZH = {
    0: "晴",           1: "大致晴朗",      2: "局部多云",      3: "阴",
    45: "雾",          48: "雾凇",
    51: "小毛毛雨",    53: "中毛毛雨",     55: "大毛毛雨",
    56: "冻毛毛雨",    57: "强冻毛毛雨",
    61: "小雨",        63: "中雨",         65: "大雨",
    66: "冻雨",        67: "强冻雨",
    71: "小雪",        73: "中雪",         75: "大雪",
    77: "雪粒",
    80: "小阵雨",      81: "中阵雨",       82: "强阵雨",
    85: "小阵雪",      86: "大阵雪",
    95: "雷阵雨",
    96: "雷阵雨伴小冰雹",  99: "雷阵雨伴大冰雹",
}
预报 = []
for i in range(3):
    shuju = {'日期': riqi[i], '天气': WMO_ZH.get(tianqima[i], '未知'), '最高温': zuigaowen[i], '最低温': zuidiwen[i], '降雨概率': jiangyugailv[i]}
    预报.append(shuju)
    print(f"{riqi[i]}  {WMO_ZH.get(tianqima[i], '未知')}  最高 {zuigaowen[i]}  最低 {zuidiwen[i]}  降雨概率 {jiangyugailv[i]}%")
with open(BASE / "out" / "weather.json", 'w', encoding='utf-8') as f:
    json.dump(预报,f,ensure_ascii=False,indent=2)
fieldnames = ['日期', '天气', '最高温', '最低温', '降雨概率']
with open(BASE / "out" / "weather.csv", 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(预报)
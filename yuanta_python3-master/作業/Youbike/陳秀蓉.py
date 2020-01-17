import json
import requests
import sys
from math import sin, cos, sqrt, atan2, radians


def main(point_1_lat, point_1_lon, point_2_lat, point_2_lon):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(point_1_lat))
    lon1 = radians(float(point_1_lon))
    lat2 = radians(float(point_2_lat))
    lon2 = radians(float(point_2_lon))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000
    return distance

data = []
url = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz"

reqs = requests.get(url)

if reqs.status_code == 200:
    text = reqs.text
    ydata = json.loads(text)
    i = 0
    for item, value in ydata["retVal"].items():
      sno = value["sno"]
      sna = value["sna"]
      lat = value["lat"]
      lng = value["lng"]
      bemp= value["bemp"]
      sbi = value["sbi"]
      if main("25.052465", "121.543700", lat, lng) < 500 and int(bemp)>=20 and int(sbi)>=20:
        std = "SNO."+ sno + " " + sna + " 場站目前車輛數量:" + sbi + " 空位數量:" + bemp
        print(std)


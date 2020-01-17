#https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz

import json
import requests
import sys
from math import sin, cos, sqrt, atan2, radians

def main(point_1_lat, point_1_lon, point_2_lat, point_2_lon, unit='m'):
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
    #print("Distance: " + str(distance) + "m")
    return distance

url = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'

r = requests.get(url)

if r.status_code == requests.codes.ok:
    print("Requests OK")

#print(r.text)

obj = json.loads(r.text)

youBikes = obj['retVal']

for item in youBikes:
    site = youBikes[item]

    bemp = int(site['bemp'])   #可還數量
    sbi = int(site['sbi'])     #可借數量
    lat = float(site['lat'])   #緯度
    lng = float(site['lng'])   #經度

    dist = main(25.052404, 121.543693, lat, lng)
    if dist < 500 and sbi >= 20 and bemp >= 20:
        print("站台: {0}, 可租:{1}, 可還: {2}, 距離: {3} 公尺".format(site['sna'], sbi, bemp, int(dist)))

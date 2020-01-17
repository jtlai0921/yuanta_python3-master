# -*- coding: utf-8 -*-
import requests
import json
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
    #print ("Distance: " + str(distance) + "m")
    return distance

url = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'
res = requests.get(url)
obj = json.loads(res.text)
ubike = obj.get('retVal')
now_lat = 25.052110
now_lon = 121.543666

near_ubike={}
print('附近500公尺內，可租20輛同時也可還20輛的站：')
for item in ubike:
    ubike_lat = ubike[item]['lat']
    ubike_lon = ubike[item]['lng']
    m = main(now_lat,now_lon,ubike_lat,ubike_lon)
    if m < 500 and int(ubike[item]['sbi']) > 20 and int(ubike[item]['bemp']) > 20:
        print('站名：',ubike[item]['sna'],',',ubike[item]['ar'])

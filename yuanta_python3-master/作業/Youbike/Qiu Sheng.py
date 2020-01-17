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
    return distance

url = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'

resp = requests.get(url)
if resp.status_code == 200:
    text = resp.text
    bike_json = json.loads(text)
    # print(bike_json)
    # print(bike_json['retVal']['0001'])
    #元大期貨 緯度25.052133, 經度121.543671
    # print(bike_json['retVal']['%04d' % 1])
    # print(len(bike_json['retVal']))
    for station in bike_json['retVal']:
        # print(bike_json['retVal'][station])
        # sbi:場站目前車輛數量(可借)、bemp：空位數量(可還)
        if int(bike_json['retVal'][station]['sbi']) < 20 or int(bike_json['retVal'][station]['bemp']) < 20:
            continue

        # lat：緯度、lng：經度
        dis = main(25.052133, 121.543671, bike_json['retVal'][station]['lat'], bike_json['retVal'][station]['lng'])
        if dis < 500:
            # print(bike_json['retVal'][station]['sno'] + '距離:%.2f' % dis)
            print("代號:{0}, 站名:{1}, 距離:{2:.2f}m, 可借:{3}, 可還:{4}".format(
            bike_json['retVal'][station]['sno'],
            bike_json['retVal'][station]['sna'],
            dis,
            bike_json['retVal'][station]['sbi'],
            bike_json['retVal'][station]['bemp']))

import json
import requests
import math

url = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz"

lat = "25.0512947"
lon = "121.5386181"


def distence(point_1_lat, point_1_lon, point_2_lat, point_2_lon, unit='m'):
    R = 6373.0
    lat1 = math.radians(float(point_1_lat))
    lon1 = math.radians(float(point_1_lon))
    lat2 = math.radians(float(point_2_lat))
    lon2 = math.radians(float(point_2_lon))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * (1000 if unit == 'm' else 1)


req = requests.get(url)
if req.status_code == 200:
    pJData = json.loads(req.text)
    if pJData["retCode"] == 1:
        pJValue = pJData["retVal"]
        # print(pJValue)
        for value in pJValue.values():
            dist = distence(lat, lon, value["lat"], value["lng"])
            if int(value["bemp"]) > 20 and int(value["sbi"]) > 20 and dist < 500:
                print("距離%.4f公尺 編號:%s %s" % (dist, value["sno"], value["ar"]))
else:
    print("Get Failed : " + req.status_code)

# coding: utf-8

import requests as re
import pandas as pd

def get_lat_lng(address):
    """
    Returns the latitude and longitude of a location using the Google Maps Geocoding API. 
    API: https://developers.google.com/maps/documentation/geocoding/start

    # INPUT -------------------------------------------------------------------
    apiKey                  [str]
    address                 [str]

    # RETURN ------------------------------------------------------------------
    lat                     [float] 
    lng                     [float] 
    """
    import requests
    apiKey="AIzaSyCTjlv-bfImwzFnQ8jXr2ZToILivD2l0wc"
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ','+'), apiKey))
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
    except:
        print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
    return lat, lng

#求距離函式distance

from math import sin, cos, sqrt, atan2, radians

def distance(point_1_lat, point_1_lon, point_2_lat, point_2_lon):
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


#youbike 網址 : https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz
YB_url="https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz"


YB_gz=re.get(YB_url)
YB_df=pd.read_json(YB_gz.text)
YB_df2=pd.DataFrame(YB_df.retVal.values.tolist())

Q_address=input("請輸入你想查詢的地址 or 地名 (例:元大投信) >>")
Q_lat,Q_lng=get_lat_lng(Q_address)
print("{} 查出來的經緯度為{},{}".format(Q_address,Q_lat,Q_lng))

rent_n=int(input("想同時借跟還的車輛數 :"))
rent_d=int(input("範圍幾公尺之內的youbike站 :"))

YB_df2.sbi=YB_df2.sbi.astype(int)
YB_df2.bemp=YB_df2.bemp.astype(int)

ok_df=YB_df2[(YB_df2['bemp'] > rent_n) & (YB_df2['sbi'] > rent_n)] 

print('可租還{}台以上，且與 [{}] 距離{}公尺以內的站台 :'.format(rent_n,Q_address,rent_d))
x=0
for lat,lng,sna,ar in zip(ok_df.lat,ok_df.lng,ok_df.sna,ok_df.ar):
    dd=distance(Q_lat,Q_lng,lat,lng)
    
    if dd<rent_d :
        x=x+1
        print('站台{}:{} \t 地址:{}'.format(x,sna,ar))
if x==0:
    print('無符合資格的站台!')




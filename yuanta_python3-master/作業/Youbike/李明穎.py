import requests, json, sys
from math import sin, cos, sqrt, atan2, radians
url ='https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'

data = requests.get(url)

def checkRice(jasondata):
    for item in list(jasondata.values()):
        bemp = item['bemp']#空位數
        tot = item['tot']#場站總停車格
        print('場站名%s 空位數:%s 場站總停車格:%s:' %(item['sna'],bemp ,tot))
        #sna 場站名稱
        if(int(bemp) >=20 or (int(bemp) - int(tot)) >=20 ):
            if(int(main(item['lat'],item['lng'],'25.052401','121.543718')) <= 500):        #25°03'08.6"N 121°32'37.4"E
                return item['sna']

    return ""


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
    print ("Distance: " + str(distance) + "m")
    return distance



if(data.status_code == 200):#204是put一個特別成功，2開頭都是成功
    print('讀取資料成功')
    #print(data.text)
    jasonstr = json.loads(data.text)
    print(jasonstr['retVal'])
    #大同大樓500公尺內的站台
    data = checkRice(jasonstr['retVal'])
    if(data !=""):
        print("5佰米內場站為："+data)
    else:
        print('沒有場站')
else:
    print('Error')




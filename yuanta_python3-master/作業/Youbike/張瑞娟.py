#找出離公司500m內的youbike站 有至少20台車，並有20個以上空位
import requests
from math import radians, cos, sin, asin, sqrt

#我的公司地點 (北市南京東路三段225號)
mylat = 25.052071
mylon = 121.543663

#北市公開資訊 youbike
"""
 sno：站點代號、
 sna：場站名稱(中文)、
 tot：場站總停車格、
 sbi：場站目前車輛數量、
 sarea：場站區域(中文)、
 mday：資料更新時間、
 lat：緯度、
 lng：經度、
 ar：地(中文)、
 sareaen：場站區域(英文)、
 snaen：場站名稱(英文)、
 aren：地址(英文)、
 bemp：空位數量、
 act：全站禁用狀態
"""

url = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz"
data = requests.get(url).json()

#大圓距離(回傳公尺)
def haversine( point_1_lon, point_1_lat, point_2_lon, point_2_lat):  # 經度1，緯度1，經度2，緯度2 （十进制度数）
    # 轉化為弧度
    lat1 = radians(float(point_1_lat))
    lon1 = radians(float(point_1_lon))
    lat2 = radians(float(point_2_lat))
    lon2 = radians(float(point_2_lon))

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6373.0  # 地球平均半徑(公里)
    dist = c * r * 1000

    return dist

#輪詢JSON資料
for key, value in data["retVal"].items():
  sno = value["sno"]
  sna = value["sna"]
  sbi = value["sbi"]
  bemp = value["bemp"]
  lat = value["lat"]
  lng = value["lng"]

  if ( int(sbi) < 20 or int(bemp) < 20) :
    continue

  if (haversine(mylon, mylat, lng, lat) > 500) :
    continue;

  print("NO.", sno, sna, "目前車輛 / 空位：",sbi, "/", bemp)
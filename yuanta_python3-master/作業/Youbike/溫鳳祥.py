# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥

import os
import json
from math import sin, cos, atan2, acos, sqrt, radians


# Method 1: https://blog.lovian.org/python/2018/04/16/python-calculate-distance-in-lat-lon.html
def calc_distance(start_lat, start_lng, end_lat, end_lng):
    # approximate radius of earth in km
    R = 6373.0

    dlng = end_lng - start_lng
    dlat = end_lat - start_lat

    a = sin(dlat / 2)**2 + cos(start_lat) * cos(end_lat) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000


# Method 2: https://www.w3resource.com/python-exercises/math/python-math-exercise-27.php
def calc_distance2(start_lat, start_lng, end_lat, end_lng):
    start_lat = radians(start_lat)
    start_lng = radians(start_lng)
    end_lat = radians(end_lat)
    end_lng = radians(end_lng)
    # return 6371.01 * 1000 * acos(sin(start_lat) * sin(end_lat) + cos(start_lat) * cos(end_lat) * cos(start_lng - end_lng))
    return 6373.0 * 1000 * acos(sin(start_lat) * sin(end_lat) + cos(start_lat) * cos(end_lat) * cos(start_lng - end_lng))


if __name__ == '__main__':
    # 元大投信: 25°03'09.0"N 121°32'35.7"E
    lat0 = 25.03090
    lng0 = 121.32357
    print("元大投信座標：lat=%.2f lng=%.2f" % (lat0, lng0))

    try:
        # read U-Bike stations info file
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        src_file = open('%s/YouBikeTP' % curr_dir, mode='r', encoding='UTF-8')
        json_obj = json.loads(src_file.read())

        num2 = None
        sinfo2 = None
        min_dist = 99999999
        """
        U-Bike JSON 格式: https://data.taipei/opendata/datalist/apiAccess?scope=datasetMetadataSearch&q=id:8ef1626a-892a-4218-8344-f7ac46e1aa48
        sno：序號(?)
        sna：場站名稱(中文)
        tot：場站總停車格
        sbi：場站目前車輛數量
        sarea：場站區域(中文)
        mday：資料更新時間
        lat：緯度
        lng：經度
        ar：地(中文)
        sareaen：場站區域(英文)
        snaen：場站名稱(英文)
        aren：地址(英文)
        bemp：空位數量
        act：全站禁用狀態
        """
        for num in json_obj["retVal"]:
            sinfo = json_obj["retVal"][num]
            sno = sinfo['sno']          # 序號(?)
            sna = sinfo['sna']          # 場站名稱(中文)
            sarea = sinfo['sarea']      # 場站區域(中文)
            ar = sinfo['ar']            # 地(中文)
            sbi = int(sinfo['sbi'])     # 場站目前車輛數量
            bemp = int(sinfo['bemp'])   # 空位數量
            act = int(sinfo['act'])     # 全站禁用狀態
            lat = float(sinfo['lat'])   # 緯度
            lng = float(sinfo['lng'])   # 經度
            dist = calc_distance(lat0, lng0, lat, lng)
            dist2 = calc_distance2(lat0, lng0, lat, lng)
            # print('[%s] sna=%s sarea=%s sbi=%d bemp=%d lat=%.2f lng=%.2f act=%d (dist=%.2fm dist2=%.2fm)'
            #       % (sno, sna, sarea, sbi, bemp, lat, lng, act, dist, dist2))

            if sbi >= 20 and bemp >= 20 and act == 1:
                if dist < 500:
                    print('Found(1): [%s] sna=%s sarea=%s sbi=%d bemp=%d lat=%.2f lng=%.2f act=%d (dist=%.2fm dist2=%.2fm)'
                          % (sno, sna, sarea, sbi, bemp, lat, lng, act, dist, dist2))
                elif dist2 < 500:
                    print('Found(2)[%s] sna=%s sarea=%s sbi=%d bemp=%d lat=%.2f lng=%.2f act=%d (dist=%.2fm dist2=%.2fm)'
                          % (sno, sna, sarea, sbi, bemp, lat, lng, act, dist, dist2))
        else:
            print("找不到符合條件的 U-Bike 站點！")

        src_file.close()
    except IOError as ex:
        print('Open file failed: ' + str(ex))
    except Exception as ex:
        print('Exception: ' + str(ex))



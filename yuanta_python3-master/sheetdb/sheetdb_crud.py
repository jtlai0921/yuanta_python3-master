# Excel 位置 : https://docs.google.com/spreadsheets/d/1FSpCRaafI1Yo3PSxFzgIwmuJ88foXVztZ6QW8GuyLR0/edit?ts=5cc7e8ac#gid=1298666315
# Excel key : rk7bud9tvo80v
# Excel sheet : tx_index
# 注意：Excel (tx_index) 第一行是欄位title定義不可以刪除

import requests

headers = {'Content-Type': 'application/json'}

# 新增
def add(d, t, ai_index, color):
    # 新增
    # https://sheetdb.io/api/v1/ 這是 url
    # rk7bud9tvo80v 這是 key 值 (用來決定是哪一個 excel 表，每一個 excel 都有一個 key 值)
    # sheet=tx_index 這是 excel 表的 sheet tab
    url = 'https://sheetdb.io/api/v1/d9tvo80v/?sheet=tx_index'
    # 存入預測指數 date, time, ai_index, red (此時 開高低收應該都是空白)
    data = '{"data":[{ "date": "%s", "time": "%s", "open":"", "high":"", "low":"", "close":"", "ai_index":%d, "color":"%s" }]}' % (d, t, ai_index, color)
    r = requests.post(url=url,data=data,headers=headers)
    print(r)


# 修改 ai_index
def patch_ai_index(t, ai_index, color):
    url = 'https://sheetdb.io/api/v1/ud9tvo80v/time/%s/?sheet=tx_index' % t
    data = '{"data":[{"ai_index":%d, "color":"%s"}]}' % (ai_index, color)
    r = requests.patch(url=url,data=data,headers=headers)
    print(r)

# 修改 ai_index 與 開高低收
def patch_ai_index_and_ohlc(t, open, high, low, close, ai_index, color):
    url = 'https://sheetdb.io/api/v1/ud9tvo80v/time/%s/?sheet=tx_index' % t
    data = '{"data":[{"open":%d, "high":%d, "low":%d, "close":%d, "ai_index":%d, "color":"%s"}]}' % (open, high, low, close, ai_index, color)
    r = requests.patch(url=url,data=data,headers=headers)
    print(r)

# 修改開高低收
def patch_ohlc(t, open, high, low, close):
    # 存入開高低收
    # PUT https://sheetdb.io/api/v1/58f61be4dda40/{column}/{value}
    # 注意：{column}/{value} -> time/08:45:00-08:45:59 是根據 time 內容來指定修改的那一行
    url = 'https://sheetdb.io/api/v1/ud9tvo80v/time/%s/?sheet=tx_index' % t
    data = '{"data":[{"open":%d, "high":%d, "low":%d, "close":%d}]}' % (open, high, low, close)
    r = requests.patch(url=url,data=data,headers=headers)
    print(r)


# 刪除
def delete(t):
    # 刪除
    url = 'https://sheetdb.io/api/v1/rk7buo80v/time/%s/?sheet=tx_index' % t
    r = requests.delete(url=url, headers=headers)
    print(r)


# 新增紀錄 參數說明：日期, 時間(Key值), ai預測值, 顏色(需填入red或green)
add("20190701", "08:45:00-08:45:59", 9983, 'red')

# 修改 ai_index 參數說明：時間(Key值), 開, 高, 低, 收
#patch_ai_index("08:45:00-08:45:59", 9982, 'green')

# 修改開高低收 參數說明：時間(Key值), 開, 高, 低, 收
#patch_ohlc("08:45:00-08:45:59", 10951, 10960, 10950, 10952)

# 刪除紀錄 參數說明：時間(Key值)
#delete("08:45:00-08:45:59")


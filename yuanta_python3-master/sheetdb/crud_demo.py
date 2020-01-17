import requests
import json

headers = {'Content-Type': 'application/json'}
# url = 'https://sheetdb.io/api/v1/rk7bud9tvo80v/?sheet=TX'
# data = '{"data":[{ "name": "Scott", "age": "21" }]}'
# r = requests.post(url=url,data=data,headers=headers)
# print(r)


# 
url = 'https://sheetdb.io/api/v1/rk7bud9tvo80v/name/B/?sheet=TX'
data = '{"data":[{ "name": "Scott", "age": "30" }]}'
r = requests.patch(url=url,data=data,headers=headers)
print(r)


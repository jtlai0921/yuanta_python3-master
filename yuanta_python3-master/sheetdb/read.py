import requests
import json

headers = {'Content-Type': 'application/json'}
url = 'https://sheetdb.io/api/v1/yaco85fdbhmed/?sheet=sheet1'
res = requests.get(url=url, headers=headers)
print(res.text)
users = json.loads(res.text)
print(users[0]['name'])

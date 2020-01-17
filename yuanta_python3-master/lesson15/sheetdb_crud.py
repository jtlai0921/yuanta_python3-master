import requests

headers = {'Content-Type': 'application/json'}

def read():
    url = 'https://sheetdb.io/api/v1/pn0tjkupilpqk?sheet=page1'
    res = requests.get(url=url, headers=headers)
    print(res.text)

def add():
    url = 'https://sheetdb.io/api/v1/pn0tjkupilpqk?sheet=page1'
    data = '{"data":[{ "name": "Scott", "age": "21" }]}'
    res = requests.post(url=url, data=data, headers=headers)

def update():
    data = '{"data":[{ "name": "Scott", "age": "40" }]}'
    url = 'https://sheetdb.io/api/v1/pn0tjkupilpqk/name/Scott?sheet=page1'
    res = requests.patch(url=url, data=data, headers=headers)

def delete():
    url = 'https://sheetdb.io/api/v1/pn0tjkupilpqk/name/Scott?sheet=page1'
    res = requests.delete(url=url, headers=headers)


#add()
#update()
#delete()
read()

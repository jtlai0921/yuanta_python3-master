import requests
from bs4 import BeautifulSoup

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

url = 'https://taqm.epa.gov.tw/pm25/tw/PM25A.aspx?area=1'
html = requests.get(url, headers=headers)


sp = BeautifulSoup(html.text, 'html.parser')

print(sp.find("span", {"id":"ctl08_labText1"}).text.strip());

rs = sp.find_all("tr", {"align":"center", "style":"border-width:1px;border-style:Solid;"})

for r in rs:
    name = r.find('a').text.strip()
    pm25 = r.find_all('span')
    print(name, end=" ")
    for p in pm25:
        print(p.text.strip(), end=" ")
    print()

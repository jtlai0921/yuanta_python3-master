import requests
from bs4 import BeautifulSoup

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

url = 'https://taqm.epa.gov.tw/pm25/tw/PM25A.aspx?area=1'
html = requests.get(url, headers=headers)


sp = BeautifulSoup(html.text, 'html.parser')

pm25_str = sp.find("span", {"id":"ctl08_labText1"}).text.strip() + "\n"

rs = sp.find_all("tr", {"align":"center", "style":"border-width:1px;border-style:Solid;"})

for r in rs:
    image_path = r.find('img').get('src').strip('..')
    image_path = 'https://taqm.epa.gov.tw/pm25' + image_path
    print(image_path)


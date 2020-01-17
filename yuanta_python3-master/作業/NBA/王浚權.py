from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import re
import os

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
url = 'https://tw.sports.yahoo.com/nba/standings/'
html = requests.get(url, headers=headers)
sp = BeautifulSoup(html.text, 'html.parser')

data = ''

#header 1
rs = sp.find_all("tr", {"data-reactid":"57"})

for r in rs:
    headers = r.find_all('th')
    for h in headers:
        data = data + h.text.strip() + ','
        print(h.text.strip())

data = data[:-1] + '\n'

#title = sp.find("a", {"href":"/nba/teams/公鹿/"}).get('title').strip()

#section 1
title_reactid = [80, 105, 130, 155, 180, 205, 230, 255, 280, 302, 324, 346, 368, 390, 412]

for t in title_reactid:
    title = sp.find("span", {"data-reactid": str(t)}).text.strip()
    data = data + title + ','
    print(title)

    rs = sp.find_all("tr", {"data-reactid": str(t-7)})

    for r in rs:
        cols = r.find_all('td')
        for c in cols:
            data = data + c.text.strip() + ','
            print(c.text.strip())

        data = data[:-1] + '\n'

#header 2
rs = sp.find_all("tr", {"data-reactid":"429"})

for r in rs:
    headers = r.find_all('th')
    for h in headers:
        data = data + h.text.strip() + ','
        print(h.text.strip())

data = data[:-1] + '\n'

#section 2
title_reactid = [452, 477, 502, 527, 552, 577, 602, 627, 652, 674, 696, 718, 740, 762, 784]

for t in title_reactid:
    title = sp.find("span", {"data-reactid": str(t)}).text.strip()
    data = data + title + ','
    print(title)

    rs = sp.find_all("tr", {"data-reactid": str(t-7)})

    for r in rs:
        cols = r.find_all('td')
        for c in cols:
            data = data + c.text.strip() + ','
            print(c.text.strip())

        data = data[:-1] + '\n'

#rs = sp.find_all("img", src=re.compile("png"))
#print(rs)

# 寫檔
filename = 'nba.txt'
folder = 'nba'
if not os.path.exists(folder):
    os.makedirs(folder)

file = open(folder + "/" + filename, 'w')
file.write(data)
file.close()

#images
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

image_reactid = [79, 104, 129, 154, 179, 204, 229, 254, 279, 301, 323, 345, 367, 389, 411, 451, 476, 501, 526, 551, 576, 601, 626, 651, 673, 695, 717, 739, 761, 783]

for i in image_reactid:
    image_path = sp.find("img", {"data-reactid": str(i)}).get('style').strip()
    image_path = image_path.split('(')[1]
    image_path = image_path.split(')')[0]
    print(image_path)

    filename = os.path.basename(image_path)
    print(filename)

    # 寫檔
    folder = 'nba/icon'
    if not os.path.exists(folder):
        os.makedirs(folder)

    req = Request(url=image_path, headers=headers)
    file = open(folder + "/" + filename, 'wb')
    file.write(urlopen(req).read())
    file.close()

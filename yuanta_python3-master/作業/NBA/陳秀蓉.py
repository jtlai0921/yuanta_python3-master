from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = 'https://tw.sports.yahoo.com/nba/standings'
html = requests.get(url, headers=headers)
sp = BeautifulSoup(html.text, 'html.parser')

rs = sp.find_all("th", {"Py(4px) Ta(c)"})
rs1 = sp.find_all("tr", {""})
rs2 = sp.find_all("img", style=re.compile("png"))

indata = "   "
for r in rs:
    if int(r.get("data-reactid")) > 71:
        break
    indata = indata + r.text.strip() + " "
indata += "\n"

for r1 in rs1:
    name = r1.find('a').text.strip()
    data = r1.find_all('td')
    indata = indata + name + " "
    for p in data:
        indata = indata + p.text.strip() + " "
    indata += "\n"

folder = "nba"
if not os.path.exists(folder):
    os.makedirs(folder)

# 寫檔
file = open(folder + "/" +'nba.txt', 'w', encoding='utf-8')
file.write(indata)

# 讀檔
file = open(folder + "/" +'nba.txt', 'r', encoding='utf-8')
outdata = file.read()
print(outdata)

folder += "/icon"
if not os.path.exists(folder):
    os.makedirs(folder)

for r in rs2:
    image_path = r.get('style')
    url_path = ""
    i = 0
    for item in image_path:
        i = i + 1
        if ( i>21 and item != ")" and item != ";"):
            url_path += item
    filename = os.path.basename(url_path)
    print(filename)
    # 寫檔
    req = Request(url=url_path, headers=headers)
    file = open(folder + "/" + filename, 'wb')
    file.write(urlopen(req).read())
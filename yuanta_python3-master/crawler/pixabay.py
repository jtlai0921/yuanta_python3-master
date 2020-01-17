from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = 'https://pixabay.com/zh/photos/?cat=nature'
html = requests.get(url, headers=headers)

sp = BeautifulSoup(html.text, 'html.parser')

rs = sp.find_all("img", src=re.compile("jpg"))

for r in rs:
    image_path = r.get('src')
    print(image_path)
    filename = os.path.basename(image_path)
    # 寫檔
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)

    req = Request(url=image_path, headers=headers)

    file = open(folder + "/" + filename, 'wb')
    file.write(urlopen(req).read())


from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = "https://tw.sports.yahoo.com/nba/standings/"
html = requests.get(url, headers=headers)

sp = BeautifulSoup(html.text, 'html.parser')
# print(sp)

# 建立存檔目錄
folder = 'nba'
if not os.path.exists(folder):
    os.makedirs(folder)
    os.makedirs(folder + "/icon")

table = sp.find("table", {"class" : "W(100%)"})
if table != None:
    file = open(folder + "/nba.txt", "w", encoding="utf-8")

    titles = list(p.text for p in table.find("thead").find_all("th"))
    # print(titles)
    for i in range(0, len(titles)):
        if i > 0:
            file.write(",")
        file.write(titles[i])

    file.write("\n")

    datas = table.find("tbody").find_all("tr")
    for dataitem in datas:
        aa = dataitem.find("th").find("a")
        name = aa.get("title")
        file.write(name)
        for value in list(td.text for td in dataitem.find_all("td")):
            file.write("," + value)
        file.write("\n")

        stylelist = aa.find("img").get("style")
        if stylelist.endswith(";"):
            stylelist = stylelist[0: -1]
        pic_url = dict(p.split(":", 1) for p in stylelist.split(";")).get("background-image", "url()")
        src = pic_url[4:-1]
        if len(src) > 0:
            req = Request(url=src, headers=headers)
            p_file = open(folder + "/icon/" + name + os.path.splitext(src)[1], "wb")
            p_file.write(urlopen(req).read())

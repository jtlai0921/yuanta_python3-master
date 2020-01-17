from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

url = 'https://tw.sports.yahoo.com/nba/standings/'
html = requests.get(url, headers=headers)

sp = BeautifulSoup(html.text, 'html.parser')
#<tr data-reactid="57"><th class="Py(4px) Ta(c) Pstart(25px) Ta(start)" title="東區" data-reactid="58">東區</th><th class="Py(4px) Ta(c)" title="Wins" data-reactid="59">勝</th><th class="Py(4px) Ta(c)" title="Losses" data-reactid="60">敗</th><th class="Py(4px) Ta(c)" title="Win Percentage" data-reactid="61">勝率</th><th class="Py(4px) Ta(c) D(n)" title="Games Back" data-reactid="62">勝差</th><th class="Py(4px) Ta(c)" title="Conf Games Back" data-reactid="63">區勝差</th><th class="Py(4px) Ta(c)" title="Home Record" data-reactid="64">主場</th><th class="Py(4px) Ta(c)" title="Division Record" data-reactid="65">分組</th><th class="Py(4px) Ta(c)" title="Conference Record" data-reactid="66">分區</th><th class="Py(4px) Ta(c)" title="Last 10 Record" data-reactid="67">近10場</th><th class="Py(4px) Ta(c)" title="Points For" data-reactid="68">平均得分</th><th class="Py(4px) Ta(c)" title="Points Against" data-reactid="69">平均失分</th><th class="Py(4px) Ta(c)" title="Net Points" data-reactid="70">得分差</th><th class="Py(4px) Ta(c)" title="Streak" data-reactid="71">連勝/敗</th></tr>
elm57 = sp.find("tr", {"data-reactid":"57"});
elm429 = sp.find("tr", {"data-reactid":"429"});
#time = sp.find("span", {"id":"ctl08_labText1"}).text.strip();
title = sp.find_all("th", {"class":"Py(4px) Ta(c)"})
#rs = sp.find_all("img", src=re.compile("png"))#正則表示式
retText = ""
table1rowcount = 15;#每區列數
table2colcount = 13;#行數

for cln in elm57.children:#東區標題
   retText+=(cln.text+",")
retText = retText[:-1]
retText +="\n"

#<a href="/nba/teams/暴龍/" title="暴龍" class="C(primary-text) C(primary-text):link C(primary-text):visited" data-reactid="102"><span class="D(tbc) Va(m) H(40px)" data-reactid="103"><img class="Trsdu(.42s) Mstart(20px) Mend(10px) Va(m)" height="30" width="30" style="" src="https://s.yimg.com/cv/apiv2/default/nba/20181221/70x70/raptors_wbgs.png" data-reactid="104"></span><span class="D(tbc) Va(m) H(40px)" data-reactid="105"><!-- react-text: 106 -->暴龍<!-- /react-text --><span data-reactid="107"><!-- react-text: 108 --> - <!-- /react-text --><!-- react-text: 109 -->y<!-- /react-text --></span></span></a>
#<th class=" Ta(start) Fw(400) W(25%) Fz(12px) Fw(b) H(40px)" data-reactid="74"><div data-reactid="75"><div class="D(tb)" data-reactid="76"><a href="/nba/teams/公鹿/" title="公鹿" class="C(primary-text) C(primary-text):link C(primary-text):visited" data-reactid="77"><span class="D(tbc) Va(m) H(40px)" data-reactid="78"><img class="Trsdu(.42s) Mstart(20px) Mend(10px) Va(m)" height="30" width="30" style="" src="https://s.yimg.com/cv/apiv2/default/nba/20181214/70x70/bucks_wbg.png" data-reactid="79"></span><span class="D(tbc) Va(m) H(40px)" data-reactid="80"><!-- react-text: 81 -->公鹿<!-- /react-text --><span data-reactid="82"><!-- react-text: 83 --> - <!-- /react-text --><!-- react-text: 84 -->z<!-- /react-text --></span></span></a></div></div></th>
content = sp.find_all("a",{"class":"C(primary-text) C(primary-text):link C(primary-text):visited"})
#<td class="Bdb(primary-border) Ta(c)" data-reactid="85">60</td>
content2 = sp.find_all("td",{"class":"Bdb(primary-border) Ta(c)"})
nbaTeamName = []
colCount =0;
nbaTeamValue = []
for r in content:
   #隊名
   nbaTeamName.append(r.text )
   colCount+=1
for r in content2:
   #數值
   nbaTeamValue.append(r.text )

rowCount = 0#第幾隊
for row in nbaTeamName:
   retText += row+","
   for row2 in range(0, len(nbaTeamValue)):
      if(rowCount == 0):
         retText += nbaTeamValue[row2]+","
      else:
         retText += nbaTeamValue[row2 + (table2colcount-1 * int(rowCount))]+","

      if(row2 % colCount == table2colcount):
         retText = retText[:-1]
         retText+="\n"
         break
   rowCount+=1
   if(rowCount == table1rowcount):#插入西區標題
      for cln in elm429.children:
         retText += (cln.text + ",")
      retText = retText[:-1]
      retText +="\n"

#print(retText)
# 寫檔
folder = 'nba'
folder1 = 'nba/icon'
if not os.path.exists(folder):
    os.makedirs(folder)
if not os.path.exists(folder1):
    os.makedirs(folder1)
file = open(folder + "/" + "nba.txt", 'w', encoding='utf-8')
file.write(str(retText))

#<img class="Trsdu(.42s) Mstart(20px) Mend(10px) Va(m)" height="30" width="30" style="" src="https://s.yimg.com/cv/apiv2/default/nba/20181213/70x70/warriors_wbg.png" data-reactid="451">
rs = sp.find_all("img")#正則表示式

for r in rs:
   image_path = r.get('style')
   image_path = image_path.replace('background-image:url(','')
   image_path = image_path.replace(');','')
   filename = os.path.basename(image_path)
   print(image_path)
   req = Request(url=image_path, headers=headers)
   file1 = open(folder1 + "/" + filename, 'wb')  # wb為2進制的代碼
   file1.write(urlopen(req).read())

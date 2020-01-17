# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥
# Desc: NBA 戰績資料寫檔

import os
import urllib.request
import requests
import bs4

if not os.path.exists('nba'):
    os.makedirs('nba/icon')

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
url = 'https://tw.sports.yahoo.com/nba/standings'
html = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(html.text, 'html.parser')
data = ''

# title = soup.title.text.strip()

# league:
# <select data-tst="standings-league-dropdown" class="Bgc(#fff)! C(#000)! Cur(p) M(0) P(0) Pos(a) T(0) Start(0) W(100%) H(100%) Op(0)" data-reactid="13">
# <option selected="" value="0" data-reactid="14">NBA</option>
# <option value="1" data-reactid="15">季後賽</option>
# </select>
league = soup.find('select', { 'data-tst': 'standings-league-dropdown' }).text.strip()

# season:
# < select data-tst="season-dropdown" class="Bgc(#fff)! C(#000)! Cur(p) M(0) P(0) Pos(a) T(0) Start(0) W(100%) H(100%) Op(0)" data-reactid="25">
# <option selected="" value="0" data-reactid="26">2018/2019</option>
# <option value="1" data-reactid="27">2017/2018</option>
# <option value="2" data-reactid="28">2016/2017</option>
# ...
# <option value="16" data-reactid="42">2002/2003</option>
# </select>
listbox = soup.find('select', { 'data-tst': 'season-dropdown' })
season = listbox.find('option', { 'selected': '' }).text.strip()
# data = '{}\n{} {}\n'.format(title, league, season)
data = '{} {}\n'.format(league, season)


# 東區/西區戰績 table
for table in soup.find_all('table', { 'class': 'W(100%)' }):
    # header
    # <thead class="Bgc($c-fuji-grey-m) C(#fff) Fz(12px)" data-reactid="56"><tr data-reactid="57"><th class="Py(4px) Ta(c) Pstart(25px) Ta(start)" title="東區" data-reactid="58">東區</th><th class="Py(4px) Ta(c)" title="Wins" data-reactid="59">勝</th><th class="Py(4px) Ta(c)" title="Losses" data-reactid="60">敗</th><th class="Py(4px) Ta(c)" title="Win Percentage" data-reactid="61">勝率</th><th class="Py(4px) Ta(c) D(n)" title="Games Back" data-reactid="62">勝差</th><th class="Py(4px) Ta(c)" title="Conf Games Back" data-reactid="63">區勝差</th><th class="Py(4px) Ta(c)" title="Home Record" data-reactid="64">主場</th><th class="Py(4px) Ta(c)" title="Division Record" data-reactid="65">分組</th><th class="Py(4px) Ta(c)" title="Conference Record" data-reactid="66">分區</th><th class="Py(4px) Ta(c)" title="Last 10 Record" data-reactid="67">近10場</th><th class="Py(4px) Ta(c)" title="Points For" data-reactid="68">平均得分</th><th class="Py(4px) Ta(c)" title="Points Against" data-reactid="69">平均失分</th><th class="Py(4px) Ta(c)" title="Net Points" data-reactid="70">得分差</th><th class="Py(4px) Ta(c)" title="Streak" data-reactid="71">連勝/敗</th></tr></thead>
    # <th class="Py(4px) Ta(c)" title="Wins" data-reactid="59">勝</th>
    for th in table.find('thead').find_all('th'):
        header = th.text.strip()
        data = data + header + ','
    data = data[:-1] + '\n'

    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        # team name:
        # <a href="/nba/teams/公鹿/" title="公鹿" class="C(primary-text) C(primary-text):link C(primary-text):visited" data-reactid="77">
        # team = tr.find_all('span')[1].text.strip()
        team = tr.find('a').get('title').strip()
        data = data + team + ','

        # score:
        # <td class="Bdb(primary-border) Ta(c)" data-reactid="85">60</td>
        for td in tr.find_all('td'):
            score = td.text.strip()
            data = data + score + ','
        data = data[:-1] + '\n'

        # icon:
        # <img class="JsEnabled_Op(0) JsEnabled_Bg(n) Trsdu(.42s) Bgr(nr) Bgz(cv) Mstart(20px) Mend(10px) Va(m)" height="30" width="30" style="background-image:url(https://s.yimg.com/cv/apiv2/default/nba/20181214/70x70/bucks_wbg.png);" src="https://s.yimg.com/g/images/spaceball.gif" data-reactid="79"/>
        img = tr.find('img')
        path = img.get('style').strip()[21:-2]
        # save icon to file
        req = urllib.request.Request(url=path, headers=headers)
        file = open('nba/icon/' + team + '.png', 'wb')
        file.write(urllib.request.urlopen(req).read())
        file.close()

file = open('nba/nba.txt', 'w', encoding='utf-8')
file.write(data)
file.close()






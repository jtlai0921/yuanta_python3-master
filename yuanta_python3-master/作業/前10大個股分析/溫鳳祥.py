# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥
# Desc: 找出前10大個股日本益比、殖利率及股價淨值比

import tkinter
from tkinter import ttk
import tkinter.messagebox
import bs4
import requests
import urllib.request
from datetime import date, timedelta

padX = 3
padY = 3

headerSeqs = range(7)
headerCodes = ['symb', 'name', 'divy', 'year', 'per', 'pbr', 'yrsn']
headerNames = ['證券代號', '證券名稱', '殖利率(%) ▼', '股利年度', '本益比', '股價淨值比', '財報年/季']
headerSortAsc = [None, None, False, None, None, None, None]
allData = []
sortOnCol = 2
prevSortCol = -1


def cmdFind():
    global allData
    # get input values
    try:
        inDate = enDate.get().strip()
        inDivy = float(enDivy.get().strip())    # 殖利率
        inPER = float(enPER.get().strip())      # 本益比
        inPBR = float(enPBR.get().strip())      # 股價淨值比
    except Exception as ex:
        tkinter.messagebox.showinfo('Error', 'Input data are incorrect')
        return -1

    # get HTML content
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        # url = 'https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU_d.html'
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=html&date={}&selectType=ALL'.format(inDate)
        print('url=%s' % url)
        html = requests.get(url, headers=headers)
        if html.status_code != 200:
            tkinter.messagebox.showinfo('Error', 'Cannot retrieve content from:\n%s' % url)
            return -1

        # clear treeview
        # tree.delete(*tree.get_children())
        for item in tree.get_children():
            tree.delete(item)
        allData = []

        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        tbody = soup.find('table').find('tbody')
        rows = 0
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')

            symb = tds[0].text.strip()  # 證券代號
            name = tds[1].text.strip()  # 證券名稱
            divy = tds[2].text.strip()  # dividend yield(殖利率)
            year = int(tds[3].text.strip())  # 股利年度
            per = tds[4].text.strip()  # PER(本益比)
            pbr = tds[5].text.strip()  # PBR(股價淨值比)
            yrsn = tds[6].text.strip()  # 財報年/季
            # print('[%02d] %s %s %s %d %s %s %s' % (rows, symb, name, divy, year, per, pbr, yrsn))

            # check 殖利率
            if divy == '-':
                fDivy = -1
            else:
                fDivy = float(divy.replace(',', ''))
            if fDivy < inDivy:
                # print('[%02d] %s %s %s %d %s %s %s' % (rows, symb, name, divy, year, per, pbr, yrsn))
                # print('Skip: divy = %s < %f' % (divy, inDivy))
                continue

            # check 本益比
            if per == '-':
                fPer = 999999
            else:
                fPer = float(per.replace(',', ''))
            if fPer > inPER:
                # print('[%02d] %s %s %s %d %s %s %s' % (rows, symb, name, divy, year, per, pbr, yrsn))
                # print('Skip: per = %s > %f' % (per, inPER))
                continue

            # check 股價淨值比
            if pbr == '-':
                fPbr = 999999
            else:
                fPbr = float(pbr.replace(',', ''))
            if fPbr > inPBR:
                # print('[%02d] %s %s %s %d %s %s %s' % (rows, symb, name, divy, year, per, pbr, yrsn))
                # print('Skip: pbr = %s > %f' % (pbr, inPBR))
                continue

            print('[%02d] %s %s %s %d %s %s %s' % (rows, symb, name, divy, year, per, pbr, yrsn))
            rowData = (symb, name, divy, year, per, pbr, yrsn)
            allData.append(rowData)
            rows += 1

        print('Total rows = %d' % rows)
        # sort data then add to the table
        sortAllData(sortOnCol, allData)

    except AttributeError as e:
        tkinter.messagebox.showinfo('Error', 'No data to show, maybe try another date?')
    except Exception as e:
        tkinter.messagebox.showinfo('Error', '{}({})'.format(str(e), type(e)))


def cmdQuit():
    win.quit()


# sort data then add to the table
def sortAllData(col, allData):
    global sortOnCol, headerSortAsc

    if col == 0 or col == 3:  # 證券代號, 股利年度
        allData.sort(key=lambda x: int(x[col]), reverse=not headerSortAsc[col])
    elif col == 1 or col == 6:    # 證券名稱, 財報年/季
        allData.sort(key=lambda x: x[col], reverse=not headerSortAsc[col])
    else:   # 殖利率, 本益比, 股價淨值比
        allData.sort(key=lambda x: 0 if x[col] == '-' else float(x[col]), reverse=not headerSortAsc[col])
    # sortOnCol = col

    # clear table
    # tree.delete(*tree.get_children())
    for item in tree.get_children():
        tree.delete(item)

    # insert into table
    try:
        maxRows = int(enMaxRows.get())
    except:
        maxRows = 10
    for ii in range(len(allData)):
        if ii >= maxRows:
            break
        tree.insert('', 'end', values=allData[ii])


# adjust column header text after clicked on it
def adjustHeader(col):
    global sortOnCol, headerSortAsc
    # remove sort symbol from previous sorted column
    if col != sortOnCol:
        text = tree.heading(headerCodes[sortOnCol], option='text')[:-2]
        tree.heading(headerCodes[sortOnCol], text=text)
    if headerSortAsc[col] is None:  # first time click
        headerSortAsc[col] = True
        text = tree.heading(headerCodes[col], option='text')
    elif col == sortOnCol:  # clicked on the same column header
        headerSortAsc[col] = not headerSortAsc[col]
        text = tree.heading(headerCodes[col], option='text')[:-2]
    else:   # clicked on another column header
        headerSortAsc[col] = True
        text = tree.heading(headerCodes[col], option='text')
    text += (' ▲' if headerSortAsc[col] else ' ▼')
    tree.heading(headerCodes[col], text=text)


# clicked on treeview
def cmdClickTree(event):
    # if clicked on header, do sort according to the clicked column
    global allData, prevSortCol, sortOnCol
    region = tree.identify_region(event.x, event.y)
    if region == 'heading':
        col = int(tree.identify_column(event.x)[1:]) - 1
        adjustHeader(col)
        sortAllData(col, allData)
        prevSortCol = sortOnCol
        sortOnCol = col


if __name__ == '__main__':
    win = tkinter.Tk()
    win.title('前10大個股日本益比、殖利率及股價淨值比')

    tkinter.Label(win, text='日期:').grid(row=0, column=0, padx=padX, pady=padY)
    enDate = tkinter.Entry(win)
    enDate.grid(row=0, column=1, padx=padX, pady=padY, columnspan=1)
    # default to use yesterday as query date
    yest = date.today() - timedelta(days=1)
    enDate.insert(0, yest.strftime('%Y%m%d'))

    tkinter.Label(win, text='殖利率 >=:').grid(row=1, column=0, padx=padX, pady=padY)
    enDivy = tkinter.Entry(win)
    enDivy.grid(row=1, column=1, padx=padX, pady=padY, columnspan=1)
    enDivy.insert(0, '0')

    tkinter.Label(win, text='本益比 <=:').grid(row=2, column=0, padx=padX, pady=padY)
    enPER = tkinter.Entry(win)
    enPER.grid(row=2, column=1, padx=padX, pady=padY, columnspan=1)
    enPER.insert(0, '10.0')

    tkinter.Label(win, text='股價淨值比 <=:').grid(row=3, column=0, padx=padX, pady=padY)
    enPBR = tkinter.Entry(win)
    enPBR.grid(row=3, column=1, padx=padX, pady=padY, columnspan=1)
    enPBR.insert(0, '1.0')

    tkinter.Label(win, text='最大資料筆數:').grid(row=4, column=0, padx=padX, pady=padY)
    enMaxRows = tkinter.Entry(win)
    enMaxRows.grid(row=4, column=1, padx=padX, pady=padY, columnspan=1)
    enMaxRows.insert(0, '10')

    tkinter.Button(win, text='查找', command=cmdFind).grid(row=5, column=0, padx=padX, pady=padY)
    tkinter.Button(win, text='關閉', command=cmdQuit).grid(row=5, column=1, padx=padX, pady=padY)

    tree = ttk.Treeview(win, columns=headerCodes, show='headings')
    for ii in headerSeqs:
        tree.column(headerCodes[ii], width=100, anchor='center')
        tree.heading(headerCodes[ii], text=headerNames[ii])
    tree.grid(row=6, column=0, padx=padX, pady=padY, columnspan=2)
    tree.bind('<ButtonRelease-1>', cmdClickTree)

    win.mainloop()

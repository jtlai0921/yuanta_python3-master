import tkinter
import tkinter.simpledialog
from tkinter import ttk
import requests
import json
import sys
from tkinter import messagebox
import datetime
import time


def btn_search_click():
    if date.get() == '' and yield_rate.get() == '' and per.get() == '' and pbr.get() == '':
        messagebox.showerror('錯誤', '請輸入查詢條件')
    else:
        tree_clear()
        search()


# 清空tree
def tree_clear():
    items = tree.get_children()
    [tree.delete(item) for item in items]


# 查詢
def search():
    url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={0}&selectType=ALL'
    # 沒給日期就用今天
    if date.get() == '':
        url = url.format(datetime.date.today())
    else:
        url = url.format(date.get())

    resp = requests.get(url)
    if resp.status_code == 200:
        text = resp.text
        list = text.split('\n')
        # print(text)
        i = 2  # 前兩項是沒用的資料
        while i < len(list):
            # print(list[i])
            list[i] = list[i].replace('"', '')
            data = list[i].split(',')
            if len(data) < 7:
                pass
            # 殖利率(%)
            elif yield_rate.get() != '' and data[2] != yield_rate.get():
                pass
            # 本益比
            elif per.get() != '' and data[4] != per.get():
                pass
            # 股價淨值比
            elif pbr.get() != '' and data[5] != pbr.get():
                pass
            else:
                tree.insert('', 'end', values=data)
            i = i + 1

    messagebox.showinfo('GUI作業', '查詢完成')


def quit():
    win.quit()


win = tkinter.Tk()
# 視窗抬頭
win.title("GUI作業")
# 視窗大小
win.geometry("750x400")

tkinter.Label(win, text="日期").grid(row=0)
tkinter.Label(win, text="殖利率").grid(row=1)
tkinter.Label(win, text="本益比").grid(row=2)
tkinter.Label(win, text="股價淨值比").grid(row=3)

date = tkinter.Entry(win)  # 日期
yield_rate = tkinter.Entry(win)  # 殖利率
per = tkinter.Entry(win)  # 本益比
pbr = tkinter.Entry(win)  # 股價淨值比

date.grid(row=0, column=1, columnspan=2)
yield_rate.grid(row=1, column=1, columnspan=2)
per.grid(row=2, column=1, columnspan=2)
pbr.grid(row=3, column=1, columnspan=2)

btn_search = tkinter.Button(win, text="查詢", command=btn_search_click)
btn_search.grid(row=4, column=0)
btn_close = tkinter.Button(win, text="關閉", command=quit)
btn_close.grid(row=4, column=1)

# Treeview
tree = ttk.Treeview(win, columns=['1', '2', '3', '4', '5', '6', '7'], show='headings')
tree.column('1', width=100, anchor='center')
tree.column('2', width=100, anchor='center')
tree.column('3', width=100, anchor='center')
tree.column('4', width=100, anchor='center')
tree.column('5', width=100, anchor='center')
tree.column('6', width=100, anchor='center')
tree.column('7', width=100, anchor='center')
tree.heading('1', text='證券代號')
tree.heading('2', text='證券名稱')
tree.heading('3', text='殖利率(%)')
tree.heading('4', text='股利年度')
tree.heading('5', text='本益比')
tree.heading('6', text='股價淨值比')
tree.heading('7', text='財報年/季')
# tree.bind('<ButtonRelease-1>', click) # 綁定事件
# tree.bind('<Key>', keydown) # 綁定事件
tree.grid(row=5, column=0, columnspan=7)

# 設定Scrollbar
vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.place(x=700, y=130, height=200 + 30)
tree.configure(yscrollcommand=vsb.set)

win.mainloop()
import requests
import pandas as pd
import tkinter
from io import StringIO
from tkinter import ttk


def df_from_csv(date):
    url = str.format('https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={0}&selectType=ALL', date)
    
    txt = requests.get(url).text
    txt = txt[txt.find('\n')+1:]
    xls = pd.read_csv(StringIO(txt))
    columns = xls.columns.tolist()
    cols_to_use = columns[:len(columns)-1]
    xls = pd.read_csv(StringIO(txt), usecols=cols_to_use)
    xls = xls.dropna()
    df = pd.DataFrame(xls)
    return df


def search_cmd():
    if len(text1.get()) < 8 or len(text1.get()) > 8:
        print('Date error')
        return

    try:
        value1 = int(text1.get())
        value2 = float(text2.get())
        value3 = float(text3.get())
        value4 = float(text4.get())
    except ValueError:
        print("Input error")
        return
    
    for i in tree.get_children():
        tree.delete(i)
        
    df = df_from_csv(value1)
    df = df[(df['本益比'] != '-')]
    df = df.replace(',', '', regex=True).astype({'殖利率(%)': float, '本益比': float, '股價淨值比': float})
    df = df[(df['殖利率(%)'] >= float(value2)) & (df['本益比'] <= float(value3)) & (df['股價淨值比'] <= float(value4))]
    
    df_col = df.columns.values

    tree["columns"] = df_col

    for x in range(len(df_col)):
        tree.column(x, width=100)
        tree.heading(x, text=df_col[x])

    for i in range(len(df)):
        tree.insert('', i, values=df.iloc[i, :].tolist())


def cancel_cmd():
    win.quit()


win = tkinter.Tk()
win.title("前十大個股日本益比、殖利率及股價淨值比")

tkinter.Label(win, text="日期").grid(row=0)
tkinter.Label(win, text="殖利率").grid(row=1)
tkinter.Label(win, text="本益比").grid(row=2)
tkinter.Label(win, text="股價淨值比").grid(row=3)

text1 = tkinter.Entry(win, justify=tkinter.CENTER)
text2 = tkinter.Entry(win, justify=tkinter.CENTER)
text3 = tkinter.Entry(win, justify=tkinter.CENTER)
text4 = tkinter.Entry(win, justify=tkinter.CENTER)

text1.grid(row=0, column=1, columnspan=2)
text2.grid(row=1, column=1, columnspan=2)
text3.grid(row=2, column=1, columnspan=2)
text4.grid(row=3, column=1, columnspan=2)

button1 = tkinter.Button(win, text="查找", command=search_cmd)
button1.grid(row=4, column=0)
button2 = tkinter.Button(win, text="關閉", command=cancel_cmd)
button2.grid(row=4, column=2)

tree = ttk.Treeview(win)
tree.grid(row=5, column=0, columnspan=4)

win.mainloop()

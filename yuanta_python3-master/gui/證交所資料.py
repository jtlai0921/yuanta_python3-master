import requests
import tkinter
from  tkinter import ttk

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=%s&selectType=ALL'
url = url % '20190621'
csv = requests.get(url, headers=headers)

print(csv.text)

win = tkinter.Tk()
win.title("前10大個股日本益比、殖利率及股價淨值比")

tkinter.Label(win, text="日期").grid(row=0)
tkinter.Label(win, text="殖利率").grid(row=1)
tkinter.Label(win, text="本益比").grid(row=2)
tkinter.Label(win, text="股價淨值比").grid(row=3)

date  = tkinter.Entry(win, justify=tkinter.LEFT)
dy = tkinter.Entry(win, justify=tkinter.RIGHT)
pe = tkinter.Entry(win, justify=tkinter.RIGHT)
pbr = tkinter.Entry(win, justify=tkinter.RIGHT)

tree = ttk.Treeview(win, columns=['1','2','3','4','5','6','7'], show='headings', padding=0)
tree.column('1',width=100, anchor='center')
tree.column('2',width=100, anchor='center')
tree.column('3',width=100, anchor='center')
tree.column('4',width=100, anchor='center')
tree.column('5',width=100, anchor='center')
tree.column('6',width=100, anchor='center')
tree.column('7',width=100, anchor='center')
tree.heading('1', text='證券代號')
tree.heading('2', text='證券名稱')
tree.heading('3', text='殖利率(%)')
tree.heading('4', text='股利年度')
tree.heading('5', text='本益比')
tree.heading('6', text='股價淨值比')
tree.heading('7', text='財報年/季')
tree.grid()


date.grid(row=0, column=1, columnspan=2)
dy.grid(row=1, column=1, columnspan=2)
pe.grid(row=2, column=1, columnspan=2)
pbr.grid(row=3, column=1, columnspan=2)

button1 = tkinter.Button(win, text="查找")
button1.grid(row=4, column=0)
button2 = tkinter.Button(win, text="關閉")
button2.grid(row=4, column=1)

tree.grid(row=5, column=0, columnspan=3, padx=4, pady=4)


win.mainloop()
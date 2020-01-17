import tkinter
import tkinter.ttk as ttk
# from tkinter import ttk
import tkinter.messagebox
import requests
import datetime
import os

url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=%d&selectType=ALL"


def findBtnClicked():
    try:
        entry1Value = int(entry1.get())
        entry2Value = float(entry2.get())
        entry3Value = float(entry3.get())
        entry4Value = float(entry4.get())
    except BaseException as e:
        tkinter.messagebox.showinfo("欄位資料內容錯誤", e)
        return

    global lastDataDate
    global dataLines
    if entry1Value != lastDataDate:
        try:
            cacheFilePath = "BWIBBU_d\\" + str(entry1Value) + ".data"
            # 是否存在快取檔中
            if os.path.exists(cacheFilePath):
                file = open(cacheFilePath, "r", encoding="utf-8")
                dataLines = file.readlines()
                print("載入快取檔" + cacheFilePath + "，資料行數" + str(len(dataLines)))
            else:
                print("url=" + (url % entry1Value))
                req = requests.get(url % entry1Value)
                if req.status_code == 200:
                    dataLines = req.text.split('\n')
                    if len(dataLines) < 10:
                        raise Exception("無 " + str(entry1Value) + " 資料")
                    lastDataDate = entry1Value
                    print("載入遠端資料，資料行數" + str(len(dataLines)))

                    # 寫入快取
                    try:
                        file = open(cacheFilePath, "w", encoding="utf-8")
                        file.writelines(dataLines)
                        print("已寫入快取" + cacheFilePath)
                    except BaseException as e:
                        os.remove(cacheFilePath)
                        print("快取檔寫入失敗，" + e)
                else:
                    tkinter.messagebox.showinfo("資料載入失敗", "Status Code = %d".format(req.status_code))
                    return
        except BaseException as e:
            tkinter.messagebox.showinfo("資料載入失敗", e)
            return

    for p in tree.get_children():
        tree.delete(p)
    skipline = 0
    for oneline in dataLines:
        if skipline < 2:
            if skipline == 0:
                oneline = oneline.replace("\"", "")
                win.title("前10大個股日本益比、殖利率及股價淨值比(" + oneline.split(" ")[0] + ")")
            skipline += 1
            continue
        elif oneline.strip() == '""':
            break
        # print(oneline)
        fields = tuple(v.replace("\"", "") for v in oneline.split(","))
        try:
            if float(fields[2]) >= entry2Value and float(fields[4]) <= entry3Value and float(fields[5]) <= entry4Value:
                tree.insert("", "end", values=fields)
        except BaseException as e:
            print("%s 資料異常 %s" % (oneline.strip(), e))


def closeBtnClicked():
    win.quit()


def sort_column(tv, col):
    sortAsc = heading[col]["sortAsc"]
    # print(tv, col, sortAsc)
    sortAsc = not sortAsc
    heading[col]["sortAsc"] = sortAsc

    for key in heading.keys():
        tv.heading(key, text=heading[key]["Name"] + (("▲" if sortAsc else "▼") if key == col else ""))

    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    if col == "2" or col == "7":
        l.sort(key=lambda t: t[0], reverse=not sortAsc)
    else:
        l.sort(key=lambda t: float(t[0]), reverse=not sortAsc)
    #      ^^^^^^^^^^^^^^^^^^^^^^^
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)


lastDataDate = None
dataLines = None
heading = {"1" : {"Name" : "證券代號", "sortAsc" : True},
    "2" : {"Name" : "證券名稱", "sortAsc" : True},
    "3" : {"Name" : "殖利率(%)", "sortAsc" : True},
    "4" : {"Name" : "股利年度", "sortAsc" : True},
    "5" : {"Name" : "本益比", "sortAsc" : True},
    "6" : {"Name" : "股價淨值比", "sortAsc" : True},
    "7" : {"Name" : "財報年/季", "sortAsc" : True}}


if not os.path.exists("BWIBBU_d"):
    os.makedirs("BWIBBU_d")

win = tkinter.Tk()
win.title("前10大個股日本益比、殖利率及股價淨值比")
win.geometry("800x600")

panel1 = tkinter.Frame(win)
panel1.pack(fill=tkinter.BOTH)
panel1.pack_propagate(False)

panel1.rowconfigure((0, 1, 2, 3, 4), weight=1)
panel1.columnconfigure((0, 1), weight=1)

label1 = tkinter.Label(panel1, text="日期")
label1.grid(row=0, column=0, pady=(5, 0))

entry1 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry1.grid(row=0, column=1, pady=(5, 0))
entry1.insert(0, str(datetime.datetime.today().date()).replace("-", ""))

label2 = tkinter.Label(panel1, text="殖利率 >=")
label2.grid(row=1, column=0, pady=(5, 0))

entry2 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry2.grid(row=1, column=1, pady=(5, 0))
entry2.insert(0, "5.0")

label3 = tkinter.Label(panel1, text="本益比 <=")
label3.grid(row=2, column=0, pady=(5, 0))

entry3 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry3.grid(row=2, column=1, pady=(5, 0))
entry3.insert(0, "5.0")

label4 = tkinter.Label(panel1, text="股價淨值比 <=")
label4.grid(row=3, column=0, pady=(5, 0))

entry4 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry4.grid(row=3, column=1, pady=(5, 0))
entry4.insert(0, "1.0")

findBtn = tkinter.Button(panel1, text="查找", command=findBtnClicked)
findBtn.grid(row=4, column=0, pady=(5, 5))

closeBtn = tkinter.Button(panel1, text="關閉", command=closeBtnClicked)
closeBtn.grid(row=4, column=1, pady=(5, 5))

panel2 = tkinter.Frame(win, relief="sunken", borderwidth=3)
panel2.pack(fill=tkinter.BOTH, expand=True)
panel2.pack_propagate(False)

tree = ttk.Treeview(panel2, columns=tuple(key for key in heading.keys()), show="headings")
for key in heading.keys():
    tree.column(key, width=100, anchor="center")
    tree.heading(key, text=heading[key]["Name"], command=lambda v=key: sort_column(tree, v))

tree.pack(fill=tkinter.BOTH, expand=True)
tree.pack_propagate(False)

win.mainloop()

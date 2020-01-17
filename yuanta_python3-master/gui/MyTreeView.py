import tkinter
from  tkinter import ttk  #匯入內部包

win = tkinter.Tk()
tree = ttk.Treeview(win)#表格

tree["columns"]=("姓名","年齡","身高")
tree.column("姓名", width=100)   #表示列,不顯示
tree.column("年齡", width=100)
tree.column("身高", width=100)

tree.heading("姓名", text="姓名-name")  #顯示錶頭
tree.heading("年齡", text="年齡-age")
tree.heading("身高", text="身高-tall")

# insert(parent, index, iid=None, **kw)
# parent is the item ID of the parent item, or the empty string to create a new top-level item
tree.insert("", 0, text="line1" ,values=("A","21","160")) #插入資料，
tree.insert("", 1, text="line1" ,values=("B","22","161"))
tree.insert("", 2, text="line1" ,values=("C","23","162"))
tree.insert("", 3, text="line1" ,values=("D","24","163"))
tree.pack()


def click(event):  # 单击
    print('Click')
    item = tree.selection()[0]
    item_text = tree.item(item, "values")
    print(item_text[0])  # 输出所选行的第一列的值


def keydown(event):  # 单击
    print(event)
    item = tree.selection()[0]
    if event.char == 'd':  # 刪除
        tree.delete(item)
    elif event.char == 'e':  # 修改
        tree.item(item, text="line1", values=("z", "30", "170"))
    elif event.char == 'c':  # 清除
        for item in tree.get_children():
            tree.delete(item)


# ButtonPress-1、Double-Button-1
tree.bind('<ButtonRelease-1>', click)  # 綁定事件
tree.bind('<Key>', keydown)


win.mainloop()
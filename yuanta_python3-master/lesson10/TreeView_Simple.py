import tkinter
from tkinter import ttk

def click(event): # Click
    item = tree.selection()[0]
    item_text = tree.item(item, "values")
    print(item_text[0]) # 第一欄的資料

def keydown(event): # Click
    print(event)
    item = tree.selection()[0]
    if event.char == 'd':  # 刪除
        tree.delete(item)
    elif event.char == 'e':  # 修改
        tree.item(item, text="line1", values=("z", "30", "170"))
    elif event.char == 'c':  # 清除
        for item in tree.get_children():
            tree.delete(item)

data1 = ['Vincent','12','男']
data2 = ['Anita','13','女']

win = tkinter.Tk()
tree = ttk.Treeview(win, columns=['1','2','3'], show='headings')
tree.column('1', width=100, anchor='center')
tree.column('2', width=100, anchor='center')
tree.column('3', width=100, anchor='center')
tree.heading('1', text='姓名')
tree.heading('2', text='年齡')
tree.heading('3', text='性别')
tree.insert('', 'end', values=data1) # end 最後一筆，0 第一筆
tree.insert('', 'end', values=data2) # end 最後一筆，0 第一筆

tree.bind('<ButtonRelease-1>', click) # 綁定事件
tree.bind('<Key>', keydown) # 綁定事件

tree.grid()


win.mainloop()
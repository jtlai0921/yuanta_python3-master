import tkinter

value = 0

def update():
    global value # 把宣告在第 3 行的 value 視為全域變數
    value += 1
    var.set(str(value))

win = tkinter.Tk()
win.geometry("100x50")
var = tkinter.StringVar() # 字串參照物件
label = tkinter.Label(win, textvariable=var)
var.set(str(value))
label.pack()
button1 = tkinter.Button(win, text="ADD", command=update)
button1.pack()
win.mainloop()
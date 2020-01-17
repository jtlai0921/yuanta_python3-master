import tkinter
import tkinter.simpledialog

def setStr():
    r = tkinter.simpledialog.askstring('輸入視窗', '請輸入字串', initialvalue='')
    label.config(text=r)

def setInt():
    r = tkinter.simpledialog.askinteger('輸入視窗', '請輸入整數', initialvalue='')
    label.config(text=str(r))

def setFloat():
    r = tkinter.simpledialog.askfloat('輸入視窗', '請輸入浮點數', initialvalue='')
    label.config(text=str(r))


win = tkinter.Tk()
label = tkinter.Label(win, text="您輸入的是...")
label.pack()

button1 = tkinter.Button(win, text="輸入字串", command=setStr)
button1.pack(side=tkinter.LEFT)
button2 = tkinter.Button(win, text="輸入整數", command=setInt)
button2.pack(side=tkinter.LEFT)
button3 = tkinter.Button(win, text="輸入浮點數", command=setFloat)
button3.pack(side=tkinter.RIGHT)

win.mainloop()
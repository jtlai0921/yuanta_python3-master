import tkinter

win = tkinter.Tk() # 視窗抬頭
win.title("tk")

# 佈局
label = tkinter.Label(win, text="Hello !")
label.config(font=("Courier", 44))

label.pack()
button1 = tkinter.Button(win, text="OK")
button1.pack(side=tkinter.LEFT)
button2 = tkinter.Button(win, text="Cancel")
button2.pack(side=tkinter.RIGHT)

# 視窗大小
win.geometry("200x100")
win.mainloop()

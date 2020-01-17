import tkinter


def ok_cmd():
    print('ok_cmd')


def cancel_cmd():
    print('cancel_cmd')
    win.quit()


win = tkinter.Tk()
win.title("tk")
win.geometry("200x200")
label = tkinter.Label(win, text="Hello !")
label.pack()

button1 = tkinter.Button(win, text="OK", command=ok_cmd)
button1.pack(side=tkinter.LEFT)

button2 = tkinter.Button(win, text="Cancel", command=cancel_cmd)
button2.pack(side=tkinter.RIGHT)

win.mainloop()

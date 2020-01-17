import tkinter
import tkinter.simpledialog

win = tkinter.Tk()
tkinter.Label(win, text="身高").grid(row=0)
tkinter.Label(win, text="體重").grid(row=1)

height = tkinter.Entry(win)
weight = tkinter.Entry(win)

height.grid(row=0, column=1)
weight.grid(row=1, column=1)

win.mainloop()

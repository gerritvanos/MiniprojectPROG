from tkinter import *
root = Tk()
label = Label(master=root,
 text='Hello World',
 background='yellow',
 foreground='blue',
 font=('Helvetica', 16, 'bold italic'),
 width=14,
 height=3)
label.pack()

button = Button(master=root, text='druk hier', command=start)
root.mainloop()

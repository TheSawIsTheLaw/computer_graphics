from tkinter import *

rootWindow = Tk()
rootWindow.minsize(1880, 1080)

helloLabel = Label(rootWindow, text="Задание:", font=("Consolas", 14), width=20)
helloLabel.pack() # side=TOP, padx=10, pady=10

rootWindow.mainloop()
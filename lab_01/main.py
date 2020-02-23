from tkinter import *

def printDebug():
    print('666')

def makeJobWindow():
    jobWindow = Tk()

    jobWindow.minsize(400, 400)
    jobLabel = Label(jobWindow, text="На плоскости даны два...")
    jobLabel.pack()

    jobWindow.mainloop()

def makeCascadeMenu(rootWindow):
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu=rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label='Формулировка', command=makeJobWindow)
    moreMenu = Menu(rootMenu)
    moreMenu.add_command(label='Сбросить всё', command=printDebug)

    rootMenu.add_cascade(label='Задание', menu=jobMenu)
    rootMenu.add_cascade(label='Дополнительные возможности', menu=moreMenu)

def makeMainWindow():
    rootWindow = Tk()
    rootWindow.minsize(1880, 1080)

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()

makeMainWindow()
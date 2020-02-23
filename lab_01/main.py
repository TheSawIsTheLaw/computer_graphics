from tkinter import *

def printDebug():
    print('666')

def makeJobWindow():
    jobWindow = Tk()

    jobWindow.minsize(400, 200)
    jobWindow.title("Формулировка задания")
    jobLabel = Label(jobWindow,
                     text="На плоскости даны два множества точек.\n"
                          "Найти пару треугольников (каждый треугольник\n"
                          "в качестве вершин имеет три различные точки\n"
                          "одного и того же множества; треугольников стоятся\n"
                          "на точках разных множеств) таких, что прямая, соединяющая\n"
                          "точки пересечения высот, образует минимальный угол с осью\n"
                          "абсцисс.",
                     font=('consolas', 20))
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
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1080)

    makeCascadeMenu(rootWindow)

    boolVar = BooleanVar()
    boolVar.set(0)
    radioButtonF = Radiobutton(text='Треугольник строится на точках одного множества', font=("consolas", 12), variable=boolVar, value=0, command=printDebug).grid(row=0, column=0, columnspan=3)
    radioButtonS = Radiobutton(text='Треугольник строится на точках разных множеств', font=("consolas", 12), variable=boolVar, value=1, command=printDebug).grid(row=1, column=0, columnspan=3)

    listLableFirst = Label(rootWindow, text="Множество 1:", font=("consolas", 20), fg="white", bg="black").grid(row=2, column=0, columnspan=2)

    listBoxFirst = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxFirst.insert(0, "0, 0.11")
    listBoxFirst.grid(row=2, column=2, columnspan=2, rowspan=5)
    listBoxFirst.insert(0, 0)
    entryFirstLable = Label(rootWindow, text="Добавляемая в первое множество вершина:")
    entryFirstLable.grid(row=3, column=0)
    entryFirst = Entry(rootWindow)
    entryFirst.grid(row=3, column=1)
    insertButtonFirst = Button(rootWindow, text="Добавить", width=30)
    insertButtonFirst.grid(row=4, column=0, columnspan=2)
    delButtonFirst = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 1)")
    delButtonFirst.grid(row=5, column=0, columnspan=2)

    listLableSecond = Label(rootWindow, text="Множество 2:", font=("consolas", 20), fg="white", bg="black").grid(row=7, column=0, columnspan=2)
    listBoxSecond = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxSecond.grid(row=7, column=2, columnspan=2, rowspan=5)
    entrySecondLable = Label(rootWindow, text="Добавляемая во второе множество вершина:")
    entrySecondLable.grid(row=8, column=0)
    entrySecond = Entry(rootWindow)
    entrySecond.grid(row=8, column=1)
    insertButtonSecond = Button(rootWindow, text="Добавить", width=30)
    insertButtonSecond.grid(row=9, column=0, columnspan=2)
    delButtonSecond = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 2)")
    delButtonSecond.grid(row=10, column=0, columnspan=2)

    rootWindow.mainloop()

makeMainWindow()
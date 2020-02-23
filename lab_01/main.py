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

def makeCanvasStart(canvasWindow):
    canvasWindow.delete("all")
    canvasWindow.grid(row=0, column=4, rowspan=16)
    canvasWindow.create_line(0, 0, 1003, 0, width=5, fill="black")  # Тут можно добавить +5 -5
    canvasWindow.create_line(1003, 0, 1003, 1000, width=5, fill="black")
    canvasWindow.create_line(1003, 1003, 0, 1003, width=5, fill="black")
    canvasWindow.create_line(0, 0, 0, 1003, width=5, fill="black")

    # Начальные Оси
    canvasWindow.create_line(500, 1000, 500, 0, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_line(0, 500, 1000, 500, width=3, arrow=LAST, arrowshape="10 20 10")

    for i in range(0, 1100, 100):
        canvasWindow.create_line(495, i, 505, i, width=3)
        if (500 - i):
            canvasWindow.create_text(525, i - 10, text=str(500 - i), font=("consolas", 9))
            canvasWindow.create_text(i + 15, 485, text=str(-500 + i), font=("consolas", 9))
        canvasWindow.create_line(i, 495, i, 505, width=3)

    canvasWindow.create_text(525, 485, text="0")



def makeMainWindow():
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1080)

    makeCascadeMenu(rootWindow)

    boolVar = BooleanVar()
    boolVar.set(0)
    radioButtonF = Radiobutton(text='Треугольник строится на точках одного множества', font=("consolas", 12), variable=boolVar, value=0, command=printDebug).grid(row=0, column=0, columnspan=3)
    radioButtonS = Radiobutton(text='Треугольник строится на точках разных множеств', font=("consolas", 12), variable=boolVar, value=1, command=printDebug).grid(row=1, column=0, columnspan=3)

    listLableFirst = Label(rootWindow, text="Множество 1:", font=("consolas", 20), fg="white", bg="black").grid(row=3, column=0, columnspan=2)

    listBoxFirst = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxFirst.insert(0, "0, 0.11")
    listBoxFirst.grid(row=4, column=2, columnspan=2, rowspan=5)
    listBoxFirst.insert(0, 0)
    entryFirstLable = Label(rootWindow, text="Добавляемая в первое множество вершина:")
    entryFirstLable.grid(row=5, column=0)
    entryFirst = Entry(rootWindow)
    entryFirst.grid(row=5, column=1)
    insertButtonFirst = Button(rootWindow, text="Добавить", width=30)
    insertButtonFirst.grid(row=6, column=0, columnspan=2)
    delButtonFirst = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 1)")
    delButtonFirst.grid(row=7, column=0, columnspan=2)
    changeButtonFirst = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 1)")
    changeButtonFirst.grid(row=8, column=0, columnspan=2)

    emptyLabel1 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                        "----------------------------------------------")
    emptyLabel2 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                         "----------------------------------------------")
    emptyLabel1.grid(row=9, columnspan=3)
    emptyLabel2.grid(row=2, columnspan=3)
    listLableSecond = Label(rootWindow, text="Множество 2:", font=("consolas", 20), fg="white", bg="black").grid(row=10, column=0, columnspan=2)
    listBoxSecond = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxSecond.grid(row=11, column=2, columnspan=2, rowspan=5)
    entrySecondLable = Label(rootWindow, text="Добавляемая во второе множество вершина:")
    entrySecondLable.grid(row=12, column=0)
    entrySecond = Entry(rootWindow)
    entrySecond.grid(row=12, column=1)
    insertButtonSecond = Button(rootWindow, text="Добавить", width=30)
    insertButtonSecond.grid(row=13, column=0, columnspan=2)
    delButtonSecond = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 2)")
    delButtonSecond.grid(row=14, column=0, columnspan=2)
    changeButtonSecond = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 2)")
    changeButtonSecond.grid(row=15, column=0, columnspan=2)

    startButton = Button(rootWindow, text="Исполнить \nпредначертанное!", font=("consolas", 20), bg="yellow", fg="blue")
    startButton.grid(row=0, column=5, rowspan=2)

    canvasWindow = Canvas(rootWindow, bg="white", width=997, height=1000)
    makeCanvasStart(canvasWindow)

    #canvasWindow.delete("all")

    rootWindow.mainloop()

makeMainWindow()
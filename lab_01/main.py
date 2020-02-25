from tkinter import *
from re import *

def masst(x, y, xmin, ymax, k, xn, yn, kx, ky):
    kx = rd(xn + (x - xmin)*k) # Промасштабированный x
    ky = rd(yn + (ymax - y)*k) # Промасштабированный y

def masstX(x, xmin, k, xn = 10):
    return rd(xn + (x - xmin)*k) # Промасштабированный x

def masstY(y, ymax, k, yn = 10):
    return rd(yn + (ymax - y)*k) # Промасштабированный y

def rd(x,y=0):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1'+'0'*y) # multiplier - how many positions to the right
    q = x*m # shift to the right by multiplier
    c = int(q) # new number
    i = int( (q-c)*10 ) # indicator number on the right
    if i >= 5:
        c += 1
    return c/m

def printDebug(var):
    print(var)

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

    # Начальные Оси
    canvasWindow.create_line(500, 1000, 500, 0, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_line(0, 500, 1000, 500, width=3, arrow=LAST, arrowshape="10 20 10")

    for i in range(100, 1000, 100):
        canvasWindow.create_line(495, i, 505, i, width=3)
        if (500 - i):
            canvasWindow.create_text(525, i - 10, text=str(500 - i), font=("consolas", 9))
            canvasWindow.create_text(i + 15, 485, text=str(-500 + i), font=("consolas", 9))
        canvasWindow.create_line(i, 495, i, 505, width=3)

    canvasWindow.create_text(525, 485, text="0")

def reRenderCanvas(canvasWindow, pointArrayF, pointArrayS):
    canvasWindow.delete("all")

    if len(pointArrayF) + len(pointArrayS) == 0:
        makeCanvasStart(canvasWindow)
        return
    try:
        maxX = pointArrayS[0][0]
        minX = pointArrayS[0][0]
    except IndexError:
        maxX = pointArrayF[0][0]
        minX = pointArrayF[0][0]

    try:
        maxY = pointArrayS[0][1]
        minY = pointArrayS[0][1]
    except IndexError:
        maxY = pointArrayF[0][1]
        minY = pointArrayF[0][1]

    for i in pointArrayS:
        if i[0] > maxX:
            maxX = i[0]
        if i[0] < minX:
            minX = i[0]
        if i[1] > maxY:
            maxY = i[1]
        if i[1] < minY:
            minY = i[1]
    for i in pointArrayF:
        if i[0] > maxX:
            maxX = i[0]
        if i[0] < minX:
            minX = i[0]
        if i[1] > maxY:
            maxY = i[1]
        if i[1] < minY:
            minY = i[1]

    global k
    try:
        kx = 1000 / (maxX - minX)
    except ZeroDivisionError:
        kx = float("inf")
    try:
        ky = 1000 / (maxY - minY)
    except ZeroDivisionError:
        ky = float("inf")
    k = min(kx, ky)
    if len(pointArrayF) + len(pointArrayS) == 1:
        k = 1
        minX = minX - 500
        maxY = maxY + 500
    #print(minX, maxY)
    for i in pointArrayF:
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill="Blue")
        canvasWindow.create_text(x + 10, y + 10, text=str(i[0])+" "+str(i[1]))

    for i in pointArrayS:
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill="Red")
        canvasWindow.create_text(x + 10, y + 10, text=str(i[0])+" "+str(i[1]))

    canvasWindow.create_line(masstX(0, minX, k), 1015, masstX(0, minX, k), 0, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_line(0, masstY(0, maxY, k), 1015, masstY(0, maxY, k), width=3, arrow=LAST, arrowshape="10 20 10")

def generateInputErrorWindow():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow, text="Должно быть введено два вещественных значения в следующем формате"
                                         ":\n'x y'\nПовторите попытку, пожалуйста.", font=("consolas", 15))
    errorLabel.pack()

def generateInputRepeatErrorWindow():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Значения уже имеются в таблице.",
                       font=("consolas", 15))
    errorLabel.pack()

def addPoint(pointArray, entry, listBox, dotIndex, canvasWindow, secPointArray):
    inputString = entry.get()
    inputString = findall(r"[-+]?\d*\.?\d+|[-+]?\d*\.?\d+", inputString)
    for i in range(len(inputString)):
        inputString[i] = float(inputString[i])
    #print(inputString)
    if len(inputString) != 2:
        generateInputErrorWindow()
        return 3
    if inputString not in pointArray:
        listBox.insert(dotIndex, "X = " + str(inputString[0]) + "; Y = " + str(inputString[1]))
        pointArray.insert(dotIndex, inputString)
    else:
        generateInputRepeatErrorWindow()
        return 3

    reRenderCanvas(canvasWindow, pointArray, secPointArray)
    print(pointArray)

def generateEmptyError():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Не выбрано ни одного значения в таблице!",
                       font=("consolas", 15))
    errorLabel.pack()

def deletePoint(pointArray, listBox, canvasWindow, secPointArray):
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]

    listBox.delete(delNum)
    pointArray.pop(delNum)
    print(pointArray)
    reRenderCanvas(canvasWindow, pointArray, secPointArray)

def changePoint(pointArray, entry, listBox, canvasWindow, secPointArray):
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]
    if addPoint(pointArray, entry, listBox, delNum + 1, canvasWindow, secPointArray) != 3:
        deletePoint(pointArray, listBox, canvasWindow, secPointArray)
    print(pointArray)

def makeVarZero(var):
    var = 0

def makeVarOne(var):
    var = 1

def makeMainWindow():
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1000)

    makeCascadeMenu(rootWindow)
    firstDotsArray = []
    secondDotsArray = []

    boolVar = BooleanVar()
    choiceVar = 0
    boolVar.set(0)
    radioButtonF = Radiobutton(text='Треугольник строится на точках одного множества', font=("consolas", 12),
                               variable=boolVar, value=0, command=lambda: makeVarZero(choiceVar)).grid(row=0,
                                                                                                       column=0,
                                                                                                       columnspan=3)
    radioButtonS = Radiobutton(text='Треугольник строится на точках разных множеств', font=("consolas", 12),
                               variable=boolVar, value=1, command=lambda: makeVarOne(choiceVar)).grid(row=1,
                                                                                                      column=0,
                                                                                                      columnspan=3)

    listLableFirst = Label(rootWindow, text="Множество 1:", font=("consolas", 20), fg="white",
                           bg="black").grid(row=3,
                                            column=0,
                                            columnspan=2)

    listBoxFirst = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxFirst.grid(row=4, column=2, columnspan=2, rowspan=5)
    entryFirstLable = Label(rootWindow, text="Координаты вершины (x, y через пробел):")
    entryFirstLable.grid(row=5, column=0)
    entryFirst = Entry(rootWindow)
    entryFirst.grid(row=5, column=1)
    insertButtonFirst = Button(rootWindow, text="Добавить", width=30, command=lambda: addPoint(firstDotsArray,
                                                                                               entryFirst,
                                                                                               listBoxFirst,
                                                                                               listBoxFirst.size() + 1,
                                                                                               canvasWindow, secondDotsArray))
    insertButtonFirst.grid(row=6, column=0, columnspan=2)
    delButtonFirst = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 1)",
                            command=lambda: deletePoint(firstDotsArray, listBoxFirst, canvasWindow, secondDotsArray))
    delButtonFirst.grid(row=7, column=0, columnspan=2)
    changeButtonFirst = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 1)",
                               command=lambda: changePoint(firstDotsArray, entryFirst, listBoxFirst, canvasWindow,
                                                           secondDotsArray))
    changeButtonFirst.grid(row=8, column=0, columnspan=2)

    emptyLabel1 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                         "----------------------------------------------")
    emptyLabel2 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                         "----------------------------------------------")
    emptyLabel1.grid(row=9, columnspan=3)
    emptyLabel2.grid(row=2, columnspan=3)
    listLableSecond = Label(rootWindow, text="Множество 2:", font=("consolas", 20), fg="white",
                            bg="black").grid(row=10,
                                             column=0,
                                             columnspan=2)
    listBoxSecond = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxSecond.grid(row=11, column=2, columnspan=2, rowspan=5)
    entrySecondLable = Label(rootWindow, text="Координаты вершины (x, y через пробел):")
    entrySecondLable.grid(row=12, column=0)
    entrySecond = Entry(rootWindow)
    entrySecond.grid(row=12, column=1)
    insertButtonSecond = Button(rootWindow, text="Добавить", width=30, command=lambda: addPoint(secondDotsArray,
                                                                                                entrySecond,
                                                                                                listBoxSecond,
                                                                                                listBoxSecond.size() + 1,
                                                                                                canvasWindow, firstDotsArray))
    insertButtonSecond.grid(row=13, column=0, columnspan=2)
    delButtonSecond = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 2)",
                             command=lambda: deletePoint(secondDotsArray, listBoxSecond, canvasWindow, firstDotsArray))
    delButtonSecond.grid(row=14, column=0, columnspan=2)
    changeButtonSecond = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 2)",
                                command=lambda: changePoint(secondDotsArray, entrySecond, listBoxSecond, canvasWindow,
                                                            firstDotsArray))
    changeButtonSecond.grid(row=15, column=0, columnspan=2)

    startButton = Button(rootWindow, text="Исполнить \nпредначертанное!", font=("consolas", 17), bg="yellow", fg="blue",
                         command = )
    startButton.grid(row=0, column=5, rowspan=1)

    canvasWindow = Canvas(rootWindow, bg="white", width=1025, height=1025)
    makeCanvasStart(canvasWindow)

    rootWindow.mainloop()

makeMainWindow()


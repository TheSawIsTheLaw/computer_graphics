from tkinter import *
from re import *

choiceVar = 0

minX = 0
maxY = 0

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
    global maxY, minX

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

def isAngle(x1, x2, x3, y1, y2, y3):
    if (y2 - y1)*(x3 - x1) != (y3 - y1)*(x2 - x1):
        return 1
    return 0

def generateNoAnglesError():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Невозможно построить по заданным параметрам ни одного треугольника!",
                       font=("consolas", 15))
    errorLabel.pack()

###################################################################
def oneArrayAngle(dotsArrayF, dotsArrayS, canvasWindow):
    if len(dotsArrayS) < 3 and len(dotsArrayF) < 3:
        generateNoAnglesError()
        return
    foundF = 0
    foundS = 0

    global k, minX, maxY

    for i in range(len(dotsArrayF) - 2):
        for j in range(i + 1, len(dotsArrayF) - 1):
            for z in range(i + 2, len(dotsArrayF)):
                if isAngle(dotsArrayF[i][0], dotsArrayF[j][0], dotsArrayF[z][0], dotsArrayF[i][1], dotsArrayF[j][1],
                           dotsArrayF[z][1]):
                    foundF += 1 # Найдено х треугольников в первом
                    canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                                             masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k), fill="Red")
                    canvasWindow.create_line(masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k),
                                             masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")
                    canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                                             masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")

    for i in range(len(dotsArrayS) - 2):
        for j in range(i + 1, len(dotsArrayS) - 1):
            for z in range(i + 2, len(dotsArrayS)):
                if isAngle(dotsArrayS[i][0], dotsArrayS[j][0], dotsArrayS[z][0], dotsArrayS[i][1], dotsArrayS[j][1],
                           dotsArrayS[z][1]):
                    foundS += 1 # Найдено х треугольников во втором
                    canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                                             masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k), fill="Blue")
                    canvasWindow.create_line(masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k),
                                             masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")
                    canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                                             masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")

    if not foundF and not foundS:
        generateNoAnglesError()

def twoArraysAngle(dotsArrayF, dotsArrayS, canvasWindow):
    if len(dotsArrayS) + len(dotsArrayF) < 3:
        generateNoAnglesError()
        return
    found = 0

    if not found:
        generateNoAnglesError()

def findTheSmallestAngle(dotsArrayF, dotsArrayS, var, canvasWindow):
    if var == 0:
        oneArrayAngle(dotsArrayF, dotsArrayS, canvasWindow)
    else:
        twoArraysAngle(dotsArrayF, dotsArrayS, canvasWindow)

def makeVarZero():
    global choiceVar
    choiceVar = 0

def makeVarOne():
    global choiceVar
    choiceVar = 1

def makeMainWindow():
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1000)

    makeCascadeMenu(rootWindow)
    firstDotsArray = []
    secondDotsArray = []

    boolVar = BooleanVar()
    global choiceVar
    boolVar.set(0)
    radioButtonF = Radiobutton(text='Треугольник строится на точках одного множества', font=("consolas", 12),
                               variable=boolVar, value=0, command=makeVarZero).grid(row=0,
                                                                                                       column=0,
                                                                                                       columnspan=3)
    radioButtonS = Radiobutton(text='Треугольник строится на точках разных множеств', font=("consolas", 12),
                               variable=boolVar, value=1, command=makeVarOne).grid(row=1,
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
                         command=lambda: findTheSmallestAngle(firstDotsArray, secondDotsArray, choiceVar, canvasWindow))
    startButton.grid(row=0, column=5, rowspan=1)

    canvasWindow = Canvas(rootWindow, bg="white", width=1025, height=1025)
    makeCanvasStart(canvasWindow)

    rootWindow.mainloop()

makeMainWindow()


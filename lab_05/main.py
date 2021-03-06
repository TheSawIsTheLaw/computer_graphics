from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
from time import sleep, time

from numpy import sign

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

extrems = [[]]

curColorLines = "#000000"
curColorBackground = "#ffffff"
noteColor = "#00C12B"
noteColorCheck = (0, 193, 43)

pointsArray = [[]]
edgesArray = [[]]
curFig = 0


def digitBresenham(image, xStart, xEnd, yStart, yEnd):
    if xStart == xEnd and yStart == yEnd:
        image.put(curColorLines, (xStart, yStart))
        return

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    stepX = int(sign(deltaX))
    stepY = int(sign(deltaY))

    deltaX = abs(deltaX)
    deltaY = abs(deltaY)

    if deltaX < deltaY:
        deltaX, deltaY = deltaY, deltaX
        flag = True
    else:
        flag = False

    acc = deltaY + deltaY - deltaX
    curX = xStart
    curY = yStart

    for i in range(deltaX + 1):
        image.put(curColorLines, (curX, curY))

        if flag:
            if acc >= 0:
                curX += stepX
                acc -= (deltaX + deltaX)
            curY += stepY
            acc += deltaY + deltaY
        else:
            if acc >= 0:
                curY += stepY
                acc -= (deltaX + deltaX)
            curX += stepX
            acc += deltaY + deltaY


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Лабораторная работа 5, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритмов растрового заполнения сплошных областей\n"
                 "Реализуется алгоритм заполнения со списком рёбер и флагом.").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(rootWindow, row, column, canvasWindow):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = row, y = column)
    canvasWindow.config(bg = curColorBackground)


def chooseLinesColor(rootWindow, row, column):
    global curColorLines
    curColorLines = colorchooser.askcolor()[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = row, y = column)


def clearImage(canvasWindow):
    canvasWindow.delete("all")
    global pointsArray, edgesArray, extrems, curFig
    curFig = 0
    pointsArray = [[]]
    edgesArray = [[]]
    extrems = [[]]
    global img
    img = PhotoImage(width = 1090, height = 1016)
    canvasWindow.create_image((545, 508), image = img, state = "normal")
    canvasWindow.place(x = 750, y = 0)


def makeCascadeMenu(rootWindow, canvasWindow):
    """
        Функция создания каскадного меню
    """
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu = rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label = 'Формулировка задания', command = makeJobWindow)
    jobMenu.add_command(label = 'Справка', command = makeReference)

    plusCommands = Menu(rootMenu)
    plusCommands.add_command(label = 'Очистить плоскость рисования', command = lambda: clearImage(canvasWindow))

    rootMenu.add_cascade(label = 'Справка', menu = jobMenu)
    rootMenu.add_cascade(label = "Доп. возможности", menu = plusCommands)


def drawArr(image, pointsArray):
    for i in pointsArray:
        image.put(i[2], (i[0], i[1]))


def setColorButtons(rootWindow, canvasWindow):
    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = 250, y = 182)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseLinesColor(rootWindow, 250, 182)).place(x = 40, y = 180)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 182)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseBackgroundColor(rootWindow, 660, 182, canvasWindow)).place(x = 500, y = 180)


def setComboDelay(rootWindow):
    Label(rootWindow, text = "Задержка рисования:", font = fontSettingLower).place(x = 5, y = 140)
    comboDelay = ttk.Combobox(rootWindow, width = 80, textvariable = delay, state = 'readonly', values =
    ('Выключена',
     'Включена'))

    comboDelay.place(x = 250, y = 145)
    comboDelay.current(0)
    return comboDelay


def setImageToCanvas(canvasWindow):
    global img
    img = PhotoImage(width = 1090, height = 1016)
    canvasWindow.create_image((545, 508), image = img, state = "normal")


def click(event):
    global pointsArray
    global img
    global curFig
    pointsArray[curFig].append([event.x, event.y, curColorLines])
    if len(pointsArray[curFig]) >= 2:
        edgesArray[curFig].append([[pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                                    pointsArray[curFig][len(pointsArray[curFig]) - 2][1]],
                                   [pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                                    pointsArray[curFig][len(pointsArray[curFig]) - 1][1]]])
        digitBresenham(img, pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 2][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])

def addPoint(xEntry, yEntry):
    xCoord = int(xEntry.get())
    yCoord = int(yEntry.get())

    global pointsArray
    global img
    global curFig
    pointsArray[curFig].append([xCoord, yCoord, curColorLines])
    if len(pointsArray[curFig]) >= 2:
        edgesArray[curFig].append([[pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                                    pointsArray[curFig][len(pointsArray[curFig]) - 2][1]],
                                   [pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                                    pointsArray[curFig][len(pointsArray[curFig]) - 1][1]]])
        digitBresenham(img, pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 2][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])


def endClick(event):
    global curFig
    global pointsArray
    global edgesArray
    digitBresenham(img, pointsArray[curFig][0][0],
                   pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                   pointsArray[curFig][0][1],
                   pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
    edgesArray[curFig].append([[pointsArray[curFig][0][0],
                        pointsArray[curFig][0][1]],
                      [pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1]]])
    curFig += 1

    edgesArray.append(list())
    pointsArray.append(list())
    print(pointsArray, edgesArray)


def cancelClick(event):
    global pointsArray, curFig
    if len(pointsArray) == 0:
        return
    global curColorLines
    global curColorBackground
    tempCol = curColorLines
    curColorLines = curColorBackground
    if len(pointsArray[curFig]):
        digitBresenham(img, pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 2][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
        pointsArray[curFig].pop()
        edgesArray[curFig].pop()
        print(pointsArray, edgesArray)
    else:
        edgesArray.pop()
        pointsArray.pop()
        curFig -= 1
        digitBresenham(img, pointsArray[curFig][0][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][0][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
        print(pointsArray, edgesArray)
    curColorLines = tempCol


def getSides(pointsArray):
    right = 0
    left = 1090
    bottom = 0
    top = 1060
    for figure in pointsArray:
        for i in figure:
            if i[0] > right:
                right = i[0]
            if i[0] < left:
                left = i[0]
            if i[1] > bottom:
                bottom = i[1]
            if i[1] < top:
                top = i[1]
    return top, right, bottom, left


def leadRoundEdge(img, edge):
    if edge[0][1] == edge[1][1]:
        return

    if edge[0][1] > edge[1][1]:
        edge[1], edge[0] = edge[0], edge[1]
    stepX = (edge[1][0] - edge[0][0])/(edge[1][1] - edge[0][1])

    curX = edge[0][0]
    curY = edge[0][1]
    while curY < edge[1][1]:
        if img.get(int(curX) + 1, curY) != noteColorCheck:
            img.put(noteColor, (int(curX) + 1, curY))
        else:
            img.put(noteColor, (int(curX), curY))
        curX += stepX
        curY += 1


def leadRoundFigure(img, edgesArray):
    for figure in range(len(edgesArray)):
        arrEnd = len(edgesArray[figure]) - 1
        for i in range(arrEnd):
            leadRoundEdge(img, edgesArray[figure][i])
        leadRoundEdge(img, edgesArray[figure][arrEnd])


def rasterScanWithFlag(img, edgesArray, sides):
    leadRoundFigure(img, edgesArray)
    for curY in range(sides[0], sides[2] + 1):
        curColor = curColorBackground
        invColor = curColorLines
        curPointScanString = sides[3]
        for curX in range(sides[3], sides[1] + 3):
            if img.get(curX, curY) == noteColorCheck:
                img.put(curColor, (curPointScanString, curY, curX, curY + 1))
                curColor, invColor = invColor, curColor
                curPointScanString = curX
        img.put(curColor, (curPointScanString, curY, curX, curY + 1))


def rasterScanWithFlagDelay(canvasWindow, img, edgesArray, sides):
    leadRoundFigure(img, edgesArray)
    canvasWindow.update()
    sleep(3)

    for curY in range(sides[0], sides[2] + 1):
        curColor = curColorBackground
        invColor = curColorLines
        curPointScanString = sides[3]
        for curX in range(sides[3], sides[1] + 3):
            if img.get(curX, curY) == noteColorCheck:
                img.put(curColor, (curPointScanString, curY, curX, curY + 1))
                curColor, invColor = invColor, curColor
                curPointScanString = curX
        canvasWindow.update()
        sleep(0.1)
        img.put(curColor, (curPointScanString, curY, curX, curY + 1))


def setExtrems(pointsArray):
    global extrems
    extrems.clear()
    extrems = [[]]

    for figure in range(len(pointsArray)):
        extrems[figure].append(((pointsArray[figure][0][1] < pointsArray[figure][len(pointsArray[figure]) - 1][1] and
                                pointsArray[figure][0][1] < pointsArray[figure][1][1]) or
                               (pointsArray[figure][0][1] > pointsArray[figure][len(pointsArray[figure]) - 1][1] and
                                pointsArray[figure][0][1] > pointsArray[figure][1][1])))
        for i in range(1, len(pointsArray[figure]) - 1):
            extrems[figure].append(((pointsArray[figure][i][1] < pointsArray[figure][i - 1][1] and
                                    pointsArray[figure][i][1] < pointsArray[figure][i + 1][1]) or
                                   (pointsArray[figure][i][1] > pointsArray[figure][i - 1][1] and
                                    pointsArray[figure][i][1] > pointsArray[figure][i + 1][1]))
                                   )

        extrems[figure].append((pointsArray[figure][len(pointsArray[figure]) - 1][1] < pointsArray[figure][len(pointsArray[figure]) - 2][1] and
                        pointsArray[figure][len(pointsArray[figure]) - 1][1] < pointsArray[figure][0][1]) or
                       (pointsArray[figure][len(pointsArray[figure]) - 1][1] > pointsArray[figure][len(pointsArray[figure]) - 2][1] and
                        pointsArray[figure][len(pointsArray[figure]) - 1][1] > pointsArray[figure][0][1]))
        extrems.append(list())
    extrems.pop()


def MakeRasterScan(comboDelay, canvasWindow):
    pointsArray.pop()
    delay = comboDelay.get()
    sides = getSides(pointsArray)
    global edgesArray
    edgesArray.pop()
    setExtrems(pointsArray)
    if delay[1] == 'ы':
        rasterScanWithFlag(img, edgesArray, sides)
    else:
        rasterScanWithFlagDelay(canvasWindow, img, edgesArray, sides)


def timeResearch():
    pointsArray.pop()
    edgesArray.pop()
    sides = getSides(pointsArray)
    setExtrems(pointsArray)
    previous = time()
    rasterScanWithFlag(img, edgesArray, sides)
    after = time()
    researchWindow = Tk()
    researchWindow.title("Временные затраты")
    Label(researchWindow, text = "Временные затраты составили " + str(after - previous) + " секунд", font = fontSettingLower).grid()
    researchWindow.mainloop()


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 5, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.bind('<1>', click)

    canvasWindow.bind('<2>', cancelClick)

    canvasWindow.bind('<3>', endClick)

    canvasWindow.place(x = 750, y = 0)

    comboDelay = setComboDelay(rootWindow)

    setColorButtons(rootWindow, canvasWindow)

    makeAlgButton = Button(rootWindow, text = "Закрасить изображённую фигуру", width = 60,
                           font = fontSettingLower, bg = "#FF9C00", command = lambda: MakeRasterScan(comboDelay, canvasWindow))
    makeAlgButton.place(x = 5, y = 300)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = timeResearch)
    makeTimeResearch.place(x = 5, y = 980)

    Label(text = "Ввод вершин многоугольника производится с помощью мыши\n"
                 "\nЧтобы завершить рисование - \nнажмите правую кнопку мыши и фигура замкнётся.\n"
                 "\nЧтобы отменить последнее действие -\n нажмите среднюю кнопку мыши\n\n"
                 "Для проверки случаев горизонтальных и вертикальных рёбер\nпредусмотрены поля ввода ниже\n", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower).place(x = 10, y = 698)
    xEntry = Entry(rootWindow, font = fontSettingLower, width = 4)
    xEntry.place(x = 239, y = 700)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower).place(x = 420, y = 698)
    yEntry = Entry(rootWindow, font = fontSettingLower, width = 4)
    yEntry.place(x = 649, y = 700)

    Button(rootWindow, text = "Добавить точку", command = lambda: addPoint(xEntry, yEntry), width = 60, font = fontSettingLower, bg = "#FF9C00").place(x = 5, y = 750)

    Label(text = "Алгоритм растрового заполнения \nсплошных областей со списком \nрёбер и флагом", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from time import sleep, time

from numpy import sign

from lab_04.shittyFuncs import niceRound

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

extrems = []

curColorLines = "#000000"
curColorBackground = "#ffffff"
noteColor = "#00C12B"
noteColorCheck = (0, 193, 43)

pointsArray = [[]]
edgesArray = [[]]
curFig = 0

prevCurEnd = []
curEndPoint = 0


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
    global pointsArray
    pointsArray.clear()
    global curEndPoint
    global prevCurEnd
    curEndPoint = 0
    prevCurEnd = []
    edgesArray = []
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


def endClick(event):
    global curEndPoint, curFig
    global pointsArray
    global edgesArray
    digitBresenham(img, pointsArray[curFig][curEndPoint][0], pointsArray[curFig][len(pointsArray[curFig]) - 1][0], pointsArray[curFig][curEndPoint][1], pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
    edgesArray.append([[pointsArray[curFig][curEndPoint[curFig]][0], pointsArray[curFig][curEndPoint][1]],
                      [pointsArray[curFig][len(pointsArray[curFig]) - 1][0], pointsArray[curFig][len(pointsArray[curFig]) - 1][1]]])
    global prevCurEnd
    prevCurEnd.append(curEndPoint)
    curEndPoint = len(pointsArray)


def cancelClick(event):
    global pointsArray
    if len(pointsArray) == 0:
        return
    global curEndPoint
    global curColorLines
    global curColorBackground
    tempCol = curColorLines
    curColorLines = curColorBackground
    if curEndPoint != len(pointsArray):
        digitBresenham(img, pointsArray[len(pointsArray) - 2][0], pointsArray[len(pointsArray) - 1][0], pointsArray[len(pointsArray) - 2][1],
                       pointsArray[len(pointsArray) - 1][1])
        pointsArray.pop()
        edgesArray.pop()
    else:
        global prevCurEnd
        curEndPoint = prevCurEnd.pop()
        digitBresenham(img, pointsArray[curEndPoint][0], pointsArray[len(pointsArray) - 1][0], pointsArray[curEndPoint][1],
                       pointsArray[len(pointsArray) - 1][1])
    curColorLines = tempCol


def getSides(pointsArray):
    right = 0
    left = 1090
    bottom = 0
    top = 1060
    for i in pointsArray:
        if i[0] > right: right = i[0]
        if i[0] < left: left = i[0]
        if i[1] > bottom: bottom = i[1]
        if i[1] < top: top = i[1]
    return top, right, bottom, left


def leadRoundEdge(img, edge, isFE, isSE):
    if edge[0][1] == edge[1][1]:
        return

    if edge[0][1] > edge[1][1]:
        edge[0], edge[1] = edge[1], edge[0]
        isFE, isSE = isSE, isFE

    yStep = 1
    xStep = (edge[1][0] - edge[0][0])/(edge[1][1] - edge[0][1])

    if isFE:
        edge[0][0] += xStep
        edge[0][1] += yStep
    if isSE:
        edge[1][0] -= xStep
        edge[1][1] -= yStep

    curPointX = edge[0][0]
    curPointY = edge[0][1]

    while curPointY < edge[1][1]:
        img.put(noteColor, (int(curPointX) + 1, curPointY))
        curPointX += xStep
        curPointY += yStep


def leadRoundFigure(img, edgesArray):
    for i in range(len(edgesArray) - 1):
        leadRoundEdge(img, edgesArray[i], extrems[i], extrems[i + 1])
    leadRoundEdge(img, edgesArray[len(edgesArray) - 1], extrems[len(edgesArray) - 1], extrems[0])


def rasterScanWithFlag(img, edgesArray, sides):
    leadRoundFigure(img, edgesArray)
    for curY in range(sides[0], sides[2]):
        curColor = curColorBackground
        invColor = curColorLines
        for curX in range(sides[3] - 1, sides[1] + 2):
            if img.get(curX, curY) == noteColorCheck:
                curColor, invColor = invColor, curColor
            img.put(curColor, (curX, curY))


def setExtrems(pointsArray, sides):
    global extrems
    extrems.clear()
    extrems.append((pointsArray[0][1] < pointsArray[len(pointsArray) - 1][1] and pointsArray[0][1] < pointsArray[1][1]) or
                       (pointsArray[0][1] > pointsArray[len(pointsArray) - 1][1] and pointsArray[0][1] > pointsArray[1][1]))

    print(pointsArray)
    for i in range(1, len(pointsArray) - 1):
        extrems.append((pointsArray[i][1] < pointsArray[i - 1][1] and pointsArray[i][1] < pointsArray[i + 1][1]) or
                       (pointsArray[i][1] > pointsArray[i - 1][1] and pointsArray[i][1] > pointsArray[i + 1][1]))

    extrems.append((pointsArray[len(pointsArray) - 1][1] < pointsArray[len(pointsArray) - 2][1] and pointsArray[len(pointsArray) - 1][1] < pointsArray[0][1]) or
                       (pointsArray[len(pointsArray) - 1][1] > pointsArray[len(pointsArray) - 2][1] and pointsArray[len(pointsArray) - 1][1] > pointsArray[0][1]))


def MakeRasterScan(comboDelay):
    delay = comboDelay.get()
    sides = getSides(pointsArray)
    global edgesArray
    setExtrems(pointsArray, sides)
    if delay[1] == 'ы':
        rasterScanWithFlag(img, edgesArray, sides)
    else:
        print("Или с делея?")


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

    makeAlgButton = Button(rootWindow, text = "Закрасить изображённую фигуру", width = 60, font = fontSettingLower, bg = "#FF9C00", command = lambda: MakeRasterScan(comboDelay))
    makeAlgButton.place(x = 5, y = 300)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = print())
    makeTimeResearch.place(x = 5, y = 600)

    Label(text = "Ввод вершин многоугольника производится с помощью мыши\n"
                 "\nЧтобы завершить рисование - \nнажмите правую кнопку мыши и фигура замкнётся.\n"
                 "\nЧтобы отменить последнее действие -\n нажмите среднюю кнопку мыши", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(text = "Алгоритм растрового заполнения \nсплошных областей со списком \nрёбер и флагом", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

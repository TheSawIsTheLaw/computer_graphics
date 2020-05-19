from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

import numpy as np

from numpy import sign

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

curLine = 0

curColorCutter = "#ffffff"
curColorBackground = "#000000"
curColorLines = "#ffff00"
curColorCuted = "#ab00ff"

comboWhatToDraw = 0
tempArr = []

linesArray = []

cutterArray = []


def digitBresenham(image, xStart, yStart, xEnd, yEnd):
    if xStart == xEnd and yStart == yEnd:
        image.put(curColorLines, (xStart, yStart))
        return

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    stepX = int(np.round(sign(deltaX)))
    stepY = int(np.round(sign(deltaY)))

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
    "Лабораторная работа 7, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: что-то очень инетерсное.").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(rootWindow, row, column, canvasWindow):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = row, y = column)
    canvasWindow.config(bg = curColorBackground)


def chooseCutedColor(rootWindow, row, column):
    global curColorCuted
    curColorCuted = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorCuted, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = row, y = column)

def chooseCutterColor(rootWindow, row, column):
    global curColorCutter
    got = colorchooser.askcolor()
    curColorCutter = got[1]
    canvasCutterColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasCutterColor.place(x = row, y = column)


def chooseLineColor(rootWindow, row, column):
    global curColorLines, seedRGB
    got = colorchooser.askcolor()
    seedRGB = (int(got[0][0]), int(got[0][1]), int(got[0][2]))
    curColorLines = got[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = row, y = column)


def clearImage(canvasWindow):
    canvasWindow.delete("all")
    global linesArray, curLine, cutterArray, tempArr
    curLine = 0
    linesArray = []
    cutterArray = []
    tempArr = []
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


def setColorButtons(rootWindow, canvasWindow):
    Button(rootWindow, text = "Цвет отсекателя: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseCutterColor(rootWindow, 250, 182)).place(x = 40, y = 180)
    canvasCutterColor = Canvas(rootWindow, bg = curColorCutter,
                              borderwidth = 5, relief = RIDGE,
                              width = 60, height = 50)
    canvasCutterColor.place(x = 270, y = 182)

    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground,
                                   borderwidth = 5, relief = RIDGE,
                                   width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 182)
    Button(rootWindow, text = "Цвет фона: ",
           font = fontSettingLower,
           height = 2, bg = "#FF9C00", width = 17,
           command = lambda: chooseBackgroundColor(rootWindow, 660,
                                                   182, canvasWindow)).place(x = 435, y = 180)

    canvasLinesColor = Canvas(rootWindow, bg = curColorLines,
                             borderwidth = 5, relief = RIDGE,
                             width = 60, height = 50)
    canvasLinesColor.place(x = 270, y = 262)
    Button(rootWindow, text = "Цвет отрезков: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00", width = 17,
           command = lambda: chooseLineColor(rootWindow, 270, 262)).place(x = 40, y = 260)

    canvasCuted = Canvas(rootWindow, bg = curColorCuted,
                              borderwidth = 5, relief = RIDGE,
                              width = 60, height = 50)
    canvasCuted.place(x = 660, y = 262)
    Button(rootWindow, text = "Цвет отсечения: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00", width = 17,
           command = lambda: chooseCutedColor(rootWindow, 660, 262)).place(x = 435, y = 260)


def setComboWhatToDraw(rootWindow):
    Label(rootWindow, text = "Режим ввода:", font = fontSettingLower).place(x = 5, y = 140)
    global comboWhatToDraw
    comboWhatToDraw = ttk.Combobox(rootWindow,
                              width = 95,
                              textvariable = delay,
                              state = 'readonly',
                              values =
                                ('Отрезки',
                                 'Отсекатель'))

    comboWhatToDraw.place(x = 155, y = 145)
    comboWhatToDraw.current(0)


def setImageToCanvas(canvasWindow):
    global img
    img = PhotoImage(width = 1090, height = 1016)
    canvasWindow.create_image((545, 508), image = img, state = "normal")


def click(event):
    global cutterArray
    global curColorLines
    global curColorCutter
    global curLine
    global linesArray
    global img
    got = comboWhatToDraw.get()
    if got[2] == "р":
        global tempArr
        tempArr.append([event.x, event.y, curColorLines])
        if len(tempArr) == 2:
            linesArray.append(tempArr)
            tempArr = []
            digitBresenham(img, linesArray[curLine][0][0], linesArray[curLine][0][1], linesArray[curLine][1][0], linesArray[curLine][1][1])
            curLine += 1
    else:
        temp = curColorLines
        if len(cutterArray) == 0:
            cutterArray.append([event.x, event.y, curColorCutter])
        else:
            cutterArray.append([event.x, cutterArray[0][1], curColorCutter])
            cutterArray.append([event.x, event.y, curColorCutter])
            cutterArray.append([cutterArray[0][0], event.y, curColorCutter])
            curColorLines = curColorCutter
            digitBresenham(img, cutterArray[0][0], cutterArray[0][1], cutterArray[1][0], cutterArray[1][1])
            digitBresenham(img, cutterArray[1][0], cutterArray[1][1], cutterArray[2][0], cutterArray[2][1])
            digitBresenham(img, cutterArray[2][0], cutterArray[2][1], cutterArray[3][0], cutterArray[3][1])
            digitBresenham(img, cutterArray[0][0], cutterArray[0][1], cutterArray[3][0], cutterArray[3][1])
            curColorLines = temp


def addPoint(xStartEntry, yStartEntry, xEndEntry, yEndEntry):
    xStart = int(xStartEntry.get())
    xEnd = int(xEndEntry.get())
    yStart = int(yStartEntry.get())
    yEnd = int(yEndEntry.get())
    global curLine
    global linesArray
    global img
    linesArray.append([[xStart, yStart, curColorLines], [xEnd, yEnd, curColorLines]])
    digitBresenham(img, linesArray[curLine][0][0], linesArray[curLine][0][1], linesArray[curLine][1][0], linesArray[curLine][1][1])
    curLine += 1


def addCutter(xEntryLeft, yEntryLeft, xEntryRight, yEntryRight):
    global curColorLines
    temp = curColorLines
    xLeft = int(xEntryLeft.get())
    xRight = int(xEntryRight.get())
    yLeft = int(yEntryLeft.get())
    yRight = int(yEntryRight.get())
    cutterArray.append([xLeft, yLeft, curColorCutter])
    cutterArray.append([xRight, yLeft, curColorCutter])
    cutterArray.append([xRight, yRight, curColorCutter])
    cutterArray.append([xLeft, yRight, curColorCutter])
    curColorLines = curColorCutter
    digitBresenham(img, cutterArray[0][0], cutterArray[0][1], cutterArray[1][0], cutterArray[1][1])
    digitBresenham(img, cutterArray[1][0], cutterArray[1][1], cutterArray[2][0], cutterArray[2][1])
    digitBresenham(img, cutterArray[2][0], cutterArray[2][1], cutterArray[3][0], cutterArray[3][1])
    digitBresenham(img, cutterArray[0][0], cutterArray[0][1], cutterArray[3][0], cutterArray[3][1])
    curColorLines = temp



def endClick(event):
    global curLine
    global linesArray
    digitBresenham(img, linesArray[curLine][0][0],
                   linesArray[curLine][len(linesArray[curLine]) - 1][0],
                   linesArray[curLine][0][1],
                   linesArray[curLine][len(linesArray[curLine]) - 1][1])
    curLine += 1

    linesArray.append(list())


def cancelClick(event):
    global linesArray, curLine
    if len(linesArray) == 0:
        return
    global curColorLines
    global curColorBackground
    tempCol = curColorLines
    curColorLines = curColorBackground
    if len(linesArray[curLine]):
        digitBresenham(img, linesArray[curLine][len(linesArray[curLine]) - 2][0],
                       linesArray[curLine][len(linesArray[curLine]) - 1][0],
                       linesArray[curLine][len(linesArray[curLine]) - 2][1],
                       linesArray[curLine][len(linesArray[curLine]) - 1][1])
        linesArray[curLine].pop()
    else:
        linesArray.pop()
        curLine -= 1
        digitBresenham(img, linesArray[curLine][0][0],
                       linesArray[curLine][len(linesArray[curLine]) - 1][0],
                       linesArray[curLine][0][1],
                       linesArray[curLine][len(linesArray[curLine]) - 1][1])
    curColorLines = tempCol


def drawLines(array):
    global img, curColorLines, curColorCuted
    temp = curColorLines
    curColorLines = curColorBackground
    for i in range(cutterArray[0][1] + 1, cutterArray[2][1]):
        digitBresenham(img, cutterArray[0][0] + 1, i, cutterArray[1][0] - 1, i)

    curColorLines = curColorCuted
    for line in array:
        digitBresenham(img, line[1][0], line[1][1], line[0][0], line[0][1])
    curColorLines = temp


def getBinCodes(curLine, leftSide, rightSide, botSide, topSide):
    firstPoint = 0b0000
    secondPoint = 0b0000
    if curLine[0][0] < leftSide:
        firstPoint += 0b1000
    if curLine[0][0] > rightSide:
        firstPoint += 0b0100
    if curLine[0][1] > botSide:
        firstPoint += 0b0010
    if curLine[0][1] < topSide:
        firstPoint += 0b0001

    if curLine[1][0] < leftSide:
        secondPoint += 0b1000
    if curLine[1][0] > rightSide:
        secondPoint += 0b0100
    if curLine[1][1] > botSide:
        secondPoint += 0b0010
    if curLine[1][1] < topSide:
        secondPoint += 0b0001

    return firstPoint, secondPoint


def getCuttedLine(linesArray, line, leftSide, rightSide, botSide, topSide):
    binCodes = getBinCodes(linesArray[line], leftSide, rightSide, botSide, topSide)
    firstPoint = binCodes[0]
    secondPoint = binCodes[1]
    fCoordinates = linesArray[line][0]
    sCoordinates = linesArray[line][1]

    if firstPoint == 0 and secondPoint == 0:
        return linesArray[line]

    if firstPoint & secondPoint:
        return []

    flag = 1
    i = -1
    tan = 1e30
    if not firstPoint:
        result = [fCoordinates]
        workVar = sCoordinates
        i = 1
        flag = 0
    elif not secondPoint:
        result = [sCoordinates]
        workVar = fCoordinates
        i = 1
        flag = 0
    else:
        result = []

    while i <= 1:
        if flag:
            workVar = linesArray[line][i]
        i += 1
        if fCoordinates[0] != sCoordinates[0]:
            tan = (sCoordinates[1] - fCoordinates[1]) / (sCoordinates[0] - fCoordinates[0])
            if workVar[0] <= leftSide:
                crosser = tan * (leftSide - workVar[0]) + workVar[1]
                if (crosser <= botSide) and (crosser >= topSide):
                    result.append([leftSide, int(np.round(crosser))])
                    continue
            elif workVar[0] >= rightSide:
                crosser = tan * (rightSide - workVar[0]) + workVar[1]
                if (crosser <= botSide) and (crosser >= topSide):
                    result.append([rightSide, int(np.round(crosser))])
                    continue
        if fCoordinates[1] != sCoordinates[1]:
            if workVar[1] <= topSide:
                crosser = (topSide - workVar[1]) / tan + workVar[0]
                if (crosser >= leftSide) and (crosser <= rightSide):
                    result.append([int(np.round(crosser)), topSide])
                    continue
            elif workVar[1] >= botSide:
                crosser = (botSide - workVar[1]) / tan + workVar[0]
                if (crosser >= leftSide) and (crosser <= rightSide):
                    result.append([int(np.round(crosser)), botSide])
                    continue

    return result


def simpleAlgCut(linesArray, cutterArray):
    finalArray = []

    if cutterArray[0][0] < cutterArray[2][0]:
        leftSide = cutterArray[0][0]
        rightSide = cutterArray[2][0]
    else:
        rightSide = cutterArray[0][0]
        leftSide = cutterArray[2][0]

    if cutterArray[0][1] < cutterArray[2][1]:
        topSide = cutterArray[0][1]
        botSide = cutterArray[2][1]
    else:
        botSide = cutterArray[0][1]
        topSide = cutterArray[2][1]

    for line in range(len(linesArray)):
        result = getCuttedLine(linesArray, line, leftSide, rightSide, botSide, topSide)
        if result:
            finalArray.append(result)
    drawLines(finalArray)


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Лабораторная работа 7, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+1980+0")

    canvasWindow = Canvas(rootWindow, bg = curColorBackground, width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.bind('<1>', click)

    canvasWindow.bind('<2>', cancelClick)

    canvasWindow.bind('<3>', endClick)

    canvasWindow.place(x = 750, y = 0)

    setComboWhatToDraw(rootWindow)

    setColorButtons(rootWindow, canvasWindow)

    makeAlgButton = Button(rootWindow, text = "Выполнить отсечение", width = 60,
                           font = fontSettingLower, bg = "#FF9C00", command = lambda: simpleAlgCut(linesArray, cutterArray))
    makeAlgButton.place(x = 5, y = 350)


    Label(text = "Ввод вершин отсекателя и отрезков \nпроизводится с помощью мыши\n"
                 "\nТакже предусмотрены поля ввода этих данных ниже\n"
                 , borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(rootWindow, text = "Координаты левого верхнего угла отсекателя", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 5, y = 550)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10,
                                                                                                                                                 y = 600)
    xEntryLeft = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntryLeft.place(x = 259, y = 600)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420,
                                                                                                                                                 y = 600)
    yEntryLeft = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntryLeft.place(x = 669, y = 600)

    Label(rootWindow, text = "Координаты правого нижнего угла отсекателя", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black",
          fg = "white").place(x = 5, y = 650)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 700)
    xEntryRight = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntryRight.place(x = 259, y = 700)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 700)
    yEntryRight = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntryRight.place(x = 669, y = 700)

    Button(rootWindow, text = "Построить отсекатель", command = lambda: addCutter(xEntryLeft, yEntryLeft, xEntryRight, yEntryRight), width = 60, font = fontSettingLower, bg = "#FF9C00").place(x = 5, y = 750)

    Label(rootWindow, text = "Координаты начала и конца отрезка", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black",
          fg = "white").place(x = 5, y = 800)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 850)
    xEntryStart = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntryStart.place(x = 260, y = 850)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 850)
    yEntryStart = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntryStart.place(x = 669, y = 850)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10,
                                                                                                                                                 y = 900)
    xEntryEnd = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntryEnd.place(x = 260, y = 900)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420,
                                                                                                                                                 y = 900)
    yEntryEnd = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntryEnd.place(x = 669, y = 900)

    addLine = Button(rootWindow, text = "Добавить заданный отрезок", width = 60, height = 3, font = fontSettingLower, bg = "#FF9C00", command = lambda: addPoint(xEntryStart, yEntryStart,
                                                                                                                                                     xEntryEnd, yEntryEnd))
    addLine.place(x = 5, y = 946)

    Label(text = "Простой алгоритм \nотсечения отрезков", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

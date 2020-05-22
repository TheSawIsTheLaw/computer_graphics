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
           command = lambda: chooseCutterColor(rootWindow, 270, 182)).place(x = 40, y = 180)
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
        cutterArray.append([event.x, event.y, curColorLines])
        if len(cutterArray) >= 2:
            temp = curColorLines
            curColorLines = curColorCutter
            digitBresenham(img, cutterArray[len(cutterArray) - 2][0], cutterArray[len(cutterArray) - 2][1],
                                cutterArray[len(cutterArray) - 1][0], cutterArray[len(cutterArray) - 1][1])
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


def endClick(event):
    global cutterArray
    global curColorLines
    temp = curColorLines
    curColorLines = curColorCutter
    digitBresenham(img, cutterArray[0][0], cutterArray[0][1],
                        cutterArray[len(cutterArray) - 1][0], cutterArray[len(cutterArray) - 1][1])
    curColorLines = temp


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


def scalProd(fVector, sVector):
    return fVector[0] * sVector[0] + fVector[1] * sVector[1]

def normal(fPoint, sPoint, posToPoint):
    foundVector = [fPoint[0] - sPoint[0], fPoint[1] - sPoint[1]]
    positiveForVector = [sPoint[0] - posToPoint[0], fPoint[1] - posToPoint[1]]

    if foundVector[1]:
        foundPoint = - (foundVector[0] / foundVector[1])
        normVec = [1, foundPoint]
    else:
        normVec = [0, 1]

    if scalProd(positiveForVector, normVec) < 0:
        normVec[0] = -normVec[0]
        normVec[1] = -normVec[1]
    return normVec


def CyrusBeckAlg(linesArray, cutterArray):
    '''
    if not isCutterConvex(cutterArray):
        errorMessage()
        return
    '''
    numOfSides = len(cutterArray)
    for line in linesArray:
        # Следующее вынести бы в отдельную функцию
        directrix = [line[1][0] - line[0][0], line[1][1] - line[0][1]]
        bottomLimit = 0
        topLimit = 1
        for i in range(numOfSides - 1):
            print(normal())
        # не забудь добавить последнюю с нормалью, положительной к первому и последнему ребру отсекателя



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


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Лабораторная работа 8, Якуба Дмитрий, ИУ7-43Б")
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
                           font = fontSettingLower, bg = "#FF9C00", command = lambda: CyrusBeckAlg(linesArray, cutterArray))
    makeAlgButton.place(x = 5, y = 350)


    Label(text = "Ввод вершин отсекателя и отрезков \nпроизводится с помощью мыши\n"
                 "\nТакже предусмотрены поля ввода этих данных ниже\n(замыкание отсекателя - пробел)"
                 , borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(rootWindow, text = "Добавление точки стороны отсекателя", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 5, y = 550)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10,
                                                                                                                                                 y = 600)
    xEntryNewPoint = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntryNewPoint.place(x = 259, y = 600)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420,
                                                                                                                                                 y = 600)
    yEntryNewPoint = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntryNewPoint.place(x = 669, y = 600)

    Button(rootWindow, text = "Добавить точку отсекателя", command = lambda: print(), height = 6, width = 60, font = fontSettingLower, bg = "#FF9C00").place(x = 5, y = 645)

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

    Label(text = "Алгоритм \nКируса-Бека", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

from time import sleep, time

from numpy import sign

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

curFig = 0

curColorCutter = "#ffffff"
curColorBackground = "#000000"
curColorLines = "#a04020"
curColorCuted = "#f0a0ff"

pointsArray = [[]]

dotsArray = []


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
    "Лабораторная работа 6, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритма построчного затравочного заполнения спрошных областей").grid()

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
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = row, y = column)


def chooseLineColor(rootWindow, row, column):
    global lineColor, seedRGB
    got = colorchooser.askcolor()
    seedRGB = (int(got[0][0]), int(got[0][1]), int(got[0][2]))
    seedColor = got[1]
    canvasLinesColor = Canvas(rootWindow, bg = seedColor, borderwidth = 5, relief = RIDGE, width = 440, height = 50)
    canvasLinesColor.place(x = row, y = column)


def clearImage(canvasWindow):
    canvasWindow.delete("all")
    global pointsArray, curFig
    curFig = 0
    pointsArray = [[]]
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
           command = lambda: chooseLineColor(rootWindow, 280, 262)).place(x = 40, y = 260)

    canvasCuted = Canvas(rootWindow, bg = curColorCuted,
                              borderwidth = 5, relief = RIDGE,
                              width = 60, height = 50)
    canvasCuted.place(x = 660, y = 262)
    Button(rootWindow, text = "Цвет отсечения: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00", width = 17,
           command = lambda: chooseCutedColor(rootWindow, 660, 262)).place(x = 435, y = 260)


def setComboWhatToDraw(rootWindow):
    Label(rootWindow, text = "Режим ввода:", font = fontSettingLower).place(x = 5, y = 140)
    comboDelay = ttk.Combobox(rootWindow,
                              width = 95,
                              textvariable = delay,
                              state = 'readonly',
                              values =
                                ('Отрезки',
                                 'Отсекать'))

    comboDelay.place(x = 155, y = 145)
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
        digitBresenham(img, pointsArray[curFig][len(pointsArray[curFig]) - 2][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 2][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])


def endClick(event):
    global curFig
    global pointsArray
    digitBresenham(img, pointsArray[curFig][0][0],
                   pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                   pointsArray[curFig][0][1],
                   pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
    curFig += 1

    pointsArray.append(list())


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
    else:
        pointsArray.pop()
        curFig -= 1
        digitBresenham(img, pointsArray[curFig][0][0],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][0],
                       pointsArray[curFig][0][1],
                       pointsArray[curFig][len(pointsArray[curFig]) - 1][1])
    curColorLines = tempCol

def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 6, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = curColorBackground, width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.bind('<B1-Motion>', click)

    canvasWindow.bind('<1>', click)

    canvasWindow.bind('<2>', cancelClick)

    canvasWindow.bind('<3>', endClick)

    canvasWindow.place(x = 750, y = 0)

    comboWhatToDraw = setComboWhatToDraw(rootWindow)

    setColorButtons(rootWindow, canvasWindow)

    makeAlgButton = Button(rootWindow, text = "Выполнить отсечение", width = 60,
                           font = fontSettingLower, bg = "#FF9C00", command = lambda: print())
    makeAlgButton.place(x = 5, y = 350)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = lambda: timeResearch(xEntrySeed, yEntrySeed))
    makeTimeResearch.place(x = 5, y = 980)

    Label(text = "Ввод вершин отсекателя и отрезков \nпроизводится с помощью мыши\n"
                 "\nТакже предусмотрены поля ввода этих данных ниже\n"
                 , borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(rootWindow, text = "Координаты левого верхнего угла отсекателя", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 5, y = 550)

    Label(rootWindow, text = "Координаты правого нижнего угла отсекателя", width = 60, font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black",
          fg = "white").place(x = 5, y = 650)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 700)
    xEntry = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntry.place(x = 259, y = 700)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 700)
    yEntry = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntry.place(x = 669, y = 700)

    Button(rootWindow, text = "Построить отсекатель", command = lambda: print(), width = 60, font = fontSettingLower, bg = "#FF9C00").place(x = 5, y = 750)

    Label(rootWindow, text = "Координаты затравочной точки (если оставить поля пустыми,\nто ею будет являться последняя поставленная мышью точка)", font = fontSettingLower).place(x = 10, y = 820)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 900)
    xEntrySeed = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntrySeed.place(x = 260, y = 900)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 900)
    yEntrySeed = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntrySeed.place(x = 669, y = 900)

    Label(text = "Простой алгоритм \nотсечения отрезков", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

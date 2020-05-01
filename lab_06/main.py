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

curColorLines = "#ffffff"
curColorBackground = "#000000"
seedColor = "#a04020"

linesRGB = (255, 255, 255)
seedRGB = (160, 64, 32)

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


def chooseLinesColor(rootWindow, row, column):
    global curColorLines
    global linesRGB
    got = colorchooser.askcolor()
    linesRGB = (int(got[0][0]), int(got[0][1]), int(got[0][2]))
    curColorLines = got[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = row, y = column)


def chooseSeedColor(rootWindow, row, column):
    global seedColor
    seedColor = colorchooser.askcolor()[1]
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
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines,
                              borderwidth = 5, relief = RIDGE,
                              width = 60, height = 50)
    canvasLinesColor.place(x = 250, y = 182)
    Button(rootWindow, text = "Цвет границ: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseLinesColor(rootWindow, 250, 182)).place(x = 40, y = 180)

    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground,
                                   borderwidth = 5, relief = RIDGE,
                                   width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 182)
    Button(rootWindow, text = "Цвет фона: ",
           font = fontSettingLower,
           height = 2, bg = "#FF9C00",
           command = lambda: chooseBackgroundColor(rootWindow, 660,
                                                   182, canvasWindow)).place(x = 500, y = 180)

    canvasSeedColor = Canvas(rootWindow, bg = seedColor,
                             borderwidth = 5, relief = RIDGE,
                             width = 440, height = 50)
    canvasSeedColor.place(x = 280, y = 262)
    Button(rootWindow, text = "Цвет заполнения: ",
           font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseSeedColor(rootWindow, 280, 262)).place(x = 40, y = 260)


def setComboDelay(rootWindow):
    Label(rootWindow, text = "Задержка рисования:", font = fontSettingLower).place(x = 5, y = 140)
    comboDelay = ttk.Combobox(rootWindow,
                              width = 80,
                              textvariable = delay,
                              state = 'readonly',
                              values =
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


def seedFill(img, xSeed, ySeed):
    stack = list()
    stack.append([xSeed, ySeed])

    while len(stack):
        gotDot = stack.pop()

        curX = gotDot[0]
        curY = gotDot[1]

        gotColor = img.get(curX, curY)
        while gotColor != linesRGB and gotColor != seedRGB:
            #img.put(seedColor, (curX, curY))    НА ПРОДЕ УБЕРИ КОММЕНТАРИИ, ВЕРНИ ИСХОД
            curX -= 1
            gotColor = img.get(curX, curY)
        xLeft = curX + 1
        img.put(seedColor, (xLeft, curY, gotDot[0] + 1, curY + 1))

        curX = gotDot[0] + 1
        gotColor = img.get(curX, curY)
        while gotColor != linesRGB and gotColor != seedRGB:
            #img.put(seedColor, (curX, curY))
            curX += 1
            gotColor = img.get(curX, curY)
        xRight = curX - 1
        img.put(seedColor, (gotDot[0], curY, xRight + 1, curY + 1))

        curX = xLeft
        curY += 1

        while curX <= xRight:
            flag = False
            gotColor = img.get(curX, curY)
            while gotColor != linesRGB and gotColor != seedRGB and curX <= xRight:
                flag = True
                curX += 1
                gotColor = img.get(curX, curY)

            if flag:
                if curX == xRight and gotColor == linesRGB and gotColor == seedRGB:
                    stack.append([curX, curY])
                else:
                    stack.append([curX - 1, curY])
                flag = False

            xStart = curX
            while (gotColor == linesRGB or gotColor == seedRGB) and curX < xRight:
                curX += 1
                gotColor = img.get(curX, curY)

            if curX == xStart:
                curX += 1

        curX = xLeft
        curY -= 2

        while curX <= xRight:
            flag = False
            gotColor = img.get(curX, curY)
            while gotColor != linesRGB and gotColor != seedRGB and curX <= xRight:
                flag = True
                curX += 1
                gotColor = img.get(curX, curY)

            if flag:
                if curX == xRight and gotColor == linesRGB and gotColor == seedRGB:
                    stack.append([curX, curY])
                else:
                    stack.append([curX - 1, curY])
                flag = False

            xStart = curX
            while (gotColor == linesRGB or gotColor == seedRGB) and curX < xRight:
                curX += 1
                gotColor = img.get(curX, curY)

            if curX == xStart:
                curX += 1


def seedFillDelayed(img, canvasWindow, xSeed, ySeed):
    stack = list()
    stack.append([xSeed, ySeed])

    while len(stack):
        gotDot = stack.pop()

        curX = gotDot[0]
        curY = gotDot[1]

        gotColor = img.get(curX, curY)
        while gotColor != linesRGB and gotColor != seedRGB:
            img.put(seedColor, (curX, curY))
            curX -= 1
            gotColor = img.get(curX, curY)
        xLeft = curX + 1

        curX = gotDot[0] + 1
        gotColor = img.get(curX, curY)
        while gotColor != linesRGB and gotColor != seedRGB:
            img.put(seedColor, (curX, curY))
            curX += 1
            gotColor = img.get(curX, curY)
        xRight = curX - 1
        canvasWindow.update()
        sleep(0.03)

        curX = xLeft
        curY += 1

        while curX <= xRight:
            flag = False
            gotColor = img.get(curX, curY)
            while gotColor != linesRGB and gotColor != seedRGB and curX <= xRight:
                flag = True
                curX += 1
                gotColor = img.get(curX, curY)

            if flag:
                if curX == xRight and gotColor == linesRGB and gotColor == seedRGB:
                    stack.append([curX, curY])
                else:
                    stack.append([curX - 1, curY])
                flag = False

            xStart = curX
            while (gotColor == linesRGB or gotColor == seedRGB) and curX < xRight:
                curX += 1
                gotColor = img.get(curX, curY)

            if curX == xStart:
                curX += 1

        curX = xLeft
        curY -= 2

        while curX <= xRight:
            flag = False
            gotColor = img.get(curX, curY)
            while gotColor != linesRGB and gotColor != seedRGB and curX <= xRight:
                flag = True
                curX += 1
                gotColor = img.get(curX, curY)

            if flag:
                if curX == xRight and gotColor == linesRGB and gotColor == seedRGB:
                    stack.append([curX, curY])
                else:
                    stack.append([curX - 1, curY])
                flag = False

            xStart = curX
            while (gotColor == linesRGB or gotColor == seedRGB) and curX < xRight:
                curX += 1
                gotColor = img.get(curX, curY)

            if curX == xStart:
                curX += 1


def makeSeedFill(canvasWindow, comboDelay, xStartEntry, yStartEntry):
    xStart = xStartEntry.get()
    yStart = yStartEntry.get()
    if xStart == "" or yStart == "":
        xStart = pointsArray[-1][0][0]
        yStart = pointsArray[-1][0][1]
    else:
        xStart = int(xStart)
        yStart = int(yStart)

    delayGot = comboDelay.get()
    global img

    if delayGot[1] == "ы":
        seedFill(img, xStart, yStart)
    else:
        seedFillDelayed(img, canvasWindow, xStart, yStart)


def makeTimeResearchWindow(time):
    resWindow = Tk()
    resWindow.title("Временные замеры")

    Label(resWindow, font = fontSettingLower, text = "Операция заполнения заняла " + str(time) + " секунд").grid()

    resWindow.mainloop()


def timeResearch(xStartEntry, yStartEntry):
    xStart = xStartEntry.get()
    yStart = yStartEntry.get()
    if xStart == "" or yStart == "":
        xStart = pointsArray[-1][0][0]
        yStart = pointsArray[-1][0][1]
    else:
        xStart = int(xStart)
        yStart = int(yStart)

    before = time()
    seedFill(img, xStart, yStart)
    after = time()
    makeTimeResearchWindow(after - before)


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

    comboDelay = setComboDelay(rootWindow)

    setColorButtons(rootWindow, canvasWindow)

    makeAlgButton = Button(rootWindow, text = "Закрасить изображённую фигуру", width = 60,
                           font = fontSettingLower, bg = "#FF9C00", command = lambda: makeSeedFill(canvasWindow, comboDelay, xEntrySeed, yEntrySeed))
    makeAlgButton.place(x = 5, y = 350)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = lambda: timeResearch(xEntrySeed, yEntrySeed))
    makeTimeResearch.place(x = 5, y = 980)

    Label(text = "Ввод вершин многоугольника производится с помощью мыши\n"
                 "\nЧтобы завершить рисование - \nнажмите правую кнопку мыши и фигура замкнётся.\n"
                 "\nЧтобы отменить последнее действие -\n нажмите среднюю кнопку мыши\n\n"
                 "Для проверки случаев горизонтальных и вертикальных рёбер\nпредусмотрены поля ввода ниже\n", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 700)
    xEntry = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntry.place(x = 259, y = 700)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 700)
    yEntry = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntry.place(x = 669, y = 700)

    Button(rootWindow, text = "Добавить точку", command = lambda: addPoint(xEntry, yEntry), width = 60, font = fontSettingLower, bg = "#FF9C00").place(x = 5, y = 750)

    Label(rootWindow, text = "Координаты затравочной точки (если оставить поля пустыми,\nто ею будет являться последняя поставленная мышью точка)", font = fontSettingLower).place(x = 10, y = 820)

    Label(rootWindow, text = "Координата X точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 10, y = 900)
    xEntrySeed = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    xEntrySeed.place(x = 260, y = 900)

    Label(rootWindow, text = "Координата Y точки:", font = fontSettingLower, borderwidth = 10, relief = RIDGE, bg = "black", fg = "white").place(x = 420, y = 900)
    yEntrySeed = Entry(rootWindow, font = fontSettingLower, width = 4, borderwidth = 10, relief = RIDGE)
    yEntrySeed.place(x = 669, y = 900)

    Label(text = "Алгоритм построчного \nзатравочного заполнения", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

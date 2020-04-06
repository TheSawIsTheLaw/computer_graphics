from tkinter import *
from tkinter import colorchooser
from math import *
from numpy import sign
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib import colors
from colormap import rgb2hex
from datetime import datetime

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

method = 0

curColorLines = "#000000"
curColorBackground = "#ffffff"

img = 0


def RGBtoHEX(rgb):
    return '#%02x%02x%02x' % rgb


def niceRound(number):
    ret = int(number)
    if number < 0:
        if fabs(number) - abs(ret) >= 0.5:
            return ret - 1
        else:
            return ret
    else:
        if number - ret >= 0.5:
            return ret + 1
        else:
            return ret


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Лабораторная работа 3, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритмов построения отрезков.\n\n"
                 "Реализовать и исследовать следующие алгоритмы построения отрезков:\n"
                 "Алгоритм цифрового дифференциального анализатора\n"
                 "Алгоритм Брезенхема с целыми коэффициентами\n"
                 "Алгоритм Брезенхема с действительными коэффициентами\n"
                 "Алгоритм Брезенхема построения отрезка с устранением ступенчаточти\n"
                 "Алгоритм Ву\n"
                 "Алгоритм Tkinter Canvas\n"
                 "Предоставить сравнение визуальных характеристик построенных отрезков \nи исследование временных характеристик").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(canvasBackgroundColor, rootWindow, row, column, canvasWindow):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasBackgroundColor.grid(row = row, column = column, sticky = W)
    canvasWindow.config(bg = curColorBackground)


def chooseLinesColor(canvasWindow, rootWindow, row, column):
    global curColorLines
    curColorLines = colorchooser.askcolor()[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasLinesColor.grid(row = row, column = column, sticky = W)


def clearImage(canvasWindow):
    canvasWindow.delete("all")
    global img
    img = PhotoImage(width = 880, height = 1017)
    canvasWindow.create_image((440, 508), image = img, state = "normal")
    canvasWindow.grid(row = 0, column = 7, rowspan = 13)


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


def makeErrorFirstEntryX():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Значение начала отрезка по Х\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorSecondEntryX():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Значение конца отрезка по Х\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorFirstEntryY():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Значение начала отрезка по Y\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorSecondEntryY():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Значение конца отрезка по Y\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeIntentity(curCol, backColor, acc):
    R = niceRound(curCol[0] + (backColor[0] - curCol[0]) * acc)
    if R > 255:
        R = 255
    elif R < 0:
        R = 0
    G = niceRound(curCol[1] + (backColor[1] - curCol[1]) * acc)
    if G > 255:
        G = 255
    elif G < 0:
        G = 0
    B = niceRound(curCol[2] + (backColor[2] - curCol[2]) * acc)
    if B > 255:
        B = 255
    elif B < 0:
        B = 0
    return rgb2hex(R, G, B)


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

    if flag:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if acc >= 0:
                curX += stepX
                acc -= (deltaX + deltaX)
            curY += stepY
            acc += deltaY + deltaY
    else:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if acc >= 0:
                curY += stepY
                acc -= (deltaX + deltaX)
            curX += stepX
            acc += deltaY + deltaY


def WuAlg(image, xStart, xEnd, yStart, yEnd):
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

    tngModule = deltaY / deltaX

    acc = -1
    curX = xStart
    curY = yStart

    curCol = list(colors.to_rgb(curColorLines))
    backColor = list(colors.to_rgb(curColorBackground))
    for k in range(3):
        curCol[k] *= 255
        backColor[k] *= 255

    if flag:
        for i in range(deltaX):
            color = makeIntentity(curCol, backColor, 1 + acc)
            image.put(color, (curX, curY))

            color = makeIntentity(curCol, backColor, - acc)
            image.put(color, (curX, curY + stepY))
            if acc >= 0:
                curX += stepX
                acc -= 1
            curY += stepY
            acc += tngModule
    else:
        for i in range(deltaX):
            color = makeIntentity(curCol, backColor, 1 + acc)
            image.put(color, (curX, curY))
            color = makeIntentity(curCol, backColor, - acc)
            image.put(color, (curX, curY + stepY))

            if acc >= 0:
                curY += stepY
                acc -= 1
            curX += stepX
            acc += tngModule


def tkinterAlg(canvasWindow, xStart, xEnd, yStart, yEnd):
    canvasWindow.create_line(xStart, yStart, xEnd, yEnd, width = 1, fill = curColorLines)


def stepRemovalBresenham(image, xStart, xEnd, yStart, yEnd):
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

    tngModule = deltaY / deltaX

    acc = 1 / 2
    correction = 1 - tngModule
    curX = xStart
    curY = yStart

    curCol = list(colors.to_rgb(curColorLines))
    backColor = list(colors.to_rgb(curColorBackground))
    for k in range(3):
        curCol[k] *= 255
        backColor[k] *= 255

    if flag:
        for i in range(deltaX):
            color = makeIntentity(curCol, backColor, acc)
            image.put(color, (curX, curY))

            if acc >= correction:
                curX += stepX
                acc -= correction + tngModule
            curY += stepY
            acc += tngModule
    else:
        for i in range(deltaX):
            color = makeIntentity(curCol, backColor, - acc)
            image.put(color, (curX, curY))

            if acc >= correction:
                curY += stepY
                acc -= correction + tngModule
            curX += stepX
            acc += tngModule


def realBresenham(image, xStart, xEnd, yStart, yEnd):
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

    tngModule = deltaY / deltaX

    acc = tngModule - 0.5
    curX = xStart
    curY = yStart

    if flag:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if acc >= 0:
                curX += stepX
                acc -= 1
            curY += stepY
            acc += tngModule
    else:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if acc >= 0:
                curY += stepY
                acc -= 1
            curX += stepX
            acc += tngModule


def DDAline(image, xStart, xEnd, yStart, yEnd):
    if xStart == xEnd and yStart == yEnd:
        image.put(curColorLines, (xStart, yStart))
        return

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    trX = abs(deltaX)
    trY = abs(deltaY)

    if trX > trY:
        length = trX
    else:
        length = trY

    deltaX = deltaX / length
    deltaY = deltaY / length

    curX = xStart
    curY = yStart

    for i in range(length):
        image.put(curColorLines, (niceRound(curX), niceRound(curY)))
        curX += deltaX
        curY += deltaY

def makeErrorDegree():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Величина угла шага\n должно являться числом \n"
                            "с плавающей точкой").grid()

    errWindow.mainloop()

def makeErrorLength():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Длина отрезка задаётся положительным целочисленным значением").grid()

    errWindow.mainloop()

def makeErrorCenterX():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Координата центра по оси x\n должна являться целочисленной величиной").grid()

    errWindow.mainloop()


def makeErrorCenterY():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, font = fontSettingLower, text = "Координата центра по оси y\n должна являться целочисленной величиной").grid()

    errWindow.mainloop()


def bunchResearch(image, degreeEntry, lengthEntry, centerEntryX, centerEntryY, combo, canvasWindow):
    try:
        degreesStep = float(degreeEntry.get())
    except Exception:
        makeErrorDegree()
        return

    try:
        length = int(lengthEntry.get())
        if length <= 0:
            makeErrorLength()
            return
    except Exception:
        makeErrorLength()
        return

    try:
        centerX = int(centerEntryX.get())
    except Exception:
        makeErrorCenterX()
        return

    try:
        centerY = int(centerEntryY.get())
    except Exception:
        makeErrorCenterY()
        return
    degrees = 0
    curX = centerX
    curY = centerY - length
    constantX = centerX - length
    constantY = centerY - length
    while abs(degrees) < 360:
        printRasterLine(image, centerX, curX, centerY, curY, combo, canvasWindow)
        degrees += degreesStep
        curX = niceRound(constantX * sin(radians(degrees)))
        curY = niceRound(constantY * cos(radians(degrees)))


def printRasterWRAP(image, entryXS, entryXE, entryYS, entryYE, combo, canvasWindow):
    try:
        xStart = entryXS.get()
        xStart = int(xStart)
    except Exception:
        makeErrorFirstEntryX()
        return

    try:
        xEnd = int(entryXE.get())
    except Exception:
        makeErrorSecondEntryX()
        return

    try:
        yStart = int(entryYS.get())
    except Exception:
        makeErrorFirstEntryY()
        return

    try:
        yEnd = int(entryYE.get())
    except Exception:
        makeErrorSecondEntryY()
        return

    printRasterLine(image, xStart, xEnd, yStart, yEnd, combo, canvasWindow)


def timeResearch(image, canvasWindow):
    masTime = []
    curTime = 0
    for i in range(100):
        clearImage(canvasWindow)
        degrees = 0
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            DDAline(image, 500, curX, 500, curY)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)
    curTime = 0

    for i in range(100):
        clearImage(canvasWindow)
        degrees = 0
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            realBresenham(image, 500, curX, 500, curY)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)
    curTime = 0

    for i in range(100):
        clearImage(canvasWindow)
        degrees = 0
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            digitBresenham(image, 500, curX, 500, curY)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)
    curTime = 0

    for i in range(100):
        clearImage(canvasWindow)
        degrees = 0
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            stepRemovalBresenham(image, 500, curX, 500, curY)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)
    curTime = 0

    for i in range(100):
        clearImage(canvasWindow)
        degrees = 0
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            WuAlg(image, 500, curX, 500, curY)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)
    curTime = 0

    i = 0
    for i in range(100):
        degrees = 0
        clearImage(canvasWindow)
        curX = 500
        curY = 200
        while abs(degrees) < 360:
            start = datetime.now()
            tkinterAlg(canvasWindow, curX, 500, curY, 500)
            end = datetime.now()
            curTime = curTime + (end.timestamp() - start.timestamp())
            degrees += 20
            curX = niceRound(500 - 300 * sin(radians(degrees)))
            curY = niceRound(500 - 300 * cos(radians(degrees)))
    curTime /= 100
    masTime.append(curTime)

    plt.figure(figsize = (15, 10))
    masNames = ["ЦДА", "Брезенхем \n(действительные коэф.)",
                "Брезенхем \n(целые коэф.)", "Брезенхем \n(с устранением ступенчатости)",
                "Ву", "canvas\ncreate_line"]

    plt.bar(masNames, masTime, align = "center")
    plt.title("Временные характеристики алгоритмов")
    plt.show()


def printRasterLine(image, xStart, xEnd, yStart, yEnd, combo, canvasWindow):
    curAlg = combo.get()

    if curAlg[0] == "1":
        DDAline(image, xStart, xEnd, yStart, yEnd)
    elif curAlg[0] == "2":
        realBresenham(image, xStart, xEnd, yStart, yEnd)
    elif curAlg[0] == "3":
        digitBresenham(image, xStart, xEnd, yStart, yEnd)
    elif curAlg[0] == "4":
        stepRemovalBresenham(image, xStart, xEnd, yStart, yEnd)
    elif curAlg[0] == "5":
        WuAlg(image, xStart, xEnd, yStart, yEnd)
    else:
        tkinterAlg(canvasWindow, xStart, xEnd, yStart, yEnd)


def makeMainWindow():
    """
            Функция Создания главного окна
        """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 3, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 880, height = 1016, borderwidth = 5, relief = RIDGE)
    global img
    img = PhotoImage(width = 880, height = 1017)
    canvasWindow.create_image((440, 508), image = img, state = "normal")
    canvasWindow.grid(row = 0, column = 7, rowspan = 13)

    # Выбор метода построения
    Label(rootWindow, text = "Алгоритм построения:", font = fontSettingLower).grid(row = 0, column = 0, columnspan = 1, sticky = E)
    listBox = ttk.Combobox(rootWindow, width = 70, textvariable = method, state = 'readonly', values =
    ('1. Алгоритм цифрового дифференциального анализатора',
     '2. Алгоритм Брезенхема с действительными коэффициентами',
     '3. Алгоритм Брезенхема с целыми коэффициентами',
     '4. Алгоритм Брезенхема построения отрезка с устранением ступенчаточти',
     '5. Алгоритм Ву',
     '6. Алгоритм Tkinter canvas.create_line'))
    listBox.grid(row = 0, column = 1, columnspan = 4, sticky = W)
    listBox.current(0)

    Label(rootWindow, text = "Начальная точка отрезка", font = fontSettingLabels).grid(row = 1, columnspan = 6, sticky = W)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 2, column = 0, sticky = E)
    entryXFirst = Entry(rootWindow, font = fontSettingLower, width = 5)
    entryXFirst.grid(row = 2, column = 1, sticky = W)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 2, column = 2, sticky = E)
    entryYFirst = Entry(rootWindow, font = fontSettingLower, width = 5)
    entryYFirst.grid(row = 2, column = 3, sticky = W)

    Label(rootWindow, text = "Конечная точка отрезка", font = fontSettingLabels).grid(row = 3, columnspan = 6, sticky = W)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 4, column = 0, sticky = E)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 4, column = 2, sticky = E)
    entryXSecond = Entry(rootWindow, font = fontSettingLower, width = 5)
    entryXSecond.grid(row = 4, column = 1, sticky = W)
    entryYSecond = Entry(rootWindow, font = fontSettingLower, width = 5)
    entryYSecond.grid(row = 4, column = 3, sticky = W)

    Button(rootWindow, text = "Построить отрезок", font = fontSettingLower,
           command = lambda: printRasterWRAP(img, entryXFirst, entryXSecond, entryYFirst, entryYSecond, listBox, canvasWindow)).grid(row = 5, columnspan = 5)

    Label(rootWindow, text = "────────────────────────────────────────────────────────────────────────────────", font = fontSettingLower, width = 79).grid(
        row = 6, columnspan = 6, sticky = NW)
    Label(rootWindow, text = "Угловой шаг при построении отрезков (в градусах): ", font = fontSettingLower).grid(row = 7, columnspan = 2)
    angleEntry = Entry(rootWindow, font = fontSettingLower, width = 13)
    angleEntry.grid(row = 7, column = 2)

    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasLinesColor.grid(row = 8, column = 1, sticky = W)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, command = lambda: chooseLinesColor(canvasLinesColor, rootWindow, 8, 1)).grid(row = 8,
                                                                                                                                                       column = 0,
                                                                                                                                                       sticky = E)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasBackgroundColor.grid(row = 8, column = 3, sticky = W)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower,
           command = lambda: chooseBackgroundColor(canvasBackgroundColor, rootWindow, 8, 3, canvasWindow)).grid(row = 8, column = 2, sticky = E)

    Label(rootWindow, text = "Длина каждого из отрезков:", font = fontSettingLower).grid(row = 9)
    lenghEntry = Entry(rootWindow, font = fontSettingLower)
    lenghEntry.grid(row = 9, column = 1)

    Label(rootWindow, text = "Координата точки начала\n исходящих 'лучей'", font = fontSettingLower).grid(row = 10)
    Label(rootWindow, text = "x:", font = fontSettingLower).grid(row = 10, column = 1, sticky = E)
    centerEntryX = Entry(rootWindow, font = fontSettingLower, width = 5)
    centerEntryX.grid(row = 10, column = 2)
    Label(rootWindow, text = "y:", font = fontSettingLower).grid(row = 10, column = 3, sticky = E)
    centerEntryY = Entry(rootWindow, font = fontSettingLower, width = 5)
    centerEntryY.grid(row = 10, column = 4)

    Button(rootWindow, text = "Исследование визуальных характеристик отрезков,\n построенных разными алгоритмами", font = fontSettingLower, command = lambda: bunchResearch(img, angleEntry, lenghEntry, centerEntryX, centerEntryY, listBox, canvasWindow),
           width = 50).grid(row = 11, columnspan = 5)
    Button(rootWindow, text = "Исследование временных характеристик", font = fontSettingLower, command = lambda: timeResearch(img, canvasWindow), width = 50).grid(row = 12, columnspan = 5)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

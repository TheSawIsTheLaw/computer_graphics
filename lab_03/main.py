from tkinter import *
from tkinter import colorchooser
from math import *
from numpy import sign
from tkinter import ttk
from matplotlib import colors
from colormap import rgb2hex

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

    Label(errWindow, text = "Значение начала отрезка по Х\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorSecondEntryX():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, text = "Значение конца отрезка по Х\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorFirstEntryY():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, text = "Значение начала отрезка по Y\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


def makeErrorSecondEntryY():
    errWindow = Tk()
    errWindow.title("Ошибка!")

    Label(errWindow, text = "Значение конца отрезка по Y\n координате должно являтся\n"
                            "единственным целочисленным значением").grid()

    errWindow.mainloop()


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

    mistake = deltaY + deltaY - deltaX
    curX = xStart
    curY = yStart

    if flag:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if mistake >= 0:
                curX += stepX
                mistake -= deltaX + deltaX
            curY += stepY
            mistake += deltaY + deltaY
    else:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if mistake >= 0:
                curY += stepY
                mistake -= deltaY + deltaY
            curX += stepX
            mistake += deltaX + deltaX


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

    mistake = -1
    curX = xStart
    curY = yStart

    curCol = list(colors.to_rgb(curColorLines))
    backColor = list(colors.to_rgb(curColorBackground))
    for k in range(3):
        curCol[k] *= 255
        backColor[k] *= 255

    if flag:
        for i in range(deltaX):
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * (1 + mistake)), niceRound(curCol[1] + (backColor[1] - curCol[1]) * (1 + mistake)),
                        niceRound(curCol[2] + (backColor[2] - curCol[2]) * (1 + mistake))), (curX, curY))
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * (- mistake)), niceRound(curCol[1] + (backColor[1] - curCol[1]) * (- mistake)),
                              niceRound(curCol[2] + (backColor[2] - curCol[2]) * (- mistake))), (curX, curY + stepY))
            if mistake >= 0:
                curX += stepX
                mistake -= 1
            curY += stepY
            mistake += tngModule
    else:
        for i in range(deltaX):
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * (1 + mistake)), niceRound(curCol[1] + (backColor[1] - curCol[1]) * (1 + mistake)),
                              niceRound(curCol[2] + (backColor[2] - curCol[2]) * (1 + mistake))), (curX, curY))
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * (- mistake)), niceRound(curCol[1] + (backColor[1] - curCol[1]) * (- mistake)),
                              niceRound(curCol[2] + (backColor[2] - curCol[2]) * (- mistake))), (curX, curY + stepY))

            if mistake >= 0:
                curY += stepY
                mistake -= 1
            curX += stepX
            mistake += tngModule


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

    mistake = 1 / 2
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
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * mistake), niceRound(curCol[1] + (backColor[1] - curCol[1]) * mistake),
                              niceRound(curCol[2] + (backColor[2] - curCol[2]) * mistake)), (curX, curY))

            if mistake >= correction:
                curX += stepX
                mistake -= correction + tngModule
            curY += stepY
            mistake += tngModule
    else:
        for i in range(deltaX):
            image.put(rgb2hex(niceRound(curCol[0] + (backColor[0] - curCol[0]) * mistake), niceRound(curCol[1] + (backColor[1] - curCol[1]) * mistake),
                              niceRound(curCol[2] + (backColor[2] - curCol[2]) * mistake)), (curX, curY))

            if mistake >= correction:
                curY += stepY
                mistake -= correction + tngModule
            curX += stepX
            mistake += tngModule


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

    mistake = tngModule - 0.5
    curX = xStart
    curY = yStart

    if flag:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if mistake >= 0:
                curX += stepX
                mistake -= 1
            curY += stepY
            mistake += tngModule
    else:
        for i in range(deltaX):
            image.put(curColorLines, (curX, curY))

            if mistake >= 0:
                curY += stepY
                mistake -= 1
            curX += stepX
            mistake += tngModule


def DDAline(image, xStart, xEnd, yStart, yEnd):
    if xStart == xEnd and yStart == yEnd:
        image.put(curColorLines, (xStart, yStart))
        return

    if abs(xStart - xEnd) > abs(yStart - yEnd):
        length = abs(xStart - xEnd)
    else:
        length = abs(yStart - yEnd)

    deltaX = (xEnd - xStart) / length
    deltaY = (yEnd - yStart) / length

    curX = xStart
    curY = yStart

    for i in range(length):
        image.put(curColorLines, (niceRound(curX), niceRound(curY)))
        curX += deltaX
        curY += deltaY
        i += 1


def printRasterLine(image, entryXS, entryXE, entryYS, entryYE, combo):
    curAlg = combo.get()

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
           command = lambda: printRasterLine(img, entryXFirst, entryXSecond, entryYFirst, entryYSecond, listBox)).grid(row = 5, columnspan = 5)

    Label(rootWindow, text = "────────────────────────────────────────────────────────────────────────────────", font = fontSettingLower, width = 79).grid(
        row = 6, columnspan = 6, sticky = NW)
    Label(rootWindow, text = "Угловой шаг при построении отрезков (в градусах): ", font = fontSettingLower).grid(row = 7, columnspan = 2)
    angleEntry = Entry(rootWindow, font = fontSettingLower, width = 13).grid(row = 7, column = 2)

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
    lenghEntry = Entry(rootWindow, font = fontSettingLower).grid(row = 9, column = 1)

    Button(rootWindow, text = "Исследование визуальных характеристик отрезков,\n построенных разными алгоритмами", font = fontSettingLower, command = print(),
           width = 50).grid(row = 10, columnspan = 5)
    Button(rootWindow, text = "Исследование временных характеристик", font = fontSettingLower, command = print(), width = 50).grid(row = 11, columnspan = 5)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

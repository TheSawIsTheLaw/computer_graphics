from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib import colors
from colormap import rgb2hex
from datetime import datetime
from lab_04.shittyFuncs import niceRound

from lab_04.circleAlgs import *
from lab_04.ellipseAlgs import *

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

method = 0
figure = 1
img = 0

curColorLines = "#000000"
curColorBackground = "#ffffff"


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Лабораторная работа 4, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритмов построения окружностей и эллипсов.\n\n"
                 "Реализовать и исследовать следующие алгоритмы построения отрезков и эллипсов:\n"
                 "Алгоритм на основе канонического уравнения\n"
                 "Алгоритм на основе параметрического уравнения\n"
                 "Алгоритм Брезенхема\n"
                 "Алгоритм средней точки\n"
                 "Алгоритм Tkinter Canvas\n"
                 "Предоставить сравнение визуальных характеристик построенных окружностей \nи исследование временных характеристик").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(canvasBackgroundColor, rootWindow, row, column, canvasWindow):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = row, y = column)
    canvasWindow.config(bg = curColorBackground)


def chooseLinesColor(canvasWindow, rootWindow, row, column):
    global curColorLines
    curColorLines = colorchooser.askcolor()[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = row, y = column)


def clearImage(canvasWindow):
    canvasWindow.delete("all")
    global img
    img = PhotoImage(width = 880, height = 1017)
    canvasWindow.create_image((440, 508), image = img, state = "normal")
    canvasWindow.place(x = 960, y = 0)


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
        image.put(i[2], (niceRound(i[0]), niceRound(i[1])))


def drawMiddlePointCircle(xCenter, yCenter, radius):
    drawArray = middlePointCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawBresenhamCircle(xCenter, yCenter, radius):
    drawArray = bresenhamCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawParameterCircle(xCenter, yCenter, radius):
    drawArray = parameterCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawCanonicalCircle(xCenter, yCenter, radius):
    drawArray = canonicalCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawTkinterCircle(canvasWindow, xCenter, yCenter, radius):
    canvasWindow.create_oval(xCenter - radius,
                             yCenter - radius, xCenter + radius,
                             yCenter + radius, outline = curColorLines)


def drawMiddlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY):
    drawArray = middlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY)
    drawArr(img, drawArray)


def drawBresenhamEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = bresenhamEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawParameterEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = parameterEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawCanonicalEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = canonicalEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawTkinterEllipse(xCenter, yCenter, radiusX, radiusY, canvasWindow):
    canvasWindow.create_oval(xCenter - radiusX, yCenter - radiusY,
                             xCenter + radiusX, yCenter + radiusY,
                             outline = curColorLines)


def drawEllipse(comboAlg, xCenterEnt, yCenterEnt, radiusXEnt, radiusYEnt, canvasWindow):
    got = comboAlg.get()
    xCenter = int(xCenterEnt.get())
    yCenter = int(yCenterEnt.get())
    radiusX = int(radiusXEnt.get())
    radiusY = int(radiusYEnt.get())

    alg = got[0]
    if alg == "1":
        drawCanonicalEllipse(xCenter, yCenter, radiusX, radiusY)
    if alg == "2":
        drawParameterEllipse(xCenter, yCenter, radiusX, radiusY)
    if alg == "3":
        drawBresenhamEllipse(xCenter, yCenter, radiusX, radiusY)
    if alg == "4":
        drawMiddlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY)
    if alg == "5":
        drawTkinterEllipse(xCenter, yCenter, radiusX, radiusY, canvasWindow)


def drawCircle(comboAlg, xCenterEnt, yCenterEnt, radiusEnt, canvasWindow):
    got = comboAlg.get()
    xCenter = int(xCenterEnt.get())
    yCenter = int(yCenterEnt.get())
    radius = int(radiusEnt.get())

    alg = got[0]
    if alg == "1":
        drawCanonicalCircle(xCenter, yCenter, radius)
    if alg == "2":
        drawParameterCircle(xCenter, yCenter, radius)
    if alg == "3":
        drawBresenhamCircle(xCenter, yCenter, radius)
    if alg == "4":
        drawMiddlePointCircle(xCenter, yCenter, radius)
    if alg == "5":
        drawTkinterCircle(canvasWindow, xCenter, yCenter, radius)


def drawCurve(comboFig, comboAlg, xCenterCir, yCenterCir, radiusCir, xCenterEll,
              yCenterEll, radiusF, radiusS, canvasWindow):
    got = comboFig.get()
    if got[0] == "1":
        drawCircle(comboAlg, xCenterCir, yCenterCir, radiusCir, canvasWindow)
    else:
        drawEllipse(comboAlg, xCenterEll, yCenterEll, radiusF, radiusS, canvasWindow)


def spectralTkinterCircle(xCenter, yCenter, radius, step, end, canvasWindow):
    for i in range(radius, end + step, step):
        drawTkinterCircle(canvasWindow, xCenter, yCenter, radius + i)


def spectralMiddlePointCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawMiddlePointCircle(xCenter, yCenter, radius + i)


def spectralBresenhamCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawBresenhamCircle(xCenter, yCenter, radius + i)


def spectralParameterCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawParameterCircle(xCenter, yCenter, radius + i)


def spectralCanonicalCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawCanonicalCircle(xCenter, yCenter, radius + i)


def spectralCircles(comboAlg, xCenterEnt, yCenterEnt, radiusEnt, stepEnt, endRadEnt,
                    canvasWindow):
    got = comboAlg.get()

    xCenter = int(xCenterEnt.get())
    yCenter = int(yCenterEnt.get())
    radius = int(radiusEnt.get())
    step = int(stepEnt.get())
    end = int(endRadEnt.get())

    alg = got[0]
    if alg == "1":
        spectralCanonicalCircle(xCenter, yCenter, radius, step, end)
    if alg == "2":
        spectralParameterCircle(xCenter, yCenter, radius, step, end)
    if alg == "3":
        spectralBresenhamCircle(xCenter, yCenter, radius, step, end)
    if alg == "4":
        spectralMiddlePointCircle(xCenter, yCenter, radius, step, end)
    if alg == "5":
        spectralTkinterCircle(xCenter, yCenter, radius, step, end, canvasWindow)


def spectralTkinterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop, canvasWindow):
    i = 0
    xi = stepX
    yi = stepY
    while i < stop:
        drawTkinterEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi, canvasWindow)
        i += 1
        xi += stepX
        yi += stepY


def spectralMiddlePointEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = stepX
    yi = stepY
    while i < stop:
        drawMiddlePointEllipseAlg(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        xi += stepX
        yi += stepY


def spectralBresenhamEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = stepX
    yi = stepY
    while i < stop:
        drawBresenhamEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        xi += stepX
        yi += stepY


def spectralParameterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = stepX
    yi = stepY
    while i < stop:
        drawParameterEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        xi += stepX
        yi += stepY


def spectralCanonicalEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = stepX
    yi = stepY
    while i < stop:
        drawCanonicalEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        xi += stepX
        yi += stepY


def spectralEllipse(comboAlg, xCenterEnt, yCenterEnt, xRadiusEnt, yRadiusEnt, stepXEnt, stepYEnt, stopEnt, canvasWindow):
    got = comboAlg.get()
    alg = got[0]

    xCenter = int(xCenterEnt.get())
    yCenter = int(yCenterEnt.get())
    xRadius = int(xRadiusEnt.get())
    yRadius = int(yRadiusEnt.get())
    stepX = int(stepXEnt.get())
    stepY = int(stepYEnt.get())
    stop = int(stopEnt.get())

    if alg == "1":
        spectralCanonicalEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "2":
        spectralParameterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "3":
        spectralBresenhamEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "4":
        spectralMiddlePointEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "5":
        spectralTkinterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop, canvasWindow)


def spectralAnal(comboFig, comboAlg, xCenter, yCenter, radiusF, radiusS,
                 stepX, stepY, stopX, stopY, canvasWindow):
    got = comboFig.get()
    if got[0] == "1":
        spectralCircles(comboAlg, xCenter, yCenter, radiusF, stepX, stopX, canvasWindow)
    else:
        spectralEllipse(comboAlg, xCenter, yCenter, radiusF, radiusS, stepX, stepY, stopY, canvasWindow)


def ellipseTimeResearch(canvasWindow):
    masTime = []
    masAllTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            canonicalEllipseAlg(500, 500, i, i + 250, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.015 and not curTime < prev - 0.015:
            print(1)
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            parameterEllipseAlg(500, 500, i, i + 250, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.015 and not curTime < prev - 0.015:
            print(2)
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            bresenhamEllipseAlg(500, 500, i, i + 250, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.015 and not curTime < prev - 0.015:
            print(3)
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            middlePointEllipseAlg(500, 500, i, i + 250, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.015 and not curTime < prev - 0.015:
            print(4)
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    masAllTime.append(masTime)

    fig = plt.figure(figsize = (18, 10))
    plot = fig.add_subplot()
    ran = []
    for i in range(1, 10002, 250):
        ran.append(i)

    plot.plot(ran, masAllTime[0], label = "Алгоритм Брезенхема")
    plot.plot(ran, masAllTime[1], label = "Алгоритм на основе параметрического уравнения")
    plot.plot(ran, masAllTime[2], label = "Алгоритм на основе канонического уравнения")
    plot.plot(ran, masAllTime[3], label = "Алгоритм средней точки")
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов построения эллипсов")
    plt.ylabel("Затраченное время")
    plt.xlabel("Длина радиуса")
    plt.show()


def circleTimeResearch(canvasWindow):
    masTime = []
    masAllTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            canonicalCircleAlg(500, 500, i, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.01 and not curTime < prev - 0.01:
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            parameterCircleAlg(500, 500, i, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.01 and not curTime < prev - 0.01:
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            bresenhamCircleAlg(500, 500, i, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.01 and not curTime < prev - 0.01:
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    curTime = 0
    masAllTime.append(masTime)
    masTime = []
    i = 1
    prev = 0

    while i <= 10001:
        curTime = 0
        for j in range(10):
            timeTempStart = datetime.now()
            middlePointCircleAlg(500, 500, i, curColorLines)
            timeTempEnd = datetime.now()
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
        if not curTime > prev + 0.01 and not curTime < prev - 0.01:
            prev = curTime
            curTime /= 10
            masTime.append(curTime)
            i += 250

    masAllTime.append(masTime)

    fig = plt.figure(figsize = (18, 10))
    plot = fig.add_subplot()
    ran = []
    for i in range(1, 10002, 250):
        ran.append(i)

    plot.plot(ran, masAllTime[0], label = "Алгоритм Брезенхема")
    plot.plot(ran, masAllTime[1], label = "Алгоритм на основе параметрического уравнения")
    plot.plot(ran, masAllTime[2], label = "Алгоритм на основе канонического уравнения")
    plot.plot(ran, masAllTime[3], label = "Алгоритм средней точки")
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов построения окружностей")
    plt.ylabel("Затраченное время")
    plt.xlabel("Длина радиуса")
    plt.show()


def timeResearch(canvasWindow, comboFig):
    fig = comboFig.get()
    if fig[0] == "1":
        circleTimeResearch(canvasWindow)
    else:
        ellipseTimeResearch(canvasWindow)


def makeMainWindow():
    """
            Функция Создания главного окна
        """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 4, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 880, height = 1016, borderwidth = 5, relief = RIDGE)
    global img
    img = PhotoImage(width = 880, height = 1018)
    canvasWindow.create_image((440, 509), image = img, state = "normal")
    canvasWindow.place(x = 960, y = 0)

    # Выбор метода построения
    Label(rootWindow, text = "Алгоритм построения:", font = fontSettingLower).place(x = 5, y = 10)
    comboAlg = ttk.Combobox(rootWindow, width = 115, textvariable = method, state = 'readonly', values =
    ('1. Алгоритм на основе канонического уравнения',
     '2. Алгоритм на основе параметрического уравнения',
     '3. Алгоритм Брезенхема',
     '4. Алгоритм средней точки',
     '5. Алгоритм Tkinter Canvas'))
    comboAlg.place(x = 250, y = 15)
    comboAlg.current(0)
    comboAlg.current(0)
    Label(rootWindow, text = "Тип кривой:", font = fontSettingLower).place(x = 113, y = 40)
    comboFig = ttk.Combobox(rootWindow, width = 115, textvariable = figure, state = 'readonly', values =
    ('1. Окружность',
     '2. Эллипс'))
    comboFig.place(x = 250, y = 45)
    comboFig.current(0)

    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = 250, y = 82)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, height = 2,
           command = lambda: chooseLinesColor(canvasLinesColor, rootWindow, 250, 82)).place(x = 40, y = 80)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 82)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, height = 2,
           command = lambda: chooseBackgroundColor(canvasBackgroundColor, rootWindow, 660, 82, canvasWindow)).place(x = 500, y = 80)

    Label(rootWindow, text = "Параметры окружности:", font = fontSettingLabels).place(x = 0, y = 160)

    Label(rootWindow, text = "Центр по оси X:", font = fontSettingLower).place(x = 0, y = 200)
    xCenterCircle = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    xCenterCircle.place(x = 190, y = 203)

    Label(rootWindow, text = "Центр по оси Y:", font = fontSettingLower).place(x = 300, y = 200)
    yCenterCircle = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    yCenterCircle.place(x = 490, y = 203)

    Label(rootWindow, text = "Радиус:", font = fontSettingLower).place(x = 700, y = 200)
    cirRad = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    cirRad.place(x = 790, y = 203)

    Label(rootWindow, text = "Параметры эллипса:", font = fontSettingLabels).place(x = 0, y = 250)

    Label(rootWindow, text = "Центр по оси X:", font = fontSettingLower).place(x = 0, y = 290)
    xCenterEllipse = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    xCenterEllipse.place(x = 190, y = 293)

    Label(rootWindow, text = "Центр по оси Y:", font = fontSettingLower).place(x = 0, y = 330)
    yCenterEllipse = Entry(rootWindow, width = 5, font = fontSettingLower)
    yCenterEllipse.place(x = 190, y = 333)

    Label(rootWindow, text = "Размер полуоси вдоль X:", font = fontSettingLower).place(x = 500, y = 290)
    ellRadX = Entry(rootWindow, width = 5, font = fontSettingLower)
    ellRadX.place(x = 780, y = 293)

    Label(rootWindow, text = "Размер полуоси вдоль Y:", font = fontSettingLower).place(x = 500, y = 330)
    ellRadY = Entry(rootWindow, width = 5, font = fontSettingLower)
    ellRadY.place(x = 780, y = 333)

    drawCurveButton = Button(rootWindow, text = "Построить", font = fontSettingLower, width = 79,
                       command = lambda: drawCurve(comboFig, comboAlg,
                                                   xCenterCircle, yCenterCircle, cirRad,
                                                   xCenterEllipse, yCenterEllipse,
                                                   ellRadX, ellRadY, canvasWindow))
    drawCurveButton.place(x = 0, y = 370)

    Label(rootWindow, font = fontSettingLabels, text = "Параметры спектра:").place(x = 0, y = 420)

    Label(rootWindow, font = fontSettingLower, text = "Центр по оси X:").place(x = 0, y = 460)
    xCenterAnalysis = Entry(rootWindow, font = fontSettingLower, width = 5)
    xCenterAnalysis.place(x = 190, y = 463)

    Label(rootWindow, font = fontSettingLower, text = "Центр по оси Y:").place(x = 0, y = 500)
    yCenterAnalysis = Entry(rootWindow, font = fontSettingLower, width = 5)
    yCenterAnalysis.place(x = 190, y = 503)

    Label(rootWindow, font = fontSettingLower, text = "Начальный размер полуоси вдоль X \n(в случае окружности - её радиус):").place(x = 300, y = 460)
    fOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    fOs.place(x = 720, y = 488)

    Label(rootWindow, font = fontSettingLower, text = "Начальный размер полуоси эллипса вдоль оси Y:").place(x = 0, y = 540)
    sOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    sOs.place(x = 545, y = 543)

    Label(rootWindow, font = fontSettingLower, text = "Конечная длина радиуса окружности:").place(x = 0, y = 580)
    stopFOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    stopFOs.place(x = 410, y = 583)

    Label(rootWindow, font = fontSettingLower, text = "Количество эллипсов:").place(x = 0, y = 620)
    stopSOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    stopSOs.place(x = 250, y = 623)

    Label(rootWindow, font = fontSettingLower, text = "Шаг изменения полуоси вдоль X (или радиуса окружности):").place(x = 0, y = 660)
    dFOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    dFOs.place(x = 665, y = 663)

    Label(rootWindow, font = fontSettingLower, text = "Шаг изменения полуоси вдоль Y:").place(x = 0, y = 700)
    dSOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    dSOs.place(x = 370, y = 703)

    Button(rootWindow, text = "Построить спектр", font = fontSettingLower, width = 79, command = lambda: spectralAnal(comboFig, comboAlg, xCenterAnalysis,
                                                                               yCenterAnalysis, fOs, sOs, dFOs, dSOs, stopFOs, stopSOs,
                                                                               canvasWindow)).place(x = 0, y = 760)
    Button(rootWindow, text = "Временные характеристики предоставленных алгоритмов", font = fontSettingLower, width = 79, command = lambda: timeResearch(canvasWindow, comboFig)).place(x = 0, y = 801)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

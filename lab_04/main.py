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
figure = 1
img = 0

curColorLines = "#000000"
curColorBackground = "#ffffff"


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


def makeItentity(curCol, backColor, acc):
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

def reflectPointsXY(pointsArray, xCenter, yCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((pointsArray[i][1] - yCenter + xCenter, pointsArray[i][0] - xCenter + yCenter,
                            pointsArray[i][2]))


def reflectPointsY(pointsArray, xCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((-(pointsArray[i][0] - xCenter) + xCenter, pointsArray[i][1], pointsArray[i][2]))


def reflectPointsX(pointsArray, yCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((pointsArray[i][0], -(pointsArray[i][1] - yCenter) + yCenter, pointsArray[i][2]))


def canonicalCircleAlg(xCenter, yCenter, radius, colour = "#000000"):
    pointsArray = []
    sqrRad = radius * radius
    for curX in range(xCenter, round(xCenter + radius / sqrt(2)) + 1):
        curY = yCenter + sqrt(sqrRad - (curX - xCenter) * (curX - xCenter))
        pointsArray.append((curX, curY, colour))
    reflectPointsXY(pointsArray, xCenter, yCenter)
    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray


def drawArr(image, pointsArray):
    for i in pointsArray:
        image.put(i[2], (niceRound(i[0]), niceRound(i[1])))


def drawCanonicalCircle(xCenter, yCenter, radius):
    drawArray = canonicalCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawCircle(comboAlg, xCenterEnt, yCenterEnt, radiusEnt):
    got = comboAlg.get()
    xCenter = int(xCenterEnt.get())
    yCenter = int(yCenterEnt.get())
    radius = int(radiusEnt.get())

    if got[0] == "1":
        drawCanonicalCircle(xCenter, yCenter, radius)


def drawCurve(comboFig, comboAlg, xCenter, yCenter, radiusF, radiusS = 0):
    got = comboFig.get()
    if got[0] == "1":
        drawCircle(comboAlg, xCenter, yCenter, radiusF)


def makeMainWindow():
    """
            Функция Создания главного окна
        """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 4, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 880, height = 1016, borderwidth = 5, relief = RIDGE)
    global img
    img = PhotoImage(width = 880, height = 1017)
    canvasWindow.create_image((440, 508), image = img, state = "normal")
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
    Label(rootWindow, text = "Алгоритм построения:", font = fontSettingLower).place(x = 5, y = 40)
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
                       command = lambda: drawCurve(comboFig, comboAlg, xCenterCircle, yCenterCircle, cirRad))
    drawCurveButton.place(x = 0, y = 370)

    Label(rootWindow, font = fontSettingLabels, text = "Параметры спектра:").place(x = 0, y = 420)

    Label(rootWindow, font = fontSettingLower, text = "Центр по оси X:").place(x = 0, y = 460)
    xCenterAnalysis = Entry(rootWindow, font = fontSettingLower, width = 5)
    xCenterAnalysis.place(x = 190, y = 463)

    Label(rootWindow, font = fontSettingLower, text = "Центр по оси Y:").place(x = 0, y = 500)
    yCenterAnalysis = Entry(rootWindow, font = fontSettingLower, width = 5)
    yCenterAnalysis.place(x = 190, y = 503)

    Label(rootWindow, font = fontSettingLower, text = "Размер полуоси вдоль X \n(в случае окружности - её радиус):").place(x = 300, y = 460)
    fOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    fOs.place(x = 720, y = 488)

    Label(rootWindow, font = fontSettingLower, text = "Размер полуоси эллипса вдоль оси Y:").place(x = 0, y = 540)
    sOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    sOs.place(x = 425, y = 543)

    Label(rootWindow, font = fontSettingLower, text = "Шаг изменения полуоси вдоль X (или радиуса окружности):").place(x = 0, y = 580)
    dFOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    dFOs.place(x = 665, y = 583)

    Label(rootWindow, font = fontSettingLower, text = "Шаг изменения полуоси вдоль Y:").place(x = 0, y = 620)
    dSOs = Entry(rootWindow, font = fontSettingLower, width = 8)
    dSOs.place(x = 370, y = 623)

    Button(rootWindow, text = "Построить спектр", font = fontSettingLower, width = 79, command = print()).place(x = 0, y = 670)
    Button(rootWindow, text = "Сравнить визуальные характеристики", font = fontSettingLower, width = 79, command = print()).place(x = 0, y = 711)
    Button(rootWindow, text = "Временные характеристики предоставленных алгоритмов", font = fontSettingLower, width = 79, command = print()).place(x = 0, y = 752)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

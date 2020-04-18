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
           command = lambda: chooseLinesColor(canvasLinesColor, rootWindow, 8, 1)).place(x = 40, y = 80)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 82)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, height = 2,
           command = lambda: chooseBackgroundColor(canvasBackgroundColor, rootWindow, 8, 3, canvasWindow)).place(x = 500, y = 80)

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
    yCenterEllipse = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    yCenterEllipse.place(x = 190, y = 333)

    Label(rootWindow, text = "Размер полуоси по X:", font = fontSettingLower).place(x = 500, y = 290)
    ellRadX = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    ellRadX.place(x = 750, y = 293)

    Label(rootWindow, text = "Размер полуоси по Y:", font = fontSettingLower).place(x = 500, y = 330)
    ellRadY = Entry(rootWindow, width = 5, font = fontSettingLower, command = print())
    ellRadY.place(x = 750, y = 333)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

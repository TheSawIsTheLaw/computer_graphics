from tkinter import *
from re import *
from math import *

fontSettingLabels = ("Source code pro", 20)
fontSettingLower = ("Source code pro", 16)

dotsArrayEll = []
dotsArrayHead = []
dotsArrayMouth = []
dotsArrayLeftLeg = []
dotsArrayRightLeg = []
dotsArrayTale = []
dotsArrayWing = []


def fillEll(canvasWindow):
    global dotsArrayEll
    for i in range(-200, 201):
        dotsArrayEll.append([i, -sqrt(20000 - (i * i) / 2)])

    for i in range(200, -201, -1):
        dotsArrayEll.append([i, sqrt(20000 - (i * i) / 2)])

    for i in dotsArrayEll:
        i[0] += 550
        i[1] += 550

    for i in range(len(dotsArrayEll) - 1):
        canvasWindow.create_line(dotsArrayEll[i][0], dotsArrayEll[i][1], dotsArrayEll[i + 1][0], dotsArrayEll[i + 1][1], fill = "blue", width = 3)


def fillHead(canvasWindow):
    global dotsArrayHead
    for i in range(-50, 51):
        dotsArrayHead.append([i, -sqrt(2500 - i * i)])

    for i in range(50, -51, -1):
        dotsArrayHead.append([i, sqrt(2500 - i * i)])

    for i in dotsArrayHead:
        i[0] += 400
        i[1] += 398

    for i in range(len(dotsArrayHead) - 1):
        canvasWindow.create_line(dotsArrayHead[i][0], dotsArrayHead[i][1], dotsArrayHead[i + 1][0], dotsArrayHead[i + 1][1], fill = "blue", width = 3)


def fillMouth(canvasWindow):
    global dotsArrayMouth
    dotsArrayMouth.append([-10, -10])
    dotsArrayMouth.append([-10, 10])
    dotsArrayMouth.append([-60, 0])

    for i in dotsArrayMouth:
        i[0] += 370
        i[1] += 398

    for i in range(len(dotsArrayMouth) - 1):
        canvasWindow.create_line(dotsArrayMouth[i][0], dotsArrayMouth[i][1], dotsArrayMouth[i + 1][0], dotsArrayMouth[i + 1][1], fill = "blue", width = 3)
    canvasWindow.create_line(dotsArrayMouth[0][0], dotsArrayMouth[0][1], dotsArrayMouth[2][0], dotsArrayMouth[2][1], fill = "blue", width = 3)

def fillLeftLeg(canvasWindow):
    dotsArrayLeftLeg.append([500, 686])
    dotsArrayLeftLeg.append([450, 786])

    canvasWindow.create_line(dotsArrayLeftLeg[0][0], dotsArrayLeftLeg[0][1], dotsArrayLeftLeg[1][0], dotsArrayLeftLeg[1][1], fill = "blue", width = 3)


def fillRightLeg(canvasWindow):
    dotsArrayRightLeg.append([600, 686])
    dotsArrayRightLeg.append([650, 786])

    canvasWindow.create_line(dotsArrayRightLeg[0][0], dotsArrayRightLeg[0][1], dotsArrayRightLeg[1][0], dotsArrayRightLeg[1][1], fill = "blue", width = 3)


def fillTale(canvasWindow):
    dotsArrayTale.append([720, 560])
    dotsArrayTale.append([810, 490])
    dotsArrayTale.append([690, 480])

    for i in range(len(dotsArrayTale) - 1):
        canvasWindow.create_line(dotsArrayTale[i][0], dotsArrayTale[i][1], dotsArrayTale[i + 1][0], dotsArrayTale[i + 1][1], fill = "blue", width = 3)
    canvasWindow.create_line(dotsArrayTale[0][0], dotsArrayTale[0][1], dotsArrayTale[2][0], dotsArrayTale[2][1], fill = "blue", width = 3)


def fillWing(canvasWindow):
    dotsArrayWing.append([550, 550])
    dotsArrayWing.append([650, 550])
    dotsArrayWing.append([720, 700])

    for i in range(len(dotsArrayWing) - 1):
        canvasWindow.create_line(dotsArrayWing[i][0], dotsArrayWing[i][1], dotsArrayWing[i + 1][0], dotsArrayWing[i + 1][1], fill = "blue", width = 3)
    canvasWindow.create_line(dotsArrayWing[0][0], dotsArrayWing[0][1], dotsArrayWing[2][0], dotsArrayWing[2][1], fill = "blue", width = 3)


def startArrays(canvasWindow):
    fillEll(canvasWindow)
    fillHead(canvasWindow)
    fillLeftLeg(canvasWindow)
    fillRightLeg(canvasWindow)
    fillMouth(canvasWindow)
    fillTale(canvasWindow)
    fillWing(canvasWindow)

    #printAll()


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Показания к работе с ПО"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Пау...\n"
    "Лабораторная работа 2, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()

    Label(jobWindow, font = fontSettingLabels,
          text = "Преобразование изображения\n\nПо заданному исходному изображению реализовать три функции преобразования данного изображения:\n\n"
                 "1. Перенос по заданным смещениям целого типа\n\n"
                 "2. Масштабирование по двум заданным коэффициентам и двум координатам центра масштабирования\n\n"
                 "3. Поворот на заданный угол и координатам центра поворота").grid()

    jobWindow.mainloop()


def makeCascadeMenu(rootWindow):
    """
        Функция создания каскадного меню
    """
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu = rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label = 'Формулировка задания', command = makeJobWindow)
    jobMenu.add_command(label = 'Справка', command = makeReference)

    rootMenu.add_cascade(label = 'Справка', menu = jobMenu)


def makeMainWindow():
    """
        Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 2, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 920)

    Label(rootWindow, text = "Перенос", font = fontSettingLabels).grid(row = 0, column = 0, rowspan = 1, columnspan = 2)
    transferEntryX = Entry(rootWindow, font = fontSettingLower)
    transferEntryX.grid(row = 1, column = 1)
    transferEntryY = Entry(rootWindow, font = fontSettingLower)
    transferEntryY.grid(row = 2, column = 1)
    Label(rootWindow, text = "dx:", font = fontSettingLower).grid(row = 1, column = 0, rowspan = 1)
    Label(rootWindow, text = "dy:", font = fontSettingLower).grid(row = 2, column = 0, rowspan = 1)
    Button(rootWindow, font = fontSettingLower, text = "Выполнить преобразование\n'перенос'", command = lambda: print("lul")).grid(row = 3, column = 0,
                                                                                                                                   columnspan = 2)
    Label(font = fontSettingLower,
          text = "--------------------------------------------------------------------------------------------------------------").grid(row = 4, columnspan = 2)

    Label(rootWindow, text = "Масштабирование", font = fontSettingLabels).grid(row = 5, column = 0, rowspan = 1, columnspan = 2)
    masstXCoef = Entry(rootWindow, font = fontSettingLower)
    masstYCoef = Entry(rootWindow, font = fontSettingLower)
    centerX = Entry(rootWindow, font = fontSettingLower)
    centerY = Entry(rootWindow, font = fontSettingLower)

    masstXCoef.grid(row = 6, column = 1)
    masstYCoef.grid(row = 7, column = 1)
    centerX.grid(row = 8, column = 1)
    centerY.grid(row = 9, column = 1)

    Label(rootWindow, font = fontSettingLower, text = "Коэффициент масштабирования по оси X:").grid(row = 6, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Коэффициент масштабирования по оси Y:").grid(row = 7, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Координата центра массштабирования по оси X:").grid(row = 8, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Координата центра массштабирования по оси Y:").grid(row = 9, column = 0)

    Button(rootWindow, font = fontSettingLower, text = "Выполнить преобразование\n'масштабирование'", command = lambda: print("lul")).grid(row = 10, column = 0,
                                                                                                                                           columnspan = 2)
    Label(font = fontSettingLower,
          text = "--------------------------------------------------------------------------------------------------------------").grid(row = 11,
                                                                                                                                        columnspan = 2)

    Label(rootWindow, font = fontSettingLower, text = "Поворот").grid(row = 12, columnspan = 2)
    angleRotation = Entry(rootWindow, font = fontSettingLower)
    centerRotationX = Entry(rootWindow, font = fontSettingLower)
    centerRotationY = Entry(rootWindow, font = fontSettingLower)

    angleRotation.grid(row = 13, column = 1)
    centerRotationX.grid(row = 14, column = 1)
    centerRotationY.grid(row = 15, column = 1)

    Label(rootWindow, font = fontSettingLower, text = "Угол поворота:").grid(row = 13, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Центр поворота по оси X:").grid(row = 14, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Центр поворота по оси Y:").grid(row = 15, column = 0)

    Button(rootWindow, font = fontSettingLower, text = "Выполнить преобразование\n'поворот'", command = lambda: startArrays(canvasWindow)).grid(row = 16,
                                                                                                                                                columnspan = 2)

    Label(font = fontSettingLower,
          text = "--------------------------------------------------------------------------------------------------------------").grid(row = 17,
                                                                                                                                        columnspan = 2)
    Button(rootWindow, font = fontSettingLower, text = "Вернуться на шаг назад", command = lambda: print("lul")).grid(row = 18, columnspan = 2)

    canvasWindow = Canvas(rootWindow, bg = "yellow", width = 1075, height = 1055)
    canvasWindow.grid(row = 0, column = 3, rowspan = 20)

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()


makeMainWindow()

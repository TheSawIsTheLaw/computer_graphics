from tkinter import *
from re import *
from math import cos, pi, sin, radians

fontSettingLabels = ("Source code pro", 20)
fontSettingLower = ("Source code pro", 16)

dotsArrayEll = []
dotsArrayHead = []
dotsArrayMouth = []
dotsArrayLeftLeg = []
dotsArrayRightLeg = []
dotsArrayTale = []

def startArrays():
    print()

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

    Label(jobWindow, font = fontSettingLabels, text = "Преобразование изображения\n\nПо заданному исходному изображению реализовать три функции преобразования данного изображения:\n\n"
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
    transferEntryX.grid(row=1, column=1)
    transferEntryY = Entry(rootWindow, font = fontSettingLower)
    transferEntryY.grid(row = 2, column = 1)
    Label(rootWindow, text = "dx:", font = fontSettingLower).grid(row = 1, column = 0, rowspan = 1)
    Label(rootWindow, text = "dy:", font = fontSettingLower).grid(row = 2, column = 0, rowspan = 1)
    Button(rootWindow, font = fontSettingLower, text = "Выполнить преобразование\n'перенос'", command=lambda: print("lul")).grid(row = 3, column = 0, columnspan = 2)
    Label(font = fontSettingLower, text = "--------------------------------------------------------------------------------------------------------------").grid(row = 4, columnspan = 2)

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
          text = "--------------------------------------------------------------------------------------------------------------").grid(row = 11, columnspan = 2)

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

    Button(rootWindow, font = fontSettingLower, text = "Выполнить преобразование\n'поворот'", command = lambda: print("lul")).grid(row = 16, columnspan = 2)

    Label(font = fontSettingLower,
          text = "--------------------------------------------------------------------------------------------------------------").grid(row = 17,
                                                                                                                                        columnspan = 2)
    Button(rootWindow, font = fontSettingLower, text = "Вернуться на шаг назад", command = lambda: print("lul")).grid(row = 18, columnspan = 2)

    canvasWindow = Canvas(rootWindow, bg = "black", width = 1075, height = 1055)
    canvasWindow.grid(row = 0, column = 3, rowspan = 20)

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()


makeMainWindow()

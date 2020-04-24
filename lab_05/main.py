from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
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
    "Лабораторная работа 5, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритмов растрового заполнения сплошных областей\n"
                 "Реализуется алгоритм заполнения со списком рёбер и флагом.").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(rootWindow, row, column, canvasWindow):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = row, y = column)
    canvasWindow.config(bg = curColorBackground)


def chooseLinesColor(rootWindow, row, column):
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
        image.put(i[2], (i[0], i[1]))


def setColorButtons(rootWindow):
    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = 250, y = 182)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseLinesColor(rootWindow, 250, 82)).place(x = 40, y = 180)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 182)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseBackgroundColor(rootWindow, 660, 82)).place(x = 500, y = 180)


def setComboDelay(rootWindow):
    Label(rootWindow, text = "Задержка рисования:", font = fontSettingLower).place(x = 5, y = 140)
    comboDelay = ttk.Combobox(rootWindow, width = 80, textvariable = delay, state = 'readonly', values =
    ('Выключена',
     'Включена'))

    comboDelay.place(x = 250, y = 145)
    comboDelay.current(0)


def setImageToCanvas(canvasWindow):
    global img
    img = PhotoImage(width = 1090, height = 1016)
    canvasWindow.create_image((545, 508), image = img, state = "normal")


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 5, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.place(x = 750, y = 0)

    setComboDelay(rootWindow)

    setColorButtons(rootWindow)

    makeAlgButton = Button(rootWindow, text = "Закрасить изображённую фигуру", width = 60, font = fontSettingLower, bg = "#FF9C00", command = print())
    makeAlgButton.place(x = 5, y = 300)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = print())
    makeTimeResearch.place(x = 5, y = 600)

    Label(text = "Ввод вершин многоугольника производится с помощью мыши\n"
                 "\nЧтобы завершить рисование - \nнажмите правую кнопку мыши и фигура замкнётся.", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(text = "Алгоритм растрового заполнения \nсплошных областей со списком \nрёбер и флагом", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

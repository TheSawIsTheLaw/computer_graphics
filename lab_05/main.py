from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from time import sleep, time

from numpy import sign

from lab_04.shittyFuncs import niceRound

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

curColorLines = "#000000"
curColorBackground = "#ffffff"

pointsArray = []

prevCurEnd = []
curEndPoint = 0


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
    global pointsArray
    pointsArray.clear()
    global curEndPoint
    global prevCurEnd
    curEndPoint = 0
    prevCurEnd = []
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

def drawArr(image, pointsArray):
    for i in pointsArray:
        image.put(i[2], (i[0], i[1]))


def setColorButtons(rootWindow, canvasWindow):
    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasLinesColor.place(x = 250, y = 182)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseLinesColor(rootWindow, 250, 182)).place(x = 40, y = 180)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 50)
    canvasBackgroundColor.place(x = 660, y = 182)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, height = 2, bg = "#FF9C00",
           command = lambda: chooseBackgroundColor(rootWindow, 660, 182, canvasWindow)).place(x = 500, y = 180)


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


def click(event):
    global pointsArray
    global img
    global curEndPoint
    pointsArray.append((event.x, event.y, curColorLines))
    if len(pointsArray) >= 2 and len(pointsArray) != curEndPoint + 1:
        digitBresenham(img, pointsArray[len(pointsArray) - 2][0], pointsArray[len(pointsArray) - 1][0], pointsArray[len(pointsArray) - 2][1], pointsArray[len(pointsArray) - 1][1])


def endClick(event):
    global curEndPoint
    global pointsArray
    digitBresenham(img, pointsArray[curEndPoint][0], pointsArray[len(pointsArray) - 1][0], pointsArray[curEndPoint][1], pointsArray[len(pointsArray) - 1][1])
    global prevCurEnd
    prevCurEnd.append(curEndPoint)
    curEndPoint = len(pointsArray)


def cancelClick(event):
    global pointsArray
    if len(pointsArray) == 0:
        return
    global curEndPoint
    global curColorLines
    global curColorBackground
    tempCol = curColorLines
    curColorLines = curColorBackground
    if curEndPoint != len(pointsArray):
        digitBresenham(img, pointsArray[len(pointsArray) - 2][0], pointsArray[len(pointsArray) - 1][0], pointsArray[len(pointsArray) - 2][1], pointsArray[len(pointsArray) - 1][1])
        pointsArray.pop()
    else:
        global prevCurEnd
        curEndPoint = prevCurEnd.pop()
        digitBresenham(img, pointsArray[curEndPoint][0], pointsArray[len(pointsArray) - 1][0], pointsArray[curEndPoint][1],
                       pointsArray[len(pointsArray) - 1][1])
    curColorLines = tempCol


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 5, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.bind('<1>', click)

    canvasWindow.bind('<2>', cancelClick)

    canvasWindow.bind('<3>', endClick)

    canvasWindow.place(x = 750, y = 0)

    setComboDelay(rootWindow)

    setColorButtons(rootWindow, canvasWindow)

    makeAlgButton = Button(rootWindow, text = "Закрасить изображённую фигуру", width = 60, font = fontSettingLower, bg = "#FF9C00", command = print())
    makeAlgButton.place(x = 5, y = 300)

    makeTimeResearch = Button(rootWindow, text = "Временные характеристики алгоритма", width = 60, font = fontSettingLower, bg = "#FF9C00", command = print())
    makeTimeResearch.place(x = 5, y = 600)

    Label(text = "Ввод вершин многоугольника производится с помощью мыши\n"
                 "\nЧтобы завершить рисование - \nнажмите правую кнопку мыши и фигура замкнётся.\n"
                 "\nЧтобы отменить последнее действие -\n нажмите среднюю кнопку мыши", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 60).place(x = 5, y = 400)

    Label(text = "Алгоритм растрового заполнения \nсплошных областей со списком \nрёбер и флагом", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()
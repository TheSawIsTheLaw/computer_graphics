from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from lab_10 import example
from math import *
from numpy import arange

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

exa = 0
xyz = 0

curColorBackground = "#000000"
curColorLines = "#ffff00"

comboWhatToDraw = 1
comboRotation = 0

width = 1090
height = 1016

trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]

sf = 1


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Лабораторная работа 10, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: что-то очень инетерсное.").grid()

    jobWindow.mainloop()


def clearImage(canvasWindow):
    canvasWindow.delete("all")


def rotate_trans_matrix(rotate_matrix):
    global trans_matrix
    res_matrix = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += trans_matrix[i][k] * rotate_matrix[k][j]

    trans_matrix = res_matrix


def rotate_x(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow, rotateAngle):
    value = float(rotateAngle.get()) / 180 * pi
    rotate_matrix = [ [ 1, 0, 0, 0 ],
                       [ 0, cos(value), sin(value), 0 ],
                       [ 0, -sin(value), cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    showSurface(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow)


def rotate_y(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow, rotateAngle):
    value = float(rotateAngle.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), 0, -sin(value), 0 ],
                       [ 0, 1, 0, 0 ],
                       [ sin(value), 0, cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    showSurface(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow)


def rotate_z(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow, rotateAngle):
    value = float(rotateAngle.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), sin(value), 0, 0 ],
                       [ -sin(value), cos(value), 0, 0 ],
                       [ 0, 0, 1, 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    showSurface(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow)


def rotate(comboRotation, comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow, rotateAngle):
    print(comboRotation.curselection()[0])
    if comboRotation.curselection()[0] == 0:
        rotate_x(comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow, rotateAngle)
    elif comboRotation.curselection()[0] == 1:
        rotate_y(comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow, rotateAngle)
    elif comboRotation.curselection()[0] == 2:
        rotate_z(comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow, rotateAngle)


def transform(point):
    # point = (x, y, z)
    point.append(1) # (x, y, z, 1)
    res_point = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            res_point[i] += point[j] * trans_matrix[j][i]

    for i in range(3):
        res_point[i] *= sf # x, y, z ==> SF * x, SF * y, SF * z

    res_point[0] += height / 2
    res_point[1] += height / 2

    return res_point[:3]


def draw_pixel(x, y, canvasWindow):
    canvasWindow.create_line(x, y, x + 1, y + 1, fill=curColorLines)


def is_visible(point):
    return 0 <= point[0] < width and 0 <= point[1] < height


def draw_point(x, y, hh, lh, canvasWindow):
    if not is_visible([x, y]):
        return False

    if y > hh[x]:
        hh[x] = y
        draw_pixel(x, y, canvasWindow)

    elif y < lh[x]:
        lh[x] = y
        draw_pixel(x, y, canvasWindow)

    return True


def draw_horizon_part(p1, p2, hh, lh, canvasWindow):
    if p1[0] > p2[0]: # хочу, чтобы x2 > x1
        p1, p2 = p2, p1

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    l = dx if dx > dy else dy
    dx /= l
    dy /= l

    x, y = p1[0], p1[1]

    for _ in range(int(l) + 1):
        if not draw_point(int(round(x)), y, hh, lh, canvasWindow):
            return
        x += dx
        y += dy


def horizonForConstant(func, hh, lh, fr, to, step, z, canvasWindow):
    f = lambda x: func(x, z)  # f = f(x, z=const)
    prev = None
    for x in arange(fr, to + step, step):
        # x, z, f(x, z=const)
        current = transform([x, f(x), z])  # transformed: Повернуть, масштабировать и сдвинуть в центр экрана
        if prev:  # Если это не первая точка (то есть если есть предыдущая)
            draw_horizon_part(prev, current, hh, lh, canvasWindow)
        prev = current


def drawAllHorizons(equation, topHorizon, bottomHorizon, xStartLimit, xEndLimit, xStep, canvasWindow, zStartLimit, zEndLimit, zStep):
    for currentZ in arange(zStartLimit, zEndLimit + zStep, zStep):
        horizonForConstant(equation, topHorizon, bottomHorizon, xStartLimit, xEndLimit, xStep, currentZ, canvasWindow)


def drawSideRibs(zStartLimit, zEndLimit, zStep, xStartLimit, xEndLimit, equation, canvasWindow):
    for currentZ in arange(zStartLimit, zEndLimit, zStep):
        p1 = transform([xStartLimit, equation(xStartLimit, currentZ), currentZ])
        p2 = transform([xStartLimit, equation(xStartLimit, currentZ + zStep), currentZ + zStep])
        canvasWindow.create_line(p1[0], p1[1], p2[0], p2[1], fill = curColorLines)
        p1 = transform([xEndLimit, equation(xEndLimit, currentZ), currentZ])
        p2 = transform([xEndLimit, equation(xEndLimit, currentZ + zStep), currentZ + zStep])
        canvasWindow.create_line(p1[0], p1[1], p2[0], p2[1], fill = curColorLines)


def floatingHorizonAlgorithm(equation, xStartLimit, zStartLimit, xEndLimit, zEndLimit, xStep, zStep, canvasWindow):
    clearImage(canvasWindow)
    topHorizon = [0 for _ in range(width)]
    bottomHorizon = [height for _ in range(width)]

    drawAllHorizons(equation, topHorizon, bottomHorizon, xStartLimit, xEndLimit, xStep, canvasWindow, zStartLimit, zEndLimit, zStep)

    drawSideRibs(zStartLimit, zEndLimit, zStep, xStartLimit, xEndLimit, equation, canvasWindow)


def showSurface(exampleCombo,
                xStartLimitEntry, zStartLimitEntry,
                xEndLimitEntry, zEndLimitEntry,
                xStepEntry, zStepEntry, canvasWindow):
    xStartLimit = float(xStartLimitEntry.get())
    zStartLimit = float(zStartLimitEntry.get())
    xEndLimit = float(xEndLimitEntry.get())
    zEndLimit = float(zEndLimitEntry.get())

    xStep = float(xStepEntry.get())
    zStep = float(zStepEntry.get())

    global exa
    if exa == 0:
        floatingHorizonAlgorithm(example.expFirst, xStartLimit, zStartLimit, xEndLimit, zEndLimit, xStep, zStep, canvasWindow)


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


def setComboWhatToDraw(rootWindow):
    Label(rootWindow, text = "Уравнение поверхности:", bg = "black", fg = "white", borderwidth = 5, relief = RIDGE, font = fontSettingLower).place(x = 5, y = 112)
    global comboWhatToDraw
    comboWhatToDraw = Combobox(rootWindow,
                              width = 75,
                              textvariable = exa,
                              state = 'readonly',
                              values =
                                ('x² + y² = z²',
                                 '...'))

    comboWhatToDraw.place(x = 280, y = 120)
    comboWhatToDraw.current(0)


def setComboRotation(rootWindow):
    global comboRotation
    comboRotation = Listbox(rootWindow,
                              width = 43, height = 3,
                              selectmode = SINGLE, bg = 'black', fg = 'white')
    comboRotation.insert(END, 'Вокруг оси x')
    comboRotation.insert(END, 'Вокруг оси y')
    comboRotation.insert(END, 'Вокруг оси z')

    comboRotation.place(x = 5, y = 554)


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Лабораторная работа 10, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+1980+0")

    canvasWindow = Canvas(rootWindow, bg = curColorBackground, width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    canvasWindow.place(x = 750, y = 0)

    setComboWhatToDraw(rootWindow)

    Label(text = "Алгоритм Плавающего горизонта\nпостроения трёхмерных моделей", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    Label(text = "Пределы", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 160)

    Label(text = "Начало по x:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 5, y = 220)
    xLimitStartEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    xLimitStartEntry.place(x = 210, y = 220)
    Label(text = "Конец по x:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 430, y = 220)
    xLimitEndEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    xLimitEndEntry.place(x = 630, y = 220)

    Label(text = "Начало по z:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 5, y = 270)
    zLimitStartEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    zLimitStartEntry.place(x = 210, y = 270)
    Label(text = "Конец по z:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 430, y = 270)
    zLimitEndEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    zLimitEndEntry.place(x = 630, y = 270)

    Label(text = "Шаг", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 320)
    Label(text = "Шаг по x:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 5, y = 380)
    xStepEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    xStepEntry.place(x = 210, y = 380)
    Label(text = "Шаг по z:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 430, y = 380)
    zStepEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    zStepEntry.place(x = 630, y = 380)

    showButton = Button(rootWindow, text = "Отрисовать фигуру", command = lambda: showSurface(comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow), height = 2, width = 61, font = fontSettingLower, bg = "#FF9C00")
    showButton.place(x = 5, y = 430)

    Label(text = "Вращение", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 500)
    setComboRotation(rootWindow)

    Label(text = "Угол поворота (в градусах): ", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 28).place(x = 270, y = 555)

    makeCascadeMenu(rootWindow, canvasWindow)
    angleEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    angleEntry.place(x = 630, y = 555)
    rotateButton = Button(rootWindow, text = "Повернуть фигуру", command = lambda: rotate(comboRotation, comboWhatToDraw, xLimitStartEntry, zLimitStartEntry, xLimitEndEntry, zLimitEndEntry, xStepEntry, zStepEntry, canvasWindow, angleEntry), height = 2, width = 61, font = fontSettingLower, bg = "#FF9C00")
    rotateButton.place(x = 5, y = 605)

    Label(text = "Список уравнений поверхностей\n задаётся в отдельном модуле.", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48, heigh = 10).place(x = 5, y = 675)
    setComboRotation(rootWindow)

    rootWindow.mainloop()


makeMainWindow()

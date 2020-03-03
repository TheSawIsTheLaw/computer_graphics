from tkinter import *
from re import *
from math import atan

Pi = 3.141592

minX = 0
maxY = 0

'''
    Масштабирование точки X
'''
def masstX(x, xmin, k, xn = 30):
    return rd(xn + (x - xmin)*k) # Промасштабированный x

'''
    Массштабирование точки Y
'''
def masstY(y, ymax, k, yn = 30):
    return rd(yn + (ymax - y)*k) # Промасштабированный y

'''
    Проверенная функция математического округления, проверенная временем
    feat. Voznica
'''
def rd(x,y=0):
    m = int('1'+'0'*y) # multiplier - how many positions to the right
    q = x*m # shift to the right by multiplier
    c = int(q) # new number
    i = int((q-c)*10) # indicator number on the right
    if i >= 5:
        c += 1
    return c/m

'''
    Отладочная команда
'''
def printDebug(var):
    print(var)

'''
    Каскадное меню->"Справка"->"Формулировка задания"
'''
def makeJobWindow():
    jobWindow = Tk()

    jobWindow.minsize(400, 200)
    jobWindow.title("Формулировка задания")
    jobLabel = Label(jobWindow,
                     text="На плоскости даны два множества точек.\n"
                          "Найти пару треугольников (каждый треугольник\n"
                          "в качестве вершин имеет три различные точки\n"
                          "одного и того же множества; прямые, соединяющие точки пере-\n"
                          "сечения двух треугольников строятся на точках разных множеств)\n"
                          "таких, что прямая, соединяющая точки пересечения высот,\n"
                          "образует минимальный угол с осью абсцисс.",
                     font=('consolas', 20))
    jobLabel.pack()

    jobWindow.mainloop()

'''
    Создание начального окна Canvas
'''
def makeCanvasStart(canvasWindow):
    canvasWindow.delete("all")
    canvasWindow.grid(row=0, column=4, rowspan=16)

    # Начальные Оси
    canvasWindow.create_line(500, 1050, 500, 0, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_text(520, 10, text="Y")
    canvasWindow.create_line(0, 500, 1000, 500, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_text(1000, 480, text="X")

'''
    Генерация окна полного ответа
'''
def makeAnswerWindow(minAnglesArray, angle, crossFX, crossFY, crossSX, crossSY):
    answerWindow = Tk()
    answerWindow.title("Ответ")
    answerLabel = Label(answerWindow, text="Треугольники, фигурирующие в ответе:\nТреугольник №1:\nВершина №1: x = "
                        + str(minAnglesArray[0][0][0]) + "; y = " + str(minAnglesArray[0][0][1]) + ";\nВершина №2: x = "
                        + str(minAnglesArray[0][1][0]) + "; y = " + str(minAnglesArray[0][1][1]) + ";\nВершина №3: x = "
                        + str(minAnglesArray[0][2][0]) + "; y = " + str(minAnglesArray[0][2][1]) + ";\n\nТреугольник №2:\nВершина №1: x = "
                        + str(minAnglesArray[1][0][0]) + "; y = " + str(minAnglesArray[1][0][1]) + ";\nВершина №2: x = "
                        + str(minAnglesArray[1][1][0]) + "; y = " + str(minAnglesArray[1][1][1]) + ";\nВершина №3: x = "
                        + str(minAnglesArray[1][2][0]) + "; y = " + str(minAnglesArray[1][2][1]) + ";\n\n"
                        "Точки пересечения высот первого треугольника:\nx = " + str(round(crossFX, 2)) + "; y = " + str(round(crossFY, 2)) +
                        "\nТочки пересечения высот второго треугольника:\nx = " + str(round(crossSX, 2)) + "; y = " + str(round(crossSY, 2)) +
                        "\n\nУгол, между прямой, соединяющей данные тчоки пересечения с осью абсцисс образуют угол: " +
                        str(round(angle, 2)) + " градусов;\nЧто является наименьшим возможным значением угла\nв заданных условиях.",
                        font=("consolas", 14))
    answerLabel.pack()
    answerWindow.mainloop()

'''
    Функция обновления окна Canvas по текущим состояниям массивов точек
'''
def reRenderCanvas(canvasWindow, pointArrayF, pointArrayS):
    canvasWindow.delete("all")
    global maxY, minX

    if len(pointArrayF) + len(pointArrayS) == 0:
        makeCanvasStart(canvasWindow)
        return
    try:
        maxX = pointArrayS[0][0]
        minX = pointArrayS[0][0]
    except IndexError:
        maxX = pointArrayF[0][0]
        minX = pointArrayF[0][0]

    try:
        maxY = pointArrayS[0][1]
        minY = pointArrayS[0][1]
    except IndexError:
        maxY = pointArrayF[0][1]
        minY = pointArrayF[0][1]

    for i in pointArrayS:
        if i[0] > maxX:
            maxX = i[0]
        if i[0] < minX:
            minX = i[0]
        if i[1] > maxY:
            maxY = i[1]
        if i[1] < minY:
            minY = i[1]
    for i in pointArrayF:
        if i[0] > maxX:
            maxX = i[0]
        if i[0] < minX:
            minX = i[0]
        if i[1] > maxY:
            maxY = i[1]
        if i[1] < minY:
            minY = i[1]

    global k
    try:
        kx = 1000 / (maxX - minX)
    except ZeroDivisionError:
        kx = float("inf")
    try:
        ky = 1000 / (maxY - minY)
    except ZeroDivisionError:
        ky = float("inf")
    k = min(kx, ky)
    if len(pointArrayF) + len(pointArrayS) == 1:
        k = 1
        minX = minX - 450
        maxY = maxY + 450
    canvasWindow.create_line(masstX(0, minX, k), 1040, masstX(0, minX, k), 0, width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_text(masstX(0, minX, k) + 20, 10, text="Y")
    canvasWindow.create_line(0, masstY(0, maxY, k), 1040, masstY(0, maxY, k), width=3, arrow=LAST, arrowshape="10 20 10")
    canvasWindow.create_text(1040, masstY(0, maxY, k) - 20, text="X")
    #print(minX, maxY)
    for i in pointArrayF:
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill="Blue")
        if y - 10 > 0:
            canvasWindow.create_text(x + 17, y - 10, text=str(round(i[0], 1))+"\n"+str(round(i[1], 1)))
        else:
            canvasWindow.create_text(x + 17, y + 10, text=str(round(i[0], 1)) + "\n" + str(round(i[1], 1)))

    for i in pointArrayS:
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill="Red")
        if y + 10 < 1000:
            canvasWindow.create_text(x + 17, y + 10, text=str(round(i[0], 1))+"\n"+str(round(i[1], 1)))
        else:
            canvasWindow.create_text(x + 17, y - 10, text=str(round(i[0], 1)) + "\n" + str(round(i[1], 1)))


''' 
    Ошибка ввода точки
'''
def generateInputErrorWindow():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow, text="Должно быть введено два вещественных значения в следующем формате"
                                         ":\n'x y'\nПовторите попытку, пожалуйста.", font=("consolas", 15))
    errorLabel.pack()

'''
    Ошибка повтора точки
'''
def generateInputRepeatErrorWindow():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Значения уже имеются в таблице.",
                       font=("consolas", 15))
    errorLabel.pack()

'''
    Функция добавления точки в ListBox и массив точек с непосредственным обновлением окна Canvas
'''
def addPoint(pointArray, entry, listBox, dotIndex, canvasWindow, secPointArray):
    inputString = entry.get()
    inputString = findall(r"[-+]?\d*\.?\d+|[-+]?\d*\.?\d+", inputString)
    for i in range(len(inputString)):
        inputString[i] = float(inputString[i])
    #print(inputString)
    if len(inputString) != 2:
        generateInputErrorWindow()
        return 3
    if inputString not in pointArray:
        listBox.insert(dotIndex, "X = " + str(inputString[0]) + "; Y = " + str(inputString[1]))
        pointArray.insert(dotIndex, inputString)
    else:
        generateInputRepeatErrorWindow()
        return 3

    reRenderCanvas(canvasWindow, pointArray, secPointArray)
    print(pointArray)
    return 0

'''
    Ошибка кнопок работы с таблицей (удаление, изменение точки) - не выбрано ни одно значения в таблице
'''
def generateEmptyError():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Не выбрано ни одного значения в таблице!",
                       font=("consolas", 15))
    errorLabel.pack()

'''
    Функция кнопки "Удалить выбранную вершину"
'''
def deletePoint(pointArray, listBox, canvasWindow, secPointArray):
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]

    listBox.delete(delNum)
    pointArray.pop(delNum)
    print(pointArray)
    reRenderCanvas(canvasWindow, pointArray, secPointArray)

'''
    Функция кнопки "Изменить выбранную вершину"
'''
def changePoint(pointArray, entry, listBox, canvasWindow, secPointArray):
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]
    if addPoint(pointArray, entry, listBox, delNum + 1, canvasWindow, secPointArray) != 3:
        deletePoint(pointArray, listBox, canvasWindow, secPointArray)
    print(pointArray)

'''
    Функция определения, образуют ли три переданные точки треугольник
'''
def isAngle(x1, x2, x3, y1, y2, y3):
    if (y2 - y1)*(x3 - x1) != (y3 - y1)*(x2 - x1):
        return 1
    return 0

'''
    Окно ошибки: отсутствуют точки, образующие треугольник.
'''
def generateNoAnglesError():
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text="Заданные параметры не удовлетворяют условию задачи!",
                       font=("consolas", 15))
    errorLabel.pack()

'''
    Функция, выполняющая задачу, поставленную во главу лабораторной работы
'''
def executionPromotion(dotsArrayF, dotsArrayS, canvasWindow):
    if len(dotsArrayS) < 3 and len(dotsArrayF) < 3:
        generateNoAnglesError()
        return

    global k, minX, maxY

    trianglesF = []
    trianglesS = []

    for i in range(len(dotsArrayF) - 2):
        for j in range(i + 1, len(dotsArrayF) - 1):
            for z in range(i + 2, len(dotsArrayF)):
                if isAngle(dotsArrayF[i][0], dotsArrayF[j][0], dotsArrayF[z][0], dotsArrayF[i][1], dotsArrayF[j][1],
                           dotsArrayF[z][1]):
                    trianglesF.append([dotsArrayF[i], dotsArrayF[j], dotsArrayF[z]])
                    #canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                    #                         masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k), fill="Red")
                    #canvasWindow.create_line(masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k),
                    #                         masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")
                    #canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                    #                         masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")

    for i in range(len(dotsArrayS) - 2):
        for j in range(i + 1, len(dotsArrayS) - 1):
            for z in range(i + 2, len(dotsArrayS)):
                if isAngle(dotsArrayS[i][0], dotsArrayS[j][0], dotsArrayS[z][0], dotsArrayS[i][1], dotsArrayS[j][1],
                           dotsArrayS[z][1]):
                    trianglesS.append([dotsArrayS[i], dotsArrayS[j], dotsArrayS[z]])
                    #canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                    #                         masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k), fill="Blue")
                    #canvasWindow.create_line(masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k),
                    #                         masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")
                    #canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                    #                         masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")

    if not len(trianglesF) or not len(trianglesS):
        generateNoAnglesError()

    print("Найденные треугольники:")
    print(trianglesF)
    print(trianglesS)

    minAngle = 90
    minTriangles = [[], []]
    for i in trianglesF:
        print("Текущий рассматриваемый треугольник первого множества:")
        print(i)
        A1 = -(i[1][0] - i[0][0])
        A2 = -(i[2][0] - i[1][0])
        B1 = i[0][1] - i[1][1]
        B2 = i[1][1] - i[2][1]
        C1 = (-1) * A1 * i[2][0] - B1 * i[2][1]
        C2 = (-1) * A2 * i[0][0] - B2 * i[0][1]
        crossPointXF = (B1 * C2 - B2 * C1)/(A1 * B2 - A2 * B1)
        crossPointYF = (C1 * A2 - C2 * A1)/(A1 * B2 - A2 * B1)

        for j in trianglesS:
            A11 = -(j[1][0] - j[0][0])
            A22 = -(j[2][0] - j[1][0])
            B11 = j[0][1] - j[1][1]
            B22 = j[1][1] - j[2][1]
            C11 = (-1) * A11 * j[2][0] - B11 * j[2][1]
            C22 = (-1) * A22 * j[0][0] - B22 * j[0][1]
            crossPointXS = (B11 * C22 - B22 * C11) / (A11 * B22 - A22 * B11)
            crossPointYS = (C11 * A22 - C22 * A11) / (A11 * B22 - A22 * B11)

            crossingA = crossPointYF - crossPointYS
            crossingB = crossPointXS - crossPointXF
            try:
                angle = abs(atan(crossingA/crossingB) * 180 / Pi)
            except ZeroDivisionError:
                pass
            else:
                if angle > 90:
                    angle = 180 - 90
                if angle <= minAngle:
                    minAngle = angle
                    minTriangles[0] = i
                    minTriangles[1] = j

    print("Два треугольника, прямая, соединяющая точку пересечения высот которых, минимальна:")
    print(minTriangles)

    A1 = -(minTriangles[0][0][0] - minTriangles[0][1][0])
    A2 = -(minTriangles[0][2][0] - minTriangles[0][1][0])
    B1 = minTriangles[0][1][1] - minTriangles[0][0][1]
    B2 = minTriangles[0][1][1] - minTriangles[0][2][1]
    C1 = (-1) * A1 * minTriangles[0][2][0] - B1 * minTriangles[0][2][1]
    C2 = (-1) * A2 * minTriangles[0][0][0] - B2 * minTriangles[0][0][1]
    crossPointXF = (B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1)
    crossPointYF = (C1 * A2 - C2 * A1) / (A1 * B2 - A2 * B1)
    XF = crossPointXF
    YF = crossPointYF
    dotsArrayF.append([crossPointXF, crossPointYF])
    A11 = -(minTriangles[1][0][0] - minTriangles[1][1][0])
    A22 = -(minTriangles[1][2][0] - minTriangles[1][1][0])
    B11 = minTriangles[1][1][1] - minTriangles[1][0][1]
    B22 = minTriangles[1][1][1] - minTriangles[1][2][1]
    C11 = (-1) * A11 * minTriangles[1][2][0] - B11 * minTriangles[1][2][1]
    C22 = (-1) * A22 * minTriangles[1][0][0] - B22 * minTriangles[1][0][1]
    crossPointXS = (B11 * C22 - B22 * C11) / (A11 * B22 - A22 * B11)
    crossPointYS = (C11 * A22 - C22 * A11) / (A11 * B22 - A22 * B11)
    dotsArrayS.append([crossPointXS, crossPointYS])
    XS = crossPointXS
    YS = crossPointYS
    reRenderCanvas(canvasWindow, dotsArrayF, dotsArrayS)

    canvasWindow.create_line(masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k),
                             fill="Green", width=6)
    canvasWindow.create_line(masstX(crossPointXF, minX, k) - 80, masstY(crossPointYF, maxY, k),
                             masstX(crossPointXF, minX, k) + 80, masstY(crossPointYF, maxY, k),
                             fill="Black", width=6)
    canvasWindow.create_line(masstX(crossPointXS, minX, k) - 80, masstY(crossPointYS, maxY, k),
                             masstX(crossPointXS, minX, k) + 80, masstY(crossPointYS, maxY, k),
                             fill="Black", width=6)

    canvasWindow.create_line(masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k),
                             fill="Red", width=3)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill="Red", width=2)

    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                            masstX(minTriangles[0][1][0], minX, k), masstY(minTriangles[0][1][1], maxY, k), fill="Blue",
                             width=3)
    canvasWindow.create_line(masstX(minTriangles[0][1][0], minX, k), masstY(minTriangles[0][1][1], maxY, k),
                             masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             fill="Blue", width=3)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             fill="Blue", width=3)

    canvasWindow.create_line(masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k),
                             fill="Red", width=2)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill="Red", width=2)

    A3 = minTriangles[0][0][1] - minTriangles[0][1][1]
    B3 = minTriangles[0][1][0] - minTriangles[0][0][0]
    C3 = (-1) * B3 * minTriangles[0][1][1] + (-1) * A3 * minTriangles[0][1][0]
    crossPointXF = (B1 * C3 - B3 * C1) / (A1 * B3 - A3 * B1)
    crossPointYF = (C1 * A3 - C3 * A1) / (A1 * B3 - A3 * B1)
    canvasWindow.create_line(masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill="Red", width=2)
    A3 = minTriangles[0][1][1] - minTriangles[0][2][1]
    B3 = minTriangles[0][2][0] - minTriangles[0][1][0]
    C3 = (-1) * B3 * minTriangles[0][2][1] + (-1) * A3 * minTriangles[0][2][0]
    crossPointXF = (B2 * C3 - B3 * C2) / (A2 * B3 - A3 * B2)
    crossPointYF = (C2 * A3 - C3 * A2) / (A2 * B3 - A3 * B2)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill="Red", width=2)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(minTriangles[1][1][0], minX, k), masstY(minTriangles[1][1][1], maxY, k),
                             fill="Blue",
                             width=3)
    canvasWindow.create_line(masstX(minTriangles[1][1][0], minX, k), masstY(minTriangles[1][1][1], maxY, k),
                             masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             fill="Blue", width=3)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             fill="Blue", width=3)

    A3 = minTriangles[1][0][1] - minTriangles[1][1][1]
    B3 = minTriangles[1][1][0] - minTriangles[1][0][0]
    C3 = (-1) * B3 * minTriangles[1][1][1] + (-1) * A3 * minTriangles[1][1][0]
    crossPointXS = (B11 * C3 - B3 * C11) / (A11 * B3 - A3 * B11)
    crossPointYS = (C11 * A3 - C3 * A11) / (A11 * B3 - A3 * B11)
    canvasWindow.create_line(masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill="Red", width=2)
    A3 = minTriangles[1][1][1] - minTriangles[1][2][1]
    B3 = minTriangles[1][2][0] - minTriangles[1][1][0]
    C3 = (-1) * B3 * minTriangles[1][2][1] + (-1) * A3 * minTriangles[1][2][0]
    crossPointXS = (B22 * C3 - B3 * C22) / (A22 * B3 - A3 * B22)
    crossPointYS = (C22 * A3 - C3 * A22) / (A22 * B3 - A3 * B22)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill="Red", width=2)

    makeAnswerWindow(minTriangles, minAngle, XF, YF, XS, YS)

    dotsArrayS.pop()
    dotsArrayF.pop()

'''
    Функция удаления всех заданных данных и очистки поял вывода
'''
def makeClearAll(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox):
    fDots.clear()
    sDots.clear()
    fListBox.delete(0, END)
    sListBox.delete(0, END)
    makeCanvasStart(canvasWindow)

'''
    Каскадное меню->"Справка"->"Справка"
'''
def makeReference():
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text=
    "Показания к работе с ПО"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Для добавления точки в одно из множеств требуется ввести координаты точки\n"
    " (значения типа float в формате 'x y') в поле 'Координаты точки' и нажать кнопку 'Добавить'"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Для удаления определённой точки из множества - выберите требуемую точку в списке (справа от поля 'Добавить')\n и "
    "нажмите кнопку 'Удалить выбранную в списке точку'"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Чтобы изменить выбранную в списке точку, требуется в поле 'Координаты точки' ввести точку, на которую\n"
    "Вы желаете заменить выбранную, а после - нажать на кнопку 'Заменить выбранную в списке точку'"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Для того, чтобы выполнить задание (см. вкладку 'Справка'-'Формулировка задания'), следует нажать на кнопку\n"
    "'Исполнить предначертанное!'"
    "\n\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ \n"
    "\n\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ \n"
    "Обозначения на графической плоскости"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Точки разных множест на плоскости изображены разными цветами\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "СИНИМИ отрезками изображены треугольники, которые фигурируют в ответе\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "КРАСНЫМИ отрезками изображены по две высоты в данных треугольниках. Точка пересечения высот так же отображена\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "ЗЕЛЁНЫЙ отрезок - прямая, соединяющая точки пересечения высот треугольников. ЧЁРНЫЕ прямые, параллельные оси\nабсцисс, показывают образуемый с осью угол\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Лабораторная работа 1, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font=("consolas", 16))
    referenceLabel.pack()
    referenceWindow.mainloop()

'''
    Функция создания каскадного меню
'''
def makeCascadeMenu(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox):
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu=rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label='Формулировка задания', command=makeJobWindow)
    jobMenu.add_command(label='Справка', command=makeReference)

    moreMenu = Menu(rootMenu)
    moreMenu.add_command(label='Очистить всё', command=lambda: makeClearAll(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox))


    rootMenu.add_cascade(label='Справка', menu=jobMenu)
    rootMenu.add_cascade(label='Дополнительные возможности', menu=moreMenu)

'''
    Функция Создания главного окна
'''
def makeMainWindow():
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1000)

    firstDotsArray = []
    secondDotsArray = []

    labLabel = Label(text="Лабораторная работа #1\nЯкуба Дмитрий\nИУ7-43Б", font=("consolas", 20))
    labLabel.grid(row=0, column=0, rowspan=2, columnspan=3)

    listLableFirst = Label(rootWindow, text="Множество 1:", font=("consolas", 20), fg="white",
                           bg="black").grid(row=3,
                                            column=0,
                                            columnspan=2)

    listBoxFirst = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxFirst.grid(row=4, column=2, columnspan=2, rowspan=5)
    entryFirstLable = Label(rootWindow, text="Координаты вершины \n(x, y через пробел):", font=("consolas", 14))
    entryFirstLable.grid(row=5, column=0)
    entryFirst = Entry(rootWindow)
    entryFirst.grid(row=5, column=1)
    insertButtonFirst = Button(rootWindow, text="Добавить", width=30, command=lambda: addPoint(firstDotsArray,
                                                                                               entryFirst,
                                                                                               listBoxFirst,
                                                                                               listBoxFirst.size() + 1,
                                                                                               canvasWindow, secondDotsArray))
    insertButtonFirst.grid(row=6, column=0, columnspan=2)
    delButtonFirst = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 1)",
                            command=lambda: deletePoint(firstDotsArray, listBoxFirst, canvasWindow, secondDotsArray))
    delButtonFirst.grid(row=7, column=0, columnspan=2)
    changeButtonFirst = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 1)",
                               command=lambda: changePoint(firstDotsArray, entryFirst, listBoxFirst, canvasWindow,
                                                           secondDotsArray))
    changeButtonFirst.grid(row=8, column=0, columnspan=2)

    emptyLabel1 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                         "----------------------------------------------")
    emptyLabel2 = Label(rootWindow, text="---------------------------------------------------------------------------"
                                         "----------------------------------------------")
    emptyLabel1.grid(row=9, columnspan=3)
    emptyLabel2.grid(row=2, columnspan=3)
    listLableSecond = Label(rootWindow, text="Множество 2:", font=("consolas", 20), fg="white",
                            bg="black").grid(row=10,
                                             column=0,
                                             columnspan=2)
    listBoxSecond = Listbox(rootWindow, height=15, width=30, selectmode=SINGLE)
    listBoxSecond.grid(row=11, column=2, columnspan=2, rowspan=5)
    entrySecondLable = Label(rootWindow, text="Координаты вершины \n(x, y через пробел):", font=("consolas", 14))
    entrySecondLable.grid(row=12, column=0)
    entrySecond = Entry(rootWindow)
    entrySecond.grid(row=12, column=1)
    insertButtonSecond = Button(rootWindow, text="Добавить", width=30, command=lambda: addPoint(secondDotsArray,
                                                                                                entrySecond,
                                                                                                listBoxSecond,
                                                                                                listBoxSecond.size() + 1,
                                                                                                canvasWindow, firstDotsArray))
    insertButtonSecond.grid(row=13, column=0, columnspan=2)
    delButtonSecond = Button(rootWindow, text="Удалить выбранную в списке точку (из множества 2)",
                             command=lambda: deletePoint(secondDotsArray, listBoxSecond, canvasWindow, firstDotsArray))
    delButtonSecond.grid(row=14, column=0, columnspan=2)
    changeButtonSecond = Button(rootWindow, text="Изменить выбранную в списке точку (из множества 2)",
                                command=lambda: changePoint(secondDotsArray, entrySecond, listBoxSecond, canvasWindow,
                                                            firstDotsArray))
    changeButtonSecond.grid(row=15, column=0, columnspan=2)

    startButton = Button(rootWindow, text="Исполнить \nпредначертанное!", font=("consolas", 15), bg="yellow", fg="blue",
                         command=lambda: executionPromotion(firstDotsArray, secondDotsArray, canvasWindow))
    startButton.grid(row=0, column=5, rowspan=1)

    canvasWindow = Canvas(rootWindow, bg="white", width=1060, height=1040)
    makeCanvasStart(canvasWindow)
    makeCascadeMenu(rootWindow, canvasWindow, firstDotsArray, secondDotsArray, listBoxFirst, listBoxSecond)

    rootWindow.mainloop()

makeMainWindow()



from tkinter import *
from re import *
from math import atan

Pi = 3.141592

minX = 0
maxY = 0


def masstX(x, xmin, k, xn = 30):
    """
       Масштабирование точки X

       k - коэффициент масштабирования
       xn - абсцисса начальной точки вывода
       xmin - минимальное значение x в МСК
       def rd - функция округления
    """
    return rd(xn + (x - xmin) * k)  # Промасштабированный x


def masstY(y, ymax, k, yn = 30):
    """
       Масштабирование точки Y

       k - коэффициент масштабирования
       yn - абсцисса начальной точки вывода
       ymax - максимальное значение y в МСК
       def rd - функция округления
    """
    return rd(yn + (ymax - y) * k)  # Промасштабированный y


def rd(x, y = 0):
    """
       Проверенная функция математического округления, проверенная временем

        feat. Voznica
    """
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m


def printDebug(var):
    """
       Отладочная команда
    """
    print(var)


def makeJobWindow():
    """
       Каскадное меню->"Справка"->"Формулировка задания"
    """
    jobWindow = Tk()

    jobWindow.minsize(400, 200)
    jobWindow.title("Формулировка задания")
    jobLabel = Label(jobWindow,
                     text = "На плоскости даны два множества точек.\n"
                            "Найти пару треугольников (каждый треугольник\n"
                            "в качестве вершин имеет три различные точки\n"
                            "одного и того же множества; прямые, соединяющие точки пере-\n"
                            "сечения двух треугольников строятся на точках разных множеств)\n"
                            "таких, что прямая, соединяющая точки пересечения высот,\n"
                            "образует минимальный угол с осью абсцисс.",
                     font = ('consolas', 20))
    jobLabel.pack()

    jobWindow.mainloop()


def makeCanvasStart(canvasWindow):
    """
       Создание начального окна Canvas
    """
    canvasWindow.delete("all")
    canvasWindow.grid(row = 0, column = 4, rowspan = 16)

    # Начальные Оси
    canvasWindow.create_line(500, 1050, 500, 0, width = 3, arrow = LAST, arrowshape = "10 20 10")
    canvasWindow.create_text(520, 10, text = "Y")
    canvasWindow.create_line(0, 500, 1000, 500, width = 3, arrow = LAST, arrowshape = "10 20 10")
    canvasWindow.create_text(1000, 480, text = "X")


def makeAnswerWindow(minAnglesArray, angle, crossFX, crossFY, crossSX, crossSY):
    """
       Генерация окна полного ответа
    """
    answerWindow = Tk()
    answerWindow.title("Ответ")
    answerLabel = Label(answerWindow, text = "Треугольники, фигурирующие в ответе:\nТреугольник №1:\nВершина №1: x = "
                                             + "{:g}".format(minAnglesArray[0][0][0]) + "; y = " + "{:g}".format(
        minAnglesArray[0][0][1]) + ";\nВершина №2: x = "
                                             + "{:g}".format(minAnglesArray[0][1][0]) + "; y = " + "{:g}".format(
        minAnglesArray[0][1][1]) + ";\nВершина №3: x = "
                                             + "{:g}".format(minAnglesArray[0][2][0]) + "; y = " + "{:g}".format(minAnglesArray[0][2][1]) + ";\n\nТреугольник "
                                                                                                                                            "№2:\nВершина №1: "
                                                                                                                                            "x = "
                                             + "{:g}".format(minAnglesArray[1][0][0]) + "; y = " + "{:g}".format(
        minAnglesArray[1][0][1]) + ";\nВершина №2: x = "
                                             + "{:g}".format(minAnglesArray[1][1][0]) + "; y = " + "{:g}".format(
        minAnglesArray[1][1][1]) + ";\nВершина №3: x = "
                                             + "{:g}".format(minAnglesArray[1][2][0]) + "; y = " + "{:g}".format(minAnglesArray[1][2][1]) + ";\n\n"
                                                                                                                                            "Точка пересечения высот первого "
                                                                                                                                            "треугольника:\nx = " + "{:g}".format(
        crossFX) + "; y = " + "{:g}".format(crossFY) +
                                             "\nТочка пересечения высот второго треугольника:\nx = " + "{:g}".format(crossSX) + "; y = " + "{:g}".format(
        crossSY) +
                                             "\n\nУгол между прямой, соединяющей данные точки пересечения,\nи осью абсцисс равен: " +
                                             "{:g}".format(angle) + "°;\nЧто является наименьшим возможным значением угла\nв заданных условиях.",
                        font = ("consolas", 14))
    answerLabel.pack()
    answerWindow.mainloop()


def reRenderCanvas(canvasWindow, pointArrayF, pointArrayS):
    """
       Функция обновления окна Canvas по текущим состояниям массивов точек
    """
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

# Находим максимальные и минимальные значения по осям x и y
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

# Глобальная переменная коэффициента масштабирования
    global k
    try:
        kx = 1000 / (maxX - minX)
    except ZeroDivisionError:
        kx = float("inf")
    try:
        ky = 1000 / (maxY - minY)
    except ZeroDivisionError:
        ky = float("inf")
# Берём минимальное, чтобы не наблюдать овалы вместо окружностей
    k = min(kx, ky)
# Параметры для вывода самой первой введённой точки
    if len(pointArrayF) + len(pointArrayS) == 1:
        k = 1
        minX = minX - 450
        maxY = maxY + 450
    canvasWindow.create_line(masstX(0, minX, k), 1040, masstX(0, minX, k), 0, width = 3, arrow = LAST, arrowshape = "10 20 10")
    canvasWindow.create_text(masstX(0, minX, k) + 20, 10, text = "Y")
    canvasWindow.create_line(0, masstY(0, maxY, k), 1040, masstY(0, maxY, k), width = 3, arrow = LAST, arrowshape = "10 20 10")
    canvasWindow.create_text(1040, masstY(0, maxY, k) - 20, text = "X")
    # print(minX, maxY)
    for i in pointArrayF:
        # Получаем промасштабированные координаты
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill = "Blue")
        if y - 10 > 0:
            canvasWindow.create_text(x + 20, y - 15, text = "{:+g}\n{:+g}".format(rd(i[0], 1), rd(i[1], 1)))
        else:
            canvasWindow.create_text(x + 20, y + 15, text = "{:+g}\n{:+g}".format(rd(i[0], 1), rd(i[1], 1)))

    for i in pointArrayS:
        # Получаем промасштабированные координаты
        x = masstX(i[0], minX, k)
        y = masstY(i[1], maxY, k)
        canvasWindow.create_oval(x - 3, y - 3, x + 3, y + 3, fill = "Red")
        if y + 10 < 1000:
            canvasWindow.create_text(x + 20, y + 15, text = "{:+g}\n{:+g}".format(rd(i[0], 1), rd(i[1], 1)))
        else:
            canvasWindow.create_text(x + 20, y - 15, text = "{:+g}\n{:+g}".format(rd(i[0], 1), rd(i[1], 1)))


def generateInputErrorWindow():
    """
       Ошибка ввода точки
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow, text = "Должно быть введено два вещественных значения в следующем формате"
                                           ":\n'x y'\nПовторите попытку, пожалуйста.", font = ("consolas", 15))
    errorLabel.pack()


def generateInputRepeatErrorWindow():
    """
       Ошибка повтора точки
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text = "Значения уже имеются в таблице.",
                       font = ("consolas", 15))
    errorLabel.pack()


def addPoint(pointArray, entry, listBox, dotIndex, canvasWindow, secPointArray, type):
    """
       Функция добавления точки в ListBox и массив точек с непосредственным обновлением окна Canvas
    """
    inputString = entry.get()
    inputString = findall(r'[-+]?\d*\.?\d+|[-+]?\d*\.?\d+', inputString)
    for i in range(len(inputString)):
        inputString[i] = float(inputString[i])
    # print(inputString)
    if len(inputString) != 2:
        generateInputErrorWindow()
        return 3
    if inputString not in pointArray:
        listBox.insert(dotIndex, "X = " + str(inputString[0]) + "; Y = " + str(inputString[1]))
        pointArray.insert(dotIndex, inputString)
    else:
        generateInputRepeatErrorWindow()
        return 3

    if type:
        reRenderCanvas(canvasWindow, pointArray, secPointArray)
    else:
        reRenderCanvas(canvasWindow, secPointArray, pointArray)
    print(pointArray)
    return 0


def generateEmptyError():
    """
       Ошибка кнопок работы с таблицей (удаление, изменение точки) - не выбрано ни одно значения в таблице
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text = "Не выбрано ни одного значения в таблице!",
                       font = ("consolas", 15))
    errorLabel.pack()


def deletePoint(pointArray, listBox, canvasWindow, secPointArray, type):
    """
       Функция кнопки "Удалить выбранную вершину"
    """
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]

    listBox.delete(delNum)
    pointArray.pop(delNum)
    print(pointArray)
    if type:
        reRenderCanvas(canvasWindow, pointArray, secPointArray)
    else:
        reRenderCanvas(canvasWindow, secPointArray, pointArray)


def changePoint(pointArray, entry, listBox, canvasWindow, secPointArray, type):
    """
       Функция кнопки "Изменить выбранную вершину"
    """
    if not listBox.curselection():
        generateEmptyError()
        return

    delNum = tuple(listBox.curselection())[0]
    if addPoint(pointArray, entry, listBox, delNum + 1, canvasWindow, secPointArray, type) != 3:
        deletePoint(pointArray, listBox, canvasWindow, secPointArray, type)
    print(pointArray)


def isAngle(x1, x2, x3, y1, y2, y3):
    """
       Функция определения, образуют ли три переданные точки треугольник

       Используется приравнивание формулы площади треугольника к нулю
    """
    if (y2 - y1) * (x3 - x1) != (y3 - y1) * (x2 - x1):
        return 1
    return 0


def generateNoAnglesError(type):
    """
       Окно ошибки: отсутствуют точки, образующие треугольник.
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    if type == 1:
        errorLabel = Label(errorWindow,
                           text = "По заданным параметрам точек в первом множестве нельзя построить ни одного треугольника: он(-и) вырождается(-ются) в "
                                  "отрезок!",
                           font = ("consolas", 15))
    elif type == 2:
        errorLabel = Label(errorWindow,
                           text = "По заданным параметрам точек во втором множестве нельзя построить ни одного треугольника: он(-и) вырождается(-ются) в "
                                  "отрезок!",
                           font = ("consolas", 15))
    else:
        errorLabel = Label(errorWindow,
                           text = "По заданным параметрам точек нельзя построить ни одного треугольника в каждом множестве: они вырождаются в отрезок!",
                           font = ("consolas", 15))
    errorLabel.pack()


def generateNotEnoughDotsError(type):
    """
       Окно ошибки: недостаточно точек
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    if type == 1:
        errorLabel = Label(errorWindow,
                           text = "Задано недостаточное количество точек для построения треугольника в первом множестве!",
                           font = ("consolas", 15))
    elif type == 2:
        errorLabel = Label(errorWindow,
                           text = "Задано недостаточное количество точек для построения треугольника во втором множестве!",
                           font = ("consolas", 15))
    else:
        errorLabel = Label(errorWindow,
                           text = "Задано недостаточное количество точек для построения треугольника в двух задаваемых множествах!",
                           font = ("consolas", 15))
    errorLabel.pack()


def generateEqualTrianglesError():
    """
           Окно ошибки: единственная прямая вырождается в точку.
    """
    errorWindow = Tk()
    errorWindow.title("Ошибка!")
    errorLabel = Label(errorWindow,
                       text = "Заданы два треугольника точки пересечения которых совпадают. Решение получено быть не может, \n"
                              "так как соединяющий точки пересечения высот треугольников отрезок вырождается в точку.",
                       font = ("consolas", 15))
    errorLabel.pack()


def executionPromotion(dotsArrayF, dotsArrayS, canvasWindow):
    """
        Функция, выполняющая задачу, поставленную во главу лабораторной работы
    """
    if len(dotsArrayF) < 3 and len(dotsArrayS) < 3:
        # Не хватает точек в двух массивах
        generateNotEnoughDotsError(0)
        return
    elif len(dotsArrayS) < 3:
        # Не хватает точек во втором
        generateNotEnoughDotsError(2)
        return
    elif len(dotsArrayF) < 3:
        # Не хватает точек в во первом
        generateNotEnoughDotsError(1)
        return

    global k, minX, maxY

    trianglesF = []  # Все треугольники по точкам первого множества
    trianglesS = []  # Все треугольники по точкам первого множества

    '''
        Поиск всех треугольников
    '''
    for i in range(len(dotsArrayF) - 2):
        for j in range(i + 1, len(dotsArrayF) - 1):
            for z in range(i + 2, len(dotsArrayF)):
                if isAngle(dotsArrayF[i][0], dotsArrayF[j][0], dotsArrayF[z][0], dotsArrayF[i][1], dotsArrayF[j][1],
                           dotsArrayF[z][1]):
                    trianglesF.append([dotsArrayF[i], dotsArrayF[j], dotsArrayF[z]])
                    # canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                    #                         masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k), fill="Red")
                    # canvasWindow.create_line(masstX(dotsArrayF[j][0], minX, k), masstY(dotsArrayF[j][1], maxY, k),
                    #                         masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")
                    # canvasWindow.create_line(masstX(dotsArrayF[i][0], minX, k), masstY(dotsArrayF[i][1], maxY, k),
                    #                         masstX(dotsArrayF[z][0], minX, k), masstY(dotsArrayF[z][1], maxY, k), fill="Red")

    for i in range(len(dotsArrayS) - 2):
        for j in range(i + 1, len(dotsArrayS) - 1):
            for z in range(i + 2, len(dotsArrayS)):
                if isAngle(dotsArrayS[i][0], dotsArrayS[j][0], dotsArrayS[z][0], dotsArrayS[i][1], dotsArrayS[j][1],
                           dotsArrayS[z][1]):
                    trianglesS.append([dotsArrayS[i], dotsArrayS[j], dotsArrayS[z]])
                    # canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                    #                         masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k), fill="Blue")
                    # canvasWindow.create_line(masstX(dotsArrayS[j][0], minX, k), masstY(dotsArrayS[j][1], maxY, k),
                    #                         masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")
                    # canvasWindow.create_line(masstX(dotsArrayS[i][0], minX, k), masstY(dotsArrayS[i][1], maxY, k),
                    #                         masstX(dotsArrayS[z][0], minX, k), masstY(dotsArrayS[z][1], maxY, k), fill="Blue")

    # Треугольники не были найдены в одном или двух массивах
    if not len(trianglesF) and not len(trianglesS):
        generateNoAnglesError(0)
        return
    elif not len(trianglesF):
        generateNoAnglesError(1)
        return
    elif not len(trianglesS):
        generateNoAnglesError(2)
        return

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
        # Точки пересечения высот
        crossPointXF = (B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1)
        crossPointYF = (C1 * A2 - C2 * A1) / (A1 * B2 - A2 * B1)

        for j in trianglesS:
            A11 = -(j[1][0] - j[0][0])
            A22 = -(j[2][0] - j[1][0])
            B11 = j[0][1] - j[1][1]
            B22 = j[1][1] - j[2][1]
            C11 = (-1) * A11 * j[2][0] - B11 * j[2][1]
            C22 = (-1) * A22 * j[0][0] - B22 * j[0][1]
            # Точки пересечения высот
            crossPointXS = (B11 * C22 - B22 * C11) / (A11 * B22 - A22 * B11)
            crossPointYS = (C11 * A22 - C22 * A11) / (A11 * B22 - A22 * B11)

            # Определяем тангенс угла между прямой и осью абсцисс
            crossingA = crossPointYF - crossPointYS
            crossingB = crossPointXS - crossPointXF
            try:
                angle = abs(atan(crossingA / crossingB) * 180 / Pi)
            except ZeroDivisionError:
                # Первая мнимальная прямая имеет наклон в 90 градусов
                if minAngle == 90 and crossingA != crossingB:
                    minTriangles[0] = i
                    minTriangles[1] = j
            else:
                # Берётся случай рассмотрения только острого угла наклона
                if angle > 90:
                    angle = 180 - 90
                if angle <= minAngle:
                    minAngle = angle
                    minTriangles[0] = i
                    minTriangles[1] = j

    print("Два треугольника, прямая, соединяющая точку пересечения высот которых, минимальна:")
    print(minTriangles)

    if minTriangles == [[], []]:
        generateEqualTrianglesError()
        return

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

    # Соединения двух точек пересечения высот в треугольниках
    canvasWindow.create_line(masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k),
                             fill = "Green", width = 6)
    # Дублёры оси Х на концах этого отрезка
    canvasWindow.create_line(masstX(crossPointXF, minX, k) - 80, masstY(crossPointYF, maxY, k),
                             masstX(crossPointXF, minX, k) + 80, masstY(crossPointYF, maxY, k),
                             fill = "Black", width = 6)
    canvasWindow.create_line(masstX(crossPointXS, minX, k) - 80, masstY(crossPointYS, maxY, k),
                             masstX(crossPointXS, minX, k) + 80, masstY(crossPointYS, maxY, k),
                             fill = "Black", width = 6)

    # Высоты треугольника из второго множества
    canvasWindow.create_line(masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k),
                             fill = "#4284D3", width = 3)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill = "#4284D3", width = 2)

    # Треугольник первого множества
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(minTriangles[0][1][0], minX, k), masstY(minTriangles[0][1][1], maxY, k), fill = "Blue",
                             width = 3)
    canvasWindow.create_line(masstX(minTriangles[0][1][0], minX, k), masstY(minTriangles[0][1][1], maxY, k),
                             masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             fill = "Blue", width = 3)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             fill = "Blue", width = 3)

    # Высоты треугольника первого множества
    canvasWindow.create_line(masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k),
                             fill = "Purple", width = 2)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill = "Purple", width = 2)

    # Дочерчиваем высоты до сторон треугольника (даже продолжений сторон треугольника)
    A3 = minTriangles[0][0][1] - minTriangles[0][1][1]
    B3 = minTriangles[0][1][0] - minTriangles[0][0][0]
    C3 = (-1) * B3 * minTriangles[0][1][1] + (-1) * A3 * minTriangles[0][1][0]
    crossPointXF = (B1 * C3 - B3 * C1) / (A1 * B3 - A3 * B1)
    crossPointYF = (C1 * A3 - C3 * A1) / (A1 * B3 - A3 * B1)
    canvasWindow.create_line(masstX(minTriangles[0][2][0], minX, k), masstY(minTriangles[0][2][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill = "Purple", width = 2)
    A3 = minTriangles[0][1][1] - minTriangles[0][2][1]
    B3 = minTriangles[0][2][0] - minTriangles[0][1][0]
    C3 = (-1) * B3 * minTriangles[0][2][1] + (-1) * A3 * minTriangles[0][2][0]
    crossPointXF = (B2 * C3 - B3 * C2) / (A2 * B3 - A3 * B2)
    crossPointYF = (C2 * A3 - C3 * A2) / (A2 * B3 - A3 * B2)
    canvasWindow.create_line(masstX(minTriangles[0][0][0], minX, k), masstY(minTriangles[0][0][1], maxY, k),
                             masstX(crossPointXF, minX, k), masstY(crossPointYF, maxY, k), fill = "Purple", width = 2)

    # Треугольник второго множества
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(minTriangles[1][1][0], minX, k), masstY(minTriangles[1][1][1], maxY, k),
                             fill = "Red",
                             width = 3)
    canvasWindow.create_line(masstX(minTriangles[1][1][0], minX, k), masstY(minTriangles[1][1][1], maxY, k),
                             masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             fill = "Red", width = 3)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             fill = "Red", width = 3)

    # Дочерчиваем высоты треугольника из второго множества
    A3 = minTriangles[1][0][1] - minTriangles[1][1][1]
    B3 = minTriangles[1][1][0] - minTriangles[1][0][0]
    C3 = (-1) * B3 * minTriangles[1][1][1] + (-1) * A3 * minTriangles[1][1][0]
    crossPointXS = (B11 * C3 - B3 * C11) / (A11 * B3 - A3 * B11)
    crossPointYS = (C11 * A3 - C3 * A11) / (A11 * B3 - A3 * B11)
    canvasWindow.create_line(masstX(minTriangles[1][2][0], minX, k), masstY(minTriangles[1][2][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill = "#4284D3", width = 2)
    A3 = minTriangles[1][1][1] - minTriangles[1][2][1]
    B3 = minTriangles[1][2][0] - minTriangles[1][1][0]
    C3 = (-1) * B3 * minTriangles[1][2][1] + (-1) * A3 * minTriangles[1][2][0]
    crossPointXS = (B22 * C3 - B3 * C22) / (A22 * B3 - A3 * B22)
    crossPointYS = (C22 * A3 - C3 * A22) / (A22 * B3 - A3 * B22)
    canvasWindow.create_line(masstX(minTriangles[1][0][0], minX, k), masstY(minTriangles[1][0][1], maxY, k),
                             masstX(crossPointXS, minX, k), masstY(crossPointYS, maxY, k), fill = "#4284D3", width = 2)
    dotsArrayS.pop()
    dotsArrayF.pop()

    print(dotsArrayF)
    print(dotsArrayS)

    makeAnswerWindow(minTriangles, minAngle, XF, YF, XS, YS)


def makeClearAll(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox):
    """
        Функция удаления всех заданных данных и очистки поля вывода
    """
    fDots.clear()
    sDots.clear()
    fListBox.delete(0, END)
    sListBox.delete(0, END)
    makeCanvasStart(canvasWindow)


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
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
    "Точки разных множест на плоскости изображены разными цветами:\n"
    "СИНИМ цветом обозначаются точки первого множества\n"
    "КРАСНЫМ цветом обозначаются точки второго множества\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "СИНИМИ и КРАСНЫМИ отрезками показаны соотвественно треугольники из первого множества и из второго множества.\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "СЕРЕНЕВЫМИ И СВЕТЛО-СИНИМИ (цвета морской волны) отрезками соотвественно показаны высоты в\nтреугольнике множества 1 и множества 2\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "ЗЕЛЁНЫЙ отрезок - прямая, соединяющая точки пересечения высот треугольников. ЧЁРНЫЕ прямые, параллельные оси\nабсцисс, "
    "показывают образуемый с осью X угол (острый)\n"
    "\n---------------------------------------------------------------------------------------------------------------\n"
    "Лабораторная работа 1, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = ("consolas", 16))
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeCascadeMenu(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox):
    """
        Функция создания каскадного меню
    """
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu = rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label = 'Формулировка задания', command = makeJobWindow)
    jobMenu.add_command(label = 'Справка', command = makeReference)

    moreMenu = Menu(rootMenu)
    moreMenu.add_command(label = 'Очистить всё', command = lambda: makeClearAll(rootWindow, canvasWindow, fDots, sDots, fListBox, sListBox))

    rootMenu.add_cascade(label = 'Справка', menu = jobMenu)
    rootMenu.add_cascade(label = 'Дополнительные возможности', menu = moreMenu)


def makeMainWindow():
    """
        Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 1, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1000)

    firstDotsArray = []
    secondDotsArray = []

    labLabel = Label(text = "Лабораторная работа #1\nЯкуба Дмитрий\nИУ7-43Б", font = ("consolas", 20))
    labLabel.grid(row = 0, column = 0, rowspan = 2, columnspan = 3)

    listLableFirst = Label(rootWindow, text = "Множество 1:", font = ("consolas", 20), fg = "white",
                           bg = "black").grid(row = 3,
                                              column = 0,
                                              columnspan = 2)

    listBoxFirst = Listbox(rootWindow, height = 15, width = 30, selectmode = SINGLE)
    listBoxFirst.grid(row = 4, column = 2, columnspan = 2, rowspan = 5)
    entryFirstLable = Label(rootWindow, text = "Координаты вершины \n(x, y через пробел):", font = ("consolas", 14))
    entryFirstLable.grid(row = 5, column = 0)
    entryFirst = Entry(rootWindow)
    entryFirst.grid(row = 5, column = 1)
    insertButtonFirst = Button(rootWindow, text = "Добавить", width = 30, command = lambda: addPoint(firstDotsArray,
                                                                                                     entryFirst,
                                                                                                     listBoxFirst,
                                                                                                     listBoxFirst.size() + 1,
                                                                                                     canvasWindow, secondDotsArray, 1))
    insertButtonFirst.grid(row = 6, column = 0, columnspan = 2)
    delButtonFirst = Button(rootWindow, text = "Удалить выбранную в списке точку (из множества 1)",
                            command = lambda: deletePoint(firstDotsArray, listBoxFirst, canvasWindow, secondDotsArray, 1))
    delButtonFirst.grid(row = 7, column = 0, columnspan = 2)
    changeButtonFirst = Button(rootWindow, text = "Изменить выбранную в списке точку (из множества 1)",
                               command = lambda: changePoint(firstDotsArray, entryFirst, listBoxFirst, canvasWindow,
                                                             secondDotsArray, 1))
    changeButtonFirst.grid(row = 8, column = 0, columnspan = 2)

    emptyLabel1 = Label(rootWindow, text = "---------------------------------------------------------------------------"
                                           "----------------------------------------------")
    emptyLabel2 = Label(rootWindow, text = "---------------------------------------------------------------------------"
                                           "----------------------------------------------")
    emptyLabel1.grid(row = 9, columnspan = 3)
    emptyLabel2.grid(row = 2, columnspan = 3)
    listLableSecond = Label(rootWindow, text = "Множество 2:", font = ("consolas", 20), fg = "white",
                            bg = "black").grid(row = 10,
                                               column = 0,
                                               columnspan = 2)
    listBoxSecond = Listbox(rootWindow, height = 15, width = 30, selectmode = SINGLE)
    listBoxSecond.grid(row = 11, column = 2, columnspan = 2, rowspan = 5)
    entrySecondLable = Label(rootWindow, text = "Координаты вершины \n(x, y через пробел):", font = ("consolas", 14))
    entrySecondLable.grid(row = 12, column = 0)
    entrySecond = Entry(rootWindow)
    entrySecond.grid(row = 12, column = 1)
    insertButtonSecond = Button(rootWindow, text = "Добавить", width = 30, command = lambda: addPoint(secondDotsArray,
                                                                                                      entrySecond,
                                                                                                      listBoxSecond,
                                                                                                      listBoxSecond.size() + 1,
                                                                                                      canvasWindow, firstDotsArray, 0))
    insertButtonSecond.grid(row = 13, column = 0, columnspan = 2)
    delButtonSecond = Button(rootWindow, text = "Удалить выбранную в списке точку (из множества 2)",
                             command = lambda: deletePoint(secondDotsArray, listBoxSecond, canvasWindow, firstDotsArray, 0))
    delButtonSecond.grid(row = 14, column = 0, columnspan = 2)
    changeButtonSecond = Button(rootWindow, text = "Изменить выбранную в списке точку (из множества 2)",
                                command = lambda: changePoint(secondDotsArray, entrySecond, listBoxSecond, canvasWindow,
                                                              firstDotsArray, 0))
    changeButtonSecond.grid(row = 15, column = 0, columnspan = 2)

    startButton = Button(rootWindow, text = "Исполнить \nпредначертанное!", font = ("consolas", 15), bg = "yellow", fg = "blue",
                         command = lambda: executionPromotion(firstDotsArray, secondDotsArray, canvasWindow))
    startButton.grid(row = 0, column = 5, rowspan = 1)

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1060, height = 1040)
    makeCanvasStart(canvasWindow)
    makeCascadeMenu(rootWindow, canvasWindow, firstDotsArray, secondDotsArray, listBoxFirst, listBoxSecond)

    rootWindow.mainloop()


makeMainWindow()

from tkinter import *
from tkinter import colorchooser
from math import *
from tkinter import ttk

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

method = 0

curColorLines = "black"
curColorBackground = "white"


def makeReference():
    """
        Каскадное меню->"Справка"->"Справка"
    """
    referenceWindow = Tk()
    referenceWindow.title("Справка")
    referenceLabel = Label(referenceWindow, text =
    "Показания к работе с ПО"
    "\nПросто пользуетесь на здоровье...\n"
    "Лабораторная работа 3, Якуба Дмитрий, ИУ7-43Б, 2020 год.", font = fontSettingLabels)
    referenceLabel.pack()
    referenceWindow.mainloop()


def makeJobWindow():
    jobWindow = Tk()
    jobWindow.title("Формулировка задания")

    Label(jobWindow, font = fontSettingLabels,
          text = "Работа: реализация и исследование алгоритмов построения отрезков.\n\n"
                 "Реализовать и исследовать следующие алгоритмы построения отрезков:\n"
                 "Алгоритм цифрового дифференциального анализатора\n"
                 "Алгоритм Брезенхема с целыми коэффициентами\n"
                 "Алгоритм Брезенхема с действительными коэффициентами\n"
                 "Алгоритм Брезенхема построения отрезка с устранением ступенчаточти\n"
                 "Алгоритм Ву\n"
                 "Алгоритм Tkinter Canvas\n"
                 "Предоставить сравнение визуальных характеристик построенных отрезков \nи исследование временных характеристик").grid()

    jobWindow.mainloop()


def chooseBackgroundColor(canvasBackgroundColor, rootWindow, row, column):
    curColorBackground = colorchooser.askcolor()[1]
    canvasBackgroundColor = Canvas(rootWindow, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasBackgroundColor.grid(row = row, column = column, sticky = W)

def chooseLinesColor(canvasWindow, rootWindow, row, column):
    curColorLines = colorchooser.askcolor()[1]
    canvasLinesColor = Canvas(rootWindow, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasLinesColor.grid(row = row, column = column, sticky = W)

def makeCascadeMenu(rootWindow):
    """
        Функция создания каскадного меню
    """
    rootMenu = Menu(rootWindow)
    rootWindow.config(menu = rootMenu)

    jobMenu = Menu(rootMenu)
    jobMenu.add_command(label = 'Формулировка задания', command = makeJobWindow)
    jobMenu.add_command(label = 'Справка', command = makeReference)

    plusCommands = Menu(rootMenu)
    plusCommands.add_command(label = 'Очистить плоскость рисования', command = print())

    rootMenu.add_cascade(label = 'Справка', menu = jobMenu)
    rootMenu.add_cascade(label = "Доп. возможности", menu = plusCommands)


def makeMainWindow():
    """
        Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Рабораторная работа 3, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    # Выбор метода построения
    Label(rootWindow, text = "Алгоритм построения:", font = fontSettingLower).grid(row = 0, column = 0, columnspan = 1, sticky = E)
    listBox = ttk.Combobox(rootWindow, width = 70, textvariable = method, state = 'readonly', values =
    ('Алгоритм цифрового дифференциального анализатора',
     'Алгоритм Брезенхема с целыми коэффициентами',
     'Алгоритм Брезенхема с действительными коэффициентами',
     'Алгоритм Брезенхема построения отрезка с устранением ступенчаточти',
     'Алгоритм Ву',
     'Алгоритм Tkinter Canvas'))
    listBox.grid(row = 0, column = 1, columnspan = 4, sticky = W)
    listBox.current(0)

    Label(rootWindow, text = "Начальная точка отрезка", font = fontSettingLabels).grid(row = 1, columnspan = 6, sticky = W)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 2, column = 0, sticky = E)
    entryXFirst = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 2, column = 1, sticky = W)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 2, column = 2, sticky = E)
    entryYFirst = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 2, column = 3, sticky = W)

    Label(rootWindow, text = "Конечная точка отрезка", font = fontSettingLabels).grid(row = 3, columnspan = 6, sticky = W)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 4, column = 0, sticky = E)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 4, column = 2, sticky = E)
    entryXSecond = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 4, column = 1, sticky = W)
    entryYSecond = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 4, column = 3, sticky = W)

    Button(rootWindow, text = "Построить отрезок", font = fontSettingLower, command = print()).grid(row = 5, columnspan = 5)

    Label(rootWindow, text = "────────────────────────────────────────────────────────────────────────────────", font = fontSettingLower, width = 79).grid(row = 6, columnspan = 6, sticky = NW)
    Label(rootWindow, text = "Угловой шаг при построении отрезков (в градусах): ", font = fontSettingLower).grid(row = 7, columnspan = 3)
    angleEntry = Entry(rootWindow, font = fontSettingLower, width = 13).grid(row = 7, column = 2)

    canvasLinesColor = Canvas(rootWindow, bg = "black", borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasLinesColor.grid(row = 8, column = 1, sticky = W)
    Button(rootWindow, text = "Цвет отрезков: ", font = fontSettingLower, command = lambda: chooseLinesColor(canvasLinesColor, rootWindow, 8, 1)).grid(row = 8, column = 0, sticky = E)

    canvasBackgroundColor = Canvas(rootWindow, bg = "white", borderwidth = 5, relief = RIDGE, width = 60, height = 40)
    canvasBackgroundColor.grid(row = 8, column = 3, sticky = W)
    Button(rootWindow, text = "Цвет фона: ", font = fontSettingLower, command = lambda: chooseBackgroundColor(canvasBackgroundColor, rootWindow, 8, 3)).grid(row = 8, column = 2, sticky = E)

    Label(rootWindow, text = "Длина каждого из отрезков:", font = fontSettingLower).grid(row = 9)
    lenghEntry = Entry(rootWindow, font = fontSettingLower).grid(row = 9, column = 1)

    Button(rootWindow, text = "Исследование визуальных характеристик отрезков,\n построенных разными алгоритмами", font = fontSettingLower, command = print(), width = 50).grid(row = 10, columnspan = 5)
    Button(rootWindow, text = "Исследование временных характеристик", font = fontSettingLower, command = print(), width = 50).grid(row = 11, columnspan = 5)

    canvasWindow = Canvas(rootWindow, bg = "white", width = 880, height = 1017, borderwidth = 5, relief = RIDGE)
    canvasWindow.grid(row = 0, column = 7, rowspan = 13)


    ''' QUICKLY
        Button(rootWindow, text = "", font = fontSettingLower, command = print()).grid(row = , column = , columnspan =, rowspan = )
        Entry(rootWindow, font = fontSettingLower).grid(row = , column = , columnspan =, rowspan = )
        Label(rootWindow, text = "", font = fontSettingLower).grid(row = , column = , columnspan =, rowspan = )
    '''
    # EXAMPLE FOR PIXEL WORK
    # Хеххехехеххехехеххех colorchooser.askcolor()
    # img = PhotoImage(width = 1075, height = 1055)
    # canvasWindow.create_image((1075, 1055
    # ), image=img, state = "normal")
    # for i in range(100):
    #     img.put("black", (500 + i, 500 - i))

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()

makeMainWindow()

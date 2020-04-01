from tkinter import *
from math import *
from tkinter import ttk

fontSettingLabels = ("Source code pro", 20)
fontSettingLower = ("Source code pro", 16)


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
          text = "Сделоть лабу...").grid()

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
    rootWindow.title("Рабораторная работа 3, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+60+0")

    # Выбор метода построения
    Label(rootWindow, text = "Метод построения:", font = fontSettingLower).grid(row = 0, column = 0, columnspan = 1)
    listBox = ttk.Combobox(rootWindow, width = 60)
    listBox.grid(row = 0, column = 1, columnspan = 4)

    Label(rootWindow, text = "Начальная точка отрезка", font = fontSettingLower).grid(row = 1, columnspan = 5)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 2)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 2, column = 2)
    entryXFirst = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 2, column = 1)
    entryYFirst = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 2, column = 3)

    Label(rootWindow, text = "Конечная точка отрезка", font = fontSettingLower).grid(row = 3, columnspan = 5)
    Label(rootWindow, text = "Координата X:", font = fontSettingLower).grid(row = 4)
    Label(rootWindow, text = "Координата Y:", font = fontSettingLower).grid(row = 4, column = 2)
    entryXSecond = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 4, column = 1)
    entryYSecond = Entry(rootWindow, font = fontSettingLower, width = 5).grid(row = 4, column = 3)

    Button(rootWindow, text = "Построить отрезок", font = fontSettingLower, command = print()).grid(row = 5, columnspan = 5)

    Label(rootWindow, text = "Угол поворота при построении каждого отрезка (в градусах): ", font = fontSettingLower).grid(row = 6, columnspan = 4)
    Entry(rootWindow, font = fontSettingLower).grid(row = 6, column = 4)

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1075, height = 1055)
    canvasWindow.grid(row = 0, column = 6, rowspan = 20)

    ''' QUICKLY
        Button(rootWindow, text = "", font = fontSettingLower, command = print()).grid(row = , column = , columnspan =, rowspan = )
        Entry(rootWindow, font = fontSettingLower).grid(row = , column = , columnspan =, rowspan = )
        Label(rootWindow, text = "", font = fontSettingLower).grid(row = , column = , columnspan =, rowspan = )
    '''
    # EXAMPLE FOR PIXEL WORK
    # img = PhotoImage(width = 1075, height = 1055)
    # canvasWindow.create_image((1075, 1055
    # ), image=img, state = "normal")
    # for i in range(100):
    #     img.put("black", (500 + i, 500 - i))

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()

makeMainWindow()

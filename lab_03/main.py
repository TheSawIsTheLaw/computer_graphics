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
    rootWindow.configure(background = "gray")
    rootWindow.minsize(1800, 920)
    listBox = ttk.Combobox(rootWindow)
    listBox.grid()

    canvasWindow = Canvas(rootWindow, bg = "white", width = 1075, height = 1055)
    canvasWindow.grid(row = 0, column = 3, rowspan = 20)

    # EXAMPLE FOR PIXEL WORK
    # img = PhotoImage(width = 1075, height = 1055)
    # canvasWindow.create_image((1075 / 2, 1055 / 2), image=img, state = "normal")
    # for i in range(100):
    #     img.put("black", (500 + i, 500 - i))

    makeCascadeMenu(rootWindow)

    rootWindow.mainloop()


makeMainWindow()

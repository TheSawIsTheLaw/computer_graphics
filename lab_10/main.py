from tkinter import *
from tkinter import ttk

fontSettingLabels = ("Consolas", 20)
fontSettingLower = ("Consolas", 16)

delay = 0
img = 0

curLine = 0

curColorBackground = "#000000"
curColorFigure = "#ffff00"

comboWhatToDraw = 0
tempArr = []

figureArray = []

cutterArray = []


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


def setComboWhatToDraw(rootWindow):
    Label(rootWindow, text = "Уравнение поверхности:", font = fontSettingLower).place(x = 5, y = 140)
    global comboWhatToDraw
    comboWhatToDraw = ttk.Combobox(rootWindow,
                              width = 75,
                              textvariable = delay,
                              state = 'readonly',
                              values =
                                ('x² + y² = z²',
                                 '...'))

    comboWhatToDraw.place(x = 275, y = 145)
    comboWhatToDraw.current(0)


def setImageToCanvas(canvasWindow):
    global img
    img = PhotoImage(width = 1090, height = 1016)
    canvasWindow.create_image((545, 508), image = img, state = "normal")


def makeMainWindow():
    """
            Функция Создания главного окна
    """
    rootWindow = Tk()
    rootWindow.title("Лабораторная работа 10, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.geometry("1850x1080+1980+0")

    canvasWindow = Canvas(rootWindow, bg = curColorBackground, width = 1090, height = 1016, borderwidth = 5, relief = RIDGE)

    setImageToCanvas(canvasWindow)

    canvasWindow.place(x = 750, y = 0)

    setComboWhatToDraw(rootWindow)

    Label(text = "Алгоритм Плавающего горизонта\nпостроения трёхмерных моделей", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 15)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

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
    Label(rootWindow, text = "Уравнение поверхности:", bg = "black", fg = "white", borderwidth = 5, relief = RIDGE, font = fontSettingLower).place(x = 5, y = 112)
    global comboWhatToDraw
    comboWhatToDraw = ttk.Combobox(rootWindow,
                              width = 75,
                              textvariable = delay,
                              state = 'readonly',
                              values =
                                ('x² + y² = z²',
                                 '...'))

    comboWhatToDraw.place(x = 280, y = 120)
    comboWhatToDraw.current(0)


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

    Label(text = "Начало по y:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 5, y = 270)
    yLimitStartEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    yLimitStartEntry.place(x = 210, y = 270)
    Label(text = "Конец по y:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 430, y = 270)
    yLimitEndEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    yLimitEndEntry.place(x = 630, y = 270)

    Label(text = "Шаг", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLabels, width = 48).place(x = 5, y = 320)
    Label(text = "Шаг по x:", borderwidth = 10, relief = RIDGE, bg = "black", fg = "white",
          font = fontSettingLower, width = 15).place(x = 5, y = 380)
    xStepEntry = Entry(rootWindow, font = fontSettingLower, borderwidth = 10, relief = RIDGE, width = 8)
    xStepEntry.place(x = 210, y = 380)

    showButton = Button(rootWindow, text = "Отрисовать фигуру", command = print(), height = 2, width = 61, font = fontSettingLower, bg = "#FF9C00")
    showButton.place(x = 5, y = 450)

    makeCascadeMenu(rootWindow, canvasWindow)

    rootWindow.mainloop()


makeMainWindow()

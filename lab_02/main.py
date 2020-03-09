from tkinter import *
from re import *

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
    rootWindow.title("Рабораторная работа 2, Якуба Дмитрий, ИУ7-43Б")
    rootWindow.minsize(1800, 1000)
    fontSettingLabels = ("Source code pro", 20)
    fontSettingLower = ("Source code pro", 16)

    Label(rootWindow, text = "Перенос", font = fontSettingLabels).grid(row = 0, column = 0, rowspan = 1, columnspan = 2)
    transferEntryX = Entry(rootWindow, font = fontSettingLower)
    transferEntryX.grid(row=1, column=1)
    transferEntryY = Entry(rootWindow, font = fontSettingLower)
    transferEntryY.grid(row = 2, column = 1)
    Label(rootWindow, text = "dx:", font = fontSettingLower).grid(row = 1, column = 0, rowspan = 1)
    Label(rootWindow, text = "dy:", font = fontSettingLower).grid(row = 2, column = 0, rowspan = 1)
    Button(rootWindow, text = "Выполнить преобразование\n'перенос'", font = ("consolas", 14), command=lambda: print("lul")).grid(row = 3, column = 0, columnspan = 2)
    Label(font = fontSettingLower, text = "--------------------------------------------------------------------------------------------------------------").grid(row = 4, columnspan = 2)

    Label(rootWindow, text = "Масштабирование", font = fontSettingLabels).grid(row = 5, column = 0, rowspan = 1, columnspan = 2)
    masstXCoef = Entry(rootWindow, font = fontSettingLower)
    masstYCoef = Entry(rootWindow, font = fontSettingLower)
    centerX = Entry(rootWindow, font = fontSettingLower)
    centerY = Entry(rootWindow, font = fontSettingLower)

    masstXCoef.grid(row = 6, column = 1)
    masstYCoef.grid(row = 7, column = 1)
    centerX.grid(row = 8, column = 1)
    centerY.grid(row = 9, column = 1)

    Label(rootWindow, font = fontSettingLower, text = "Коэффициент масштабирования по оси X:").grid(row = 6, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Коэффициент масштабирования по оси Y:").grid(row = 7, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Координата центра массштабирования по оси X:").grid(row = 8, column = 0)
    Label(rootWindow, font = fontSettingLower, text = "Координата центра массштабирования по оси Y:").grid(row = 9, column = 0)

    Button(rootWindow, text = "Выполнить преобразование\n'массштабирование'", font = ("consolas", 14), command = lambda: print("lul")).grid(row = 10, column = 0,
                                                                                                                                   columnspan = 2)

    canvasWindow = Canvas(rootWindow, bg = "black", width = 1060, height = 1040)
    canvasWindow.grid(row = 0, column = 4, rowspan = 16)

    rootWindow.mainloop()


makeMainWindow()

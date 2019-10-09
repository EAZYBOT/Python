import textwrap
import math


def read_float_element(text):
    res = None
    while res is None:
        try:
            res = float(input(text))
        except ValueError:
            res = None
            print("Ошибка! Введите вещественное число.")
    return res


def read_int_element(text):
    res = None
    while res is None:
        try:
            res = int(input(text))
        except ValueError:
            res = None
            print("Ошибка! Введите целое число.")
    return res


def print_text_menu():
    text = """
        С) Площадь круга
        E) Площадь эллипса
        M) Площадь многоугольника
        
        Q) Выход
    """
    print(textwrap.dedent(text))


def area_circle():
    r = read_float_element("R: ")
    res = math.pi * math.pow(r, 2)
    print("Результат:", res)


def area_ellipsis():
    a, b = None, None
    a = read_float_element("a: ")
    b = read_float_element("b: ")
    res = math.pi*a*b
    print("Результат:", res)


def area_polygon():
    n, a = None, None
    a = read_float_element("Длина стороны многоугольника: ")
    n = read_int_element("Кол-во сторон: ")

    res = (n * math.pow(a, 2)) / (4*math.tan(math.pi / n))
    print("Результат: ", res)


running = True
while running:
    print_text_menu()

    choice = 0
    try:
        choice = input("\nВыбор: ")
    except ValueError:
        print("Введите корректное значение")
        continue

    if choice == 'C':
        area_circle()
    elif choice == 'E':
        area_ellipsis()
    elif choice == 'M':
        area_polygon()
    elif choice == 'Q':
        running = False
        continue
    else:
        print("Нет такого пункта меню")

    input("Нажмите ENTER")


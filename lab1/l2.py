import textwrap


def print_text_menu():
    text = """
        1) Показать все элементы списка
        2) Вставить элемент
        3) Удалить элемент
        4) Кортеж из строковых элементов
        5) Сумма отрицательных элементов
        6) Кол-во букв в строке
        7) Разница множеств
        8) Словарь из нечетных элементов
    
        0) Выход
    """
    print(textwrap.dedent(text))


def insert(list_elements):
    index = None
    while index is None:
        try:
            index = int(input("Введите индекс: "))
        except ValueError:
            index = None

    type_item = None
    while type_item is None:
        type_item = input("Введите тип вставляемого элемента[f, i, c, s]:")
        if len(type_item) > 1 or type_item not in "fics":
            print("Введите букву из списка!")
            type_item = None

    value = None
    if type_item == 'f':
        while value is None:
            try:
                value = float(input("Введите float: "))
            except ValueError:
                value = None
                print("Ошибка!")
    elif type_item == 'i':
        while value is None:
            try:
                value = int(input("Введите int: "))
            except ValueError:
                value = None
                print("Ошибка!")
    elif type_item == 'c':
        while value is None:
            try:
                value = complex(input("Введите complex: "))
            except ValueError:
                value = None
                print("Ошибка!")
    else:
        value = input("Введите строку: ")

    list_elements.insert(index, value)


def delete_element(list_elements):
    list_elements.pop()


def tuple_of_str(list_elements):
    result = []
    for element in list_elements:
        if type(element) == str:
            result.append(element)

    print(tuple(result))


def sum_of_neg_int(list_elements):
    result = 0
    for element in list_elements:
        if type(element) == int and element < 0:
            result += element

    print("Результат:", result)


def len_str_list(list_elements):
    result = ""
    for element in list_elements:
        result += str(element)

    print("Строка:", result)
    print("Кол-во букв:", len(result))


def difference_of_sets(list_elements):
    m1_str = input("M1 (Через пробел): ")

    m1_list = []
    for elem in m1_str.split(' '):
        value = None

        if 'j' in elem:
            try:
                value = complex(elem)
            except ValueError:
                value = None

        if (value is None) and ('.' in elem):
            try:
                value = float(elem)
            except ValueError:
                value = None

        if value is None:
            try:
                value = int(elem)
            except ValueError:
                value = elem

        m1_list.append(value)

    m1 = set(m1_list)

    m2 = set(list_elements)

    print(m2.difference(m1))


def dictionary_of_list(list_elements):
    result = {}
    i = 0

    for element in list_elements:
        if i % 2 != 0:
            result[i] = element
        i += 1

    print(result)


my_list = [123, 2.13, "Example", "Example2", 0 + 1j]

running = True
while running:
    print_text_menu()

    choice = 0
    try:
        choice = int(input("\nВыбор: "))
    except ValueError:
        print("Введите корректное значение")
        continue

    if choice == 0:
        running = False
        continue
    elif choice == 1:
        print(my_list)
    elif choice == 2:
        insert(my_list)
    elif choice == 3:
        delete_element(my_list)
    elif choice == 4:
        tuple_of_str(my_list)
    elif choice == 5:
        sum_of_neg_int(my_list)
    elif choice == 6:
        len_str_list(my_list)
    elif choice == 7:
        difference_of_sets(my_list)
    elif choice == 8:
        dictionary_of_list(my_list)
    else:
        print("Нет такого пункта меню")

    input("Нажмите ENTER")

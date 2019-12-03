import textwrap
import re
from PetsManager import PetsManager


class DialogHandler:
    def __init__(self):
        self.pets_manager = PetsManager()

    @staticmethod
    def print_menu():
        text = """
                1) Добавить питомца
                2) Удалить питомца
                3) Поиск питомца по ФИО
                4) Вывод всех питомцев
                
                0) Выход
            """
        print(textwrap.dedent(text))

    @staticmethod
    def print_pet(pet):
        text = """
            ID: {}
            Вид: {}
            Кличка: {}
            Окрас: {}
            День рождения: {}
            ФИО владельца: {}
            Телефон владельца: {}
        """.format(pet.id, pet.type, pet.nickname, pet.color, pet.birthday, pet.owner, pet.phone)

        print(textwrap.dedent(text))

    def add_pet(self):
        while True:
            try:
                new_id = int(input("Введите ID: "))
                if self.pets_manager.get_pet(new_id) is not None:
                    print("Такой ID уже существует!")
                else:
                    break
            except ValueError:
                print("Введён не корректный ID!")

        type_pet = ""
        while True:
            type_pet = input("Введите вид питомца: ")
            if re.fullmatch("[A-ZА-Я][a-zа-я]*", type_pet):
                break
            else:
                print("Некорректное значение")

        nickname = ""
        while True:
            nickname = input("Введите кличку питомца: ")
            if re.fullmatch("[A-ZА-Я][a-zа-я]*", nickname):
                break
            else:
                print("Некорректное значение")

        color = ""
        while True:
            color = input("Введите окрас шерсти питомца: ")
            if re.fullmatch("[A-ZА-Я][a-zа-я]*", color):
                break
            else:
                print("Некорректное значение")

        birthday = ""
        while True:
            birthday = input("Введите день рождения питомца[DD-MM-YYYY]: ")
            if re.fullmatch("\d{2}-\d{2}-\d{4}", birthday):
                break
            else:
                print("Некорректное значение")

        owner = ""
        while True:
            owner = input("Введите ФИО владельца: ")
            if re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
                break
            else:
                print("Некорректное значение")

        phone = ""
        while True:
            phone = input("Введите номер телефона владельца[+7XXXXXXXXXX]: ")
            if re.fullmatch("\+?\d{11}", phone):
                break
            else:
                print("Некорректное значение")

        self.pets_manager.add_pet(new_id, type_pet, nickname, color, birthday, owner, phone)

        print("Запись добавлена")

    def delete_pet(self):
        try:
            new_id = int(input("Введите ID: "))
            if self.pets_manager.get_pet(new_id) is not None:
                self.pets_manager.delete_pet(new_id)
                print("Успешно удалено!")
            else:
                print("Такого ID не существует!")
        except ValueError:
            print("Введён не корректный ID!")

    def print_all(self):
        if len(self.pets_manager.get_pets()) == 0:
            print("База пуста!")

        for pet in self.pets_manager.get_pets():
            self.print_pet(pet)

    def search_by_owner(self):
        owner = ""
        while True:
            owner = input("Введите ФИО владельца: ")
            if re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
                break
            else:
                print("Некорректное значение")

        pets = self.pets_manager.search_pet_by_owner(owner)

        if len(pets) != 0:
            for pet in pets:
                self.print_pet(pet)
        else:
            print("Нет ни одного питомца с введённым владельцем!")

    def run(self):
        running = True
        while running:
            self.print_menu()

            choice = 0
            try:
                choice = int(input("\nВыбор: "))
            except ValueError:
                print("Введите корректное значение")
                input("Нажмите ENTER")
                continue

            if choice == 1:
                self.add_pet()
            elif choice == 2:
                self.delete_pet()
            elif choice == 3:
                self.search_by_owner()
            elif choice == 4:
                self.print_all()
            elif choice == 0:
                running = False
                continue
            else:
                print("Нет такого пункта меню")

            input("Нажмите ENTER")

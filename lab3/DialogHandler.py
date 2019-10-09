import textwrap
import PetsManager


class DialogHandler:
    def __init__(self):
        if __name__ == '__main__':
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

    def add_pet(self):
        id = int(input("Введите ID: "))

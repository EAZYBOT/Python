import re
from lab4.Pet import Pet


class PetsManager:
    def __init__(self):
        self.pets = list()

    def add_pet(self, id_pet, type_pet, nickname, color, birthday, owner, phone):

        if self.get_pet(id_pet) is not None:
            return False

        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type_pet):
            raise ValueError

        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", nickname):
            raise ValueError

        if not re.fullmatch("[A-ZА-Я][a-zа-я-]*", color):
            raise ValueError

        if not re.fullmatch(r"\d{2}.\d{2}.\d{4}", birthday):
            raise ValueError

        if not re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
            raise ValueError

        if not re.fullmatch(r"\+?\d{11}", phone):
            raise ValueError

        new_pet = Pet(id_pet, type_pet, nickname, color, birthday, owner, phone)

        self.pets.append(new_pet)

        return True

    def delete_pet(self, id_pet):
        pet = self.get_pet(id_pet)

        if pet is None:
            return False
        else:
            self.pets.remove(pet)
            return True

    def get_pets(self):
        return self.pets

    def get_pet(self, id_pet):
        for pet in self.pets:
            if id_pet == pet.id:
                return pet

        return None

    def search_pet_by_owner(self, owner):
        result = []
        for pet in self.pets:
            if owner == pet.owner:
                result.append(pet)

        return result

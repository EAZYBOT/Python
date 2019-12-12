import re
import pymysql
from lab7.Pet import Pet


class PetsManager:
    def __init__(self):
        self.__config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root1213141516',
            'database': 'wets_db',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def __exec_query_with_result(self, query: str):
        con = pymysql.connect(**self.__config)

        with con:
            cur = con.cursor()
            cur.execute(query)
            return cur.fetchall()

    def __exec_query_without_result(self, query: str):
        con = pymysql.connect(**self.__config)

        with con:
            cur = con.cursor()
            cur.execute(query)

    def add_pet(self, type_pet: str, nickname: str, color: str, birthday: str, owner: str, phone: str):
        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type_pet):
            raise ValueError

        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", nickname):
            raise ValueError

        if not re.fullmatch(r"\d{2}.\d{2}.\d{4}", birthday):
            raise ValueError

        if not re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
            raise ValueError

        if not re.fullmatch(r"\+?\d{11}", phone):
            raise ValueError

        result = self.__exec_query_with_result("SELECT id FROM owners WHERE phone = {};".format(phone))
        if len(result) == 0:
            arr_owner = owner.split(' ')
            self.__exec_query_without_result(
                "INSERT INTO owners VALUES (null, '{}', '{}', '{}', '{}');".format(arr_owner[0], arr_owner[1],
                                                                                   arr_owner[2], phone)
            )

        arr_birhtday = birthday.split('.')
        birthday = "{}-{}-{}".format(arr_birhtday[2], arr_birhtday[1], arr_birhtday[0])
        self.__exec_query_without_result(
            "INSERT INTO wets VALUES (null, '{}', '{}', '{}', ".format(type_pet, nickname, birthday) +
            "(SELECT id FROM colors WHERE color = '{}' LIMIT 1), ".format(color) +
            "(SELECT id FROM owners WHERE phone = '{}' LIMIT 1));".format(phone)
        )

        return True

    def get_colors(self):
        return self.__exec_query_with_result("SELECT color FROM colors")

    def delete_all(self):
        self.__exec_query_without_result("DELETE FROM wets;")

    def delete_pet(self, id_pet: int):
        self.__exec_query_without_result("DELETE FROM wets WHERE id = {};".format(id_pet))

    def update_pet(self, id_pet: int, type_pet: str, nickname: str, color: str, birthday: str, owner: str, phone: str):
        if type(id_pet) != int:
            raise ValueError

        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type_pet):
            raise ValueError

        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", nickname):
            raise ValueError

        if not re.fullmatch(r"\d{2}.\d{2}.\d{4}", birthday):
            raise ValueError

        if not re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
            raise ValueError

        if not re.fullmatch(r"\+?\d{11}", phone):
            raise ValueError

        arr_owner = owner.split(' ')
        self.__exec_query_without_result(
            "UPDATE owners SET " +
            "second_name = '{}', ".format(arr_owner[0]) +
            "first_name = '{}', ".format(arr_owner[1]) +
            "middle_name = '{}', ".format(arr_owner[2]) +
            "phone = '{}' ".format(phone) +
            "WHERE id = (SELECT owners_id FROM wets WHERE id = {} LIMIT 1);".format(id_pet)
        )

        arr_birthday = birthday.split('.')
        birthday = "{}-{}-{}".format(arr_birthday[2], arr_birthday[1], arr_birthday[0])
        self.__exec_query_without_result(
            "UPDATE wets SET " +
            "type = '{}', ".format(type_pet) +
            "nick = '{}', ".format(nickname) +
            "birthday = '{}', ".format(birthday) +
            "colors_id = (SELECT id FROM colors WHERE color = '{}' LIMIT 1) ".format(color) +
            "WHERE id = {};".format(id_pet)
        )

    def get_pet(self, pet_id: int):
        return self.__exec_query_with_result(
            "SELECT wets.id AS id, type, nick, color, birthday, "
            "second_name, first_name, middle_name, phone "
            "FROM wets INNER JOIN colors ON colors_id = colors.id "
            "INNER JOIN owners ON owners_id = owners.id "
            "WHERE wets.id = {};".format(pet_id)
        )

    def get_pets(self):
        return self.__exec_query_with_result(
            "SELECT wets.id AS id, type, nick, color, birthday, "
            "second_name, first_name, middle_name, phone "
            "FROM wets INNER JOIN colors ON colors_id = colors.id "
            "INNER JOIN owners ON owners_id = owners.id;"
        )

    def search_pet_by_owner(self, owner: str):
        arr_owner = owner.split(' ')
        return self.__exec_query_with_result(
            "SELECT wets.id AS id, type, nick, color, birthday, "
            "second_name, first_name, middle_name, phone "
            "FROM wets INNER JOIN colors ON colors_id = colors.id "
            "INNER JOIN owners ON owners_id = owners.id "
            "WHERE second_name = '{}' AND first_name = '{}' AND middle_name = '{}';".format(arr_owner[0],
                                                                                            arr_owner[1],
                                                                                            arr_owner[2])
        )

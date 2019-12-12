from PyQt5 import QtWidgets
from PyQt5 import QtCore
import lab7.forms.search as search
import lab7.forms.about as about
import lab7.forms.edit as edit
from lab7.PetsManager import PetsManager
import re


class SearchWet(QtWidgets.QWidget, search.Ui_Form):
    def __init__(self, petManager: PetsManager):
        super().__init__()
        self.setupUi(self)

        self.petManager = petManager
        self.pushButton.clicked.connect(self.searchBtn)

    def searchBtn(self):
        owner = self.lineEdit.text()
        result = self.petManager.search_pet_by_owner(owner)

        self.tableWidget.setRowCount(0)

        for pet in result:
            index_row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(index_row)

            cellinfo = QtWidgets.QTableWidgetItem(str(pet["id"]))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 0, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["type"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 1, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["nick"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 2, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["color"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 3, cellinfo)

            arr_birthday = str(pet["birthday"]).split('-')
            birthday = "{}.{}.{}".format(arr_birthday[2], arr_birthday[1], arr_birthday[0])
            cellinfo = QtWidgets.QTableWidgetItem(birthday)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 4, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem("{} {} {}".format(pet["second_name"],
                                                                    pet["first_name"],
                                                                    pet["middle_name"]))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 5, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["phone"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 6, cellinfo)


class AboutWindow(QtWidgets.QWidget, about.Ui_About_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class EditWindow(QtWidgets.QWidget, edit.Ui_Edit_Form):
    def __init__(self, manager: PetsManager, pet_id: int):
        super().__init__()
        self.setupUi(self)

        self.manager = manager
        self.pet_id = pet_id

        self.btn_cancel.clicked.connect(self.close)
        self.btn_edit.clicked.connect(self.edit_item)

        pet = self.manager.get_pet(self.pet_id)[0]
        self.edit_type.setText(pet["type"])
        self.edit_nick.setText(pet["nick"])
        self.edit_owner.setText(
            "{} {} {}".format(pet["second_name"], pet["first_name"], pet["middle_name"])
        )
        self.edit_phone.setText(pet["phone"])
        self.dateEdit.setDate(pet["birthday"])

        self.update_colors()
        self.box_color_2.setCurrentIndex(self.box_color_2.findText(pet["color"]))

    def update_colors(self):
        self.box_color_2.clear()
        colors = self.manager.get_colors()
        for color in colors:
            self.box_color_2.addItem(color['color'])

    def edit_item(self):
        type_pet = self.edit_type.text()
        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type_pet):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введён некорретный вид')
            return

        nick = self.edit_nick.text()
        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", nick):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введена некорретная кличка')
            return

        owner = self.edit_owner.text()
        if not re.fullmatch("([A-ZА-Я][a-zа-я]* ){2}[A-ZА-Я][a-zа-я]*", owner):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введёно некорретное ФИО')
            return

        phone = self.edit_phone.text()
        if not re.fullmatch(r"\+?\d{11}", phone):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введён некорретный телефон')
            return

        color = self.box_color_2.currentText()

        birthday = self.dateEdit.text()

        self.manager.update_pet(self.pet_id, type_pet, nick, color, birthday, owner, phone)

        QtWidgets.QMessageBox.information(self, 'Успех', 'Элемент успешно изменёны')

        self.close()

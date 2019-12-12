import re
import sys

import lab7.forms.main_window as main_window
from lab7.UtilityWidgets import *


class WetApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    petManager = PetsManager()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchWin = SearchWet(self.petManager)
        self.aboutWidget = AboutWindow()
        self.editWidget = None

        self.btnDelete.clicked.connect(self.deleteItem)
        self.btnAdd.clicked.connect(self.addItem)
        self.btn_update.clicked.connect(self.updateTable)

        self.searchAct.triggered.connect(self.search)
        self.actAbout.triggered.connect(self.show_about)
        self.actQuit.triggered.connect(self.close)

        self.mainTable.doubleClicked.connect(self.editItem)
        self.update_colors()

        self.updateTable()

    def search(self):
        self.searchWin.show()

    def show_about(self):
        self.aboutWidget.show()

    def addItem(self):
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

        color = self.box_color.currentText()

        birthday = self.dateEdit.text()

        self.petManager.add_pet(type_pet, nick, color, birthday, owner, phone)

        QtWidgets.QMessageBox.information(self, 'Успех', 'Элемент успешно добавлен')
        self.updateTable()
        self.btnClear.click()

    def editItem(self):
        pet_id = int(self.mainTable.selectionModel().selectedRows(0)[0].data())
        self.editWidget = EditWindow(self.petManager, pet_id)
        self.editWidget.btn_edit.clicked.connect(self.updateTable)
        self.editWidget.show()

    def deleteItem(self):
        if self.cbAll.isChecked():
            self.petManager.delete_all()
        else:
            if len(self.mainTable.selectedIndexes()) == 0:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle('Ошибка')
                message.setText('Выделите элемент')
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.exec_()
                return

            list_id = []
            for index in self.mainTable.selectionModel().selectedRows(0):
                list_id.append(int(index.data()))

            for id_pet in list_id:
                self.petManager.delete_pet(id_pet)

        self.updateTable()

    def update_colors(self):
        self.box_color.clear()
        colors = self.petManager.get_colors()
        for color in colors:
            self.box_color.addItem(color['color'])

    def updateTable(self):
        self.update_colors()
        self.mainTable.setRowCount(0)

        pets = self.petManager.get_pets()

        for pet in pets:
            index_row = self.mainTable.rowCount()
            self.mainTable.insertRow(index_row)

            cellinfo = QtWidgets.QTableWidgetItem(str(pet["id"]))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 0, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["type"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 1, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["nick"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 2, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["color"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 3, cellinfo)

            arr_birthday = str(pet["birthday"]).split('-')
            birthday = "{}.{}.{}".format(arr_birthday[2], arr_birthday[1], arr_birthday[0])
            cellinfo = QtWidgets.QTableWidgetItem(birthday)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 4, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem("{} {} {}".format(pet["second_name"],
                                                                    pet["first_name"],
                                                                    pet["middle_name"]))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 5, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet["phone"])
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 6, cellinfo)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WetApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

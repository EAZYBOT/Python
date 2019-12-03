import sys
import re
import lab4.main_window as main_window
from lab4.PetsManager import PetsManager
import lab4.test_append as test_append
from lab4.SearchWeb import SearchWet
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class WetApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    petManager = PetsManager()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchWin = SearchWet(self.petManager)

        test_append.test_append(self.petManager)

        self.btnDelete.clicked.connect(self.deleteItem)
        self.btnAdd.clicked.connect(self.addItem)
        self.searchAct.triggered.connect(self.search)

        self.updateTable()

    def search(self):
        self.searchWin.show()

    def addItem(self):
        id = 0
        try:
            id = int(self.edit_id.text())
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введён некорретный ID')
            return

        if self.petManager.get_pet(id) is not None:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Такой ID уже существует')

        type = self.edit_type.text()
        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введён некорретный вид')
            return


        nick = self.edit_nick.text()
        if not re.fullmatch("[A-ZА-Я][a-zа-я]*", type):
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

        self.petManager.add_pet(id, type, nick, color, birthday, owner, phone)

        QtWidgets.QMessageBox.information(self, 'Успех', 'Элемент успешно добавлен')
        self.updateTable()
        self.btnClear.click()


    def deleteItem(self):
        if self.cbAll.isChecked():
            self.petManager.pets.clear()
        else:
            if len(self.mainTable.selectedIndexes()) == 0:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle('Ошибка')
                message.setText('Выделите элемент')
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.exec_()
                return

            list_id = []
            for item in self.mainTable.selectedItems():
                index = item.row()
                pet = self.petManager.get_pets()[index]
                list_id.append(pet.id)

            for id in list_id:
                self.petManager.delete_pet(id)

        self.updateTable()

    def updateTable(self):
        self.mainTable.setRowCount(0)

        pets = self.petManager.get_pets()

        for pet in pets:
            index_row = self.mainTable.rowCount()
            self.mainTable.insertRow(index_row)

            cellinfo = QtWidgets.QTableWidgetItem(str(pet.id))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 0, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.type)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 1, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.nickname)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 2, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.color)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 3, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.birthday)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 4, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.owner)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 5, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.phone)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.mainTable.setItem(index_row, 6, cellinfo)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WetApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
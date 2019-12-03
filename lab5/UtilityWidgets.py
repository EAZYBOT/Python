import sys
import re
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import lab5.search as search
import lab5.about as about
from lab4.PetsManager import PetsManager


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

            cellinfo = QtWidgets.QTableWidgetItem(str(pet.id))
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 0, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.type)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 1, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.nickname)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 2, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.color)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 3, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.birthday)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 4, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.owner)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 5, cellinfo)

            cellinfo = QtWidgets.QTableWidgetItem(pet.phone)
            cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(index_row, 6, cellinfo)


class About_window(QtWidgets.QWidget, about.Ui_About_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

import socket
import sys
import json
import string

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import lab6.client.main_window as main_window


class ClientApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_send.clicked.connect(self.send_text)

        self.counter = dict()
        self.update_info()

    def send_text(self):
        text = self.edit_text.text()

        client_socket = socket.socket()

        try:
            client_socket.connect(('localhost', 9005))

            client_socket.send(text.encode('utf-8'))
            text = client_socket.recv(1024).decode("utf-8")

            client_socket.close()
        except ConnectionError:
            print("Server is not founded")
            return

        self.edit_text.clear()

        self.counter = dict(json.loads(text))
        self.update_info()

    def update_info(self):
        for ch in string.ascii_lowercase:
            cell_info = self.findChild(QtWidgets.QLabel, 'l_{}'.format(ch))

            if cell_info is not None:
                cell_info.setText(str(self.counter.get(ch, 0)))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ClientApp()
    window.show()
    app.exec_()


def start():
    client_socket = socket.socket()

    client_socket.connect(('localhost', 9005))

    client_socket.send('Hello world!'.encode('utf-8'))
    data = client_socket.recv(1024).decode("utf-8")

    client_socket.close()

    print(data)


if __name__ == '__main__':
    main()

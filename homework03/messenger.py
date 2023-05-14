from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore
import clientui

class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host):
        super().__init__()
        self.host = host
        self.setupUi(self)

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def print_messages(self, message):
        t = message['time']
        dt = datetime.fromtimestamp(t)
        dt = dt.strftime('%H:%M:%S')
        self.textBrowser.append(dt + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')



    def get_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}
            )
        except:
            return
        messages = response.json()['messages']
        for message in messages:
            self.print_messages(message)
            self.after = message['time']


    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                self.host + '/send',

                json={
                    'name': name,
                    'text': text,

                }
            )
        except:
            # TODO the server is unavailable
            self.textBrowser.append('Сервер недоступен')
            self.textBrowser.append('Попробуйте позже')
            self.textBrowser.append('')

            return
        if response.status_code != 200:
            # TODO report an error
            self.textBrowser.append('Проверьте ваше имя и текст')
            self.textBrowser.append('')

            return

        self.textEdit.setText('')





app = QtWidgets.QApplication([])
window = Messenger(host='https://7cf0-2a00-1fa0-665-4bc0-f54e-dbff-8ef2-6629.ngrok-free.app')
window.show()
app.exec()
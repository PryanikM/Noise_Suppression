from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog, QMainWindow

from PyQt5.QtGui import QFont

from screen import Ui_Form
#
import sys
import os

class Form(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.nextScreen = Ui_Form()

        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))


        self.getFileNameButton = QtWidgets.QPushButton("Открыть файл")
        self.getFileNameButton.clicked.connect(self.get_file_name)

        self.startWorkButton = QtWidgets.QPushButton("Начать обработку")
        self.startWorkButton.clicked.connect(self.start_work)

        self.file_name = ''




        layoutV = QtWidgets.QVBoxLayout()
        layoutV.addWidget(self.getFileNameButton)

        layoutV.addWidget(self.startWorkButton)


        layoutH = QtWidgets.QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)

        centerWidget = QtWidgets.QWidget()
        centerWidget.setLayout(layoutH)
        self.setCentralWidget(centerWidget)

        self.resize(740, 480)
        self.setWindowTitle("PyQt5-QFileDialog")


    def get_file_name(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "wav file(*.wav);; Mp3 Files(*.Mp3);;\
                                                         All Files(*)")
        self.plainTextEdit.appendHtml("<br><b>{}</b> <br>"
                                      "".format(filename, filetype))


        self.file_name = filename

    def start_work(self):
        # print('Here')
        # print(self.file_name != '')
        if self.file_name != '':
            self.file_name.replace('\\', '/')
            if self.nextScreen.set_audio(self.file_name) != -1:
                global Form
                Form = QtWidgets.QWidget()
                self.nextScreen.setupUi(Form)
                ex.close()
                Form.show()
            else:
                pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())

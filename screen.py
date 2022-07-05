from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from MplForWidget import PlotCanvas
from NoiseSuppression import NoiseSuppression

import simpleaudio as sa
import numpy as np

class Ui_Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.k = NoiseSuppression()
        #self.k.set_audio('C:/Project/USATU_Lab/Практика/music.wav')

        self.play_obj = None

    def set_audio(self, path_to_file):
        if not self.k.set_audio(path_to_file):
            return -1
        else:
            return 1

    def __check_target_amplitude(self):
        str_input = str(self.textEdit_2.text())
        if str_input == '':
            return -1
        else:
            rng = [int(str_input)]
            return rng

    def __check_range(self):
        str_input = str(self.textEdit.text())
        print(str_input)
        if str_input == '':
            return -1
        else:
            if '-' in str_input:
                try:
                    rng = list(map(int, str_input.replace(" ", '').split('-')))
                except Exception:
                    return -1
                if (len(rng) == 2) and (rng[0] < rng[1]) and (0 <= rng[0]) and (rng[1] <= self.k.get_audio().shape[0]):
                    return rng
                else:
                    return -1
            else:
                rng = list(map(int, str_input.split(" ")))
                if len(rng) == 1 and 0 <= rng[0] <= self.k.get_audio().shape[0]:
                    return rng
                else:
                    return -1

    def delete_noise_button_click(self):
        answer_range = self.__check_range()
        answer_amplitude = self.__check_target_amplitude()
        if answer_range != -1:
            if answer_amplitude != -1:
                xf, yf = self.k.delete_noise(answer_range, answer_amplitude)
            else:
                xf, yf = self.k.delete_noise(answer_range)

        else:
            xf, yf = self.k.delete_noise()
        self.delete_noise_widget.plot(xf, yf)

    def play_audio(self, audio, sample_rate):
        if self.play_obj is not None:
            if not self.play_obj.is_playing():
                print(self.play_obj.is_playing())
                self.play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        else:
            self.play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    def play_original_audio(self):
        self.play_audio(self.k.get_audio(), self.k.get_sample_rate())

    def play_clear_audio(self):
        audio = self.k.get_clear_audio()
        if audio is not None:
            self.play_audio(self.k.get_clear_audio(), self.k.get_sample_rate())
        #self.play_obj = sa.play_buffer(self.k.get_clear_audio(), 1, 2, self.k.get_sample_rate())

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1093, 713)

        self.delete_noise_button = QtWidgets.QPushButton(Form)
        self.delete_noise_button.setGeometry(QtCore.QRect(150, 580, 181, 51))
        self.delete_noise_button.setObjectName("delete_noise_button")
        self.delete_noise_button.clicked.connect(self.delete_noise_button_click)

        self.delete_noise_widget = PlotCanvas(Form, width=5, height=4, color='g', text='Очищенный сигнал')
        self.delete_noise_widget.setGeometry(QtCore.QRect(490, 410, 591, 291))
        self.delete_noise_widget.setObjectName("delete_noise_widget")

        self.frequency_response_widget = PlotCanvas(Form, width=5, height=4, color='m', text='Сигнал')
        self.frequency_response_widget.setGeometry(QtCore.QRect(490, 10, 591, 291))
        self.frequency_response_widget.setObjectName("frequency_response_widget")
        xf, yf = self.k.get_frequency_response()
        self.frequency_response_widget.plot(xf, yf)

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 40, 481, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.plainTextEdit = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.textEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setValidator(QRegExpValidator(QRegExp('^[0-9\-]+[0-9]')))

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 220, 481, 45))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.plainTextEdit_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")

        self.verticalLayout_2.addWidget(self.plainTextEdit_2)

        self.textEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_2.addWidget(self.textEdit_2)
        self.textEdit_2.setValidator(QRegExpValidator(QRegExp('^[0-9]+$')))

        self.original_audio_button = QtWidgets.QPushButton(Form)
        self.original_audio_button.setGeometry(QtCore.QRect(0, 470, 181, 51))
        self.original_audio_button.setObjectName("original_audio_button")
        self.original_audio_button.clicked.connect(self.play_original_audio)

        self.modify_audio_button = QtWidgets.QPushButton(Form)
        self.modify_audio_button.setGeometry(QtCore.QRect(300, 470, 181, 51))
        self.modify_audio_button.setObjectName("modify_audio_button")
        self.modify_audio_button.clicked.connect(self.play_clear_audio)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.delete_noise_button.setText(_translate("Form", "Убрать шум"))
        self.plainTextEdit.setText(
            _translate("Form", f"Введите диапозон частоты, который нужно очистить. Формат: {0} - "
                               f"{self.k.get_audio().shape[0]}"))
        self.plainTextEdit_2.setText(_translate("Form", "Введите с какой амплитуды нужно очистить\n"""))

        self.original_audio_button.setText(_translate("Form", "Послушать оригинал"))
        self.modify_audio_button.setText(_translate("Form", "Послушать очищенную версию"))


if __name__ == "__main__":
    import sys
    print('HERE')
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     import sys
#     print('HERE')
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())

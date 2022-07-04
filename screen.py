from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from MplForWidget import PlotCanvas
from NoiseSuppression import NoiseSuppression


class Ui_Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.k = NoiseSuppression()
        self.k.set_audio('music.wav')

    def __check_range(self):
        str_input = str(self.textEdit.text())
        try:
            rng = list(map(int, str_input.replace(" ", '').split('-')))
        except Exception:
            return -1
        if (rng[0] < rng[1]) and 0 <= rng[0] and rng[1] <= self.k.get_audio().shape[0]:
            return rng
        else:
            return -1

    def delete_noise_button_click(self):
        xf, yf = self.k.delete_noise()
        print(self.__check_range())
        self.delete_noise_widget.plot(xf, yf)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1093, 713)

        self.delete_noise_button = QtWidgets.QPushButton(Form)
        self.delete_noise_button.setGeometry(QtCore.QRect(40, 530, 181, 51))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.delete_noise_button.setText(_translate("Form", "Убрать шум"))
        self.plainTextEdit.setText(
            _translate("Form", f"Введите диапозон частоты, который нужно очистить. Формат: {0} - "
                               f"{self.k.get_audio().shape[0]}"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

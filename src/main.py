from PyQt5 import QtWidgets
import sys

from views.login import LoginUi


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginUi()
    app.exec_()

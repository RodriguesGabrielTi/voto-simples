import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


def button1_clicked():
    print("button work!")


def window():
    app = QApplication(sys.argv)
    widget = QWidget()

    text_label = QLabel(widget)
    text_label.setText("Hello World!")
    text_label.move(110, 85)

    button1 = QPushButton(widget)
    button1.setText("Button1")
    button1.move(64, 32)
    button1.clicked.connect(button1_clicked)

    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("Voto Simples")
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()

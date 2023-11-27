import sys
from PyQt6.QtWidgets import QApplication
from mainwindow.mainwindow import MainWindow


if "__main__" == __name__:
    app = QApplication(sys.argv)

    calc = MainWindow()
    calc.show()

    sys.exit(app.exec())

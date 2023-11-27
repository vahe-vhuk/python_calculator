from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from .buttons import buttons
from .styles import calc_btn, input_expr, main_window


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = {i: QPushButton(i, self) for i in buttons}
        self.input = QLineEdit("0", self)

        self.setFixedSize(305, 390)
        self.setWindowTitle("Calculator")
        self.setStyleSheet(main_window)

        self.init_ui()

    def init_ui(self):

        for btn in self.buttons:
            self.buttons[btn].setGeometry(*buttons[btn])
            self.buttons[btn].setStyleSheet(calc_btn)
            self.buttons[btn].clicked.connect(lambda _=None, sym=btn: self.press_event(_, sym))

        self.input.setGeometry(5, 10, 295, 60)
        self.input.setStyleSheet(input_expr)
        self.input.setMaxLength(21)
        self.input.setEnabled(False)

    def press_event(self, *args):
        text = self.input.text()
        if text == "error":
            text = "0"

        match args[1]:
            case sym if sym in "C=«":
                self.exec_command(text, sym)
            case sym if sym in "11234567890":
                self.add_num(text, sym)
            case sym if sym in "+-*/.":
                self.add_operator(text, sym)

    def exec_command(self, text, sym):
        res = text
        match sym:
            case "C":
                res = "0"
            case "=":
                try:
                    res = str(eval(text))
                except Exception:
                    res = "error"
            case "«":
                res = text[:-1]
                if res == "":
                    res = "0"
        self.input.setText(res)

    def add_num(self, text, sym):
        if text == "0":
            text = ""
        self.input.setText(text + sym)

    def add_operator(self, text, sym):
        operators = "+-*/"
        res = text
        match sym:
            case ".":
                res = text + "."
            case "-":
                if text == "0":
                    text = ""
                if text[-1:] != "-":
                    res = text + "-"
            case sym if sym in "+/*":
                if text != "0" and text[-1:] not in operators:
                    res = text + sym
        self.input.setText(res)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter - 1:
            key = "="
        elif event.key() == Qt.Key.Key_Backspace:
            key = "«"
        elif event.key() == Qt.Key.Key_Escape:
            key = "C"
        else:
            key = event.text()
        self.press_event(False, key)

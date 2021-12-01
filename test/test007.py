import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGridLayout,
    QWidget,
)
from PyQt5.QtGui import QTextCursor


class VentanaFindText(QMainWindow):
    def __init__(self):
        super(VentanaFindText, self).__init__()
        self.setWindowTitle("find text - QTextEdit")
        self.resize(475, 253)
        self.line_buscar = QLineEdit()
        self.btn_buscar = QPushButton("buscar",)
        self.text_edit = QTextEdit()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(central_widget)
        grid_layout.addWidget(self.line_buscar, 0, 0)
        grid_layout.addWidget(self.btn_buscar, 0, 1)
        grid_layout.addWidget(self.text_edit, 1, 0, 1, 2)

        self.btn_buscar.clicked.connect(self.gotoLine)

    def gotoLine(self):
        text = self.line_buscar.text()
        try:
            n = int(text)
        except ValueError:
            print("Cannot convert '{}' to integer number".format(text))
        else:
            if n < 1:
                print("The number must be greater than 1")
                return
            doc = self.text_edit.document()
            self.text_edit.setFocus()
            if n > doc.blockCount():
                self.text_edit.insertPlainText("\n" * (n - doc.blockCount()))
            cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
            self.text_edit.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFindText()
    ventana.show()
    sys.exit(app.exec_())
## !/usr/bin/python3
# _*_ coding: utf-8 _*_

import sys

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('文本编辑器')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
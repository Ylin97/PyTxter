## !/usr/bin/python3
# _*_ coding: utf-8 _*_

import sys
from PyQt5.QtCore import QLocale, QTranslator

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    if len(sys.argv) > 1:
        locale = sys.argv[1]
    else:
        locale = QLocale.system().name()
    translator.load('resource/qt_%s.qm' % locale)
    # 切换语言，主要针对系统窗口如字体选择
    app.installTranslator(translator)
    app.setApplicationName('PyTxter')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
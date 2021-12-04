# -*- coding: utf-8 -*-

"""
PyQt5 教程

这个程序是将一个窗口显示在屏幕的中心。

作者：我的世界你曾经来过
博客：http://blog.csdn.net/weiaitaowang
最后编辑：2016年7月30日
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # self.setGeometry(300, 300, 300, 220)

        self.center()

        self.setWindowTitle('窗口居中')        
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
#! /usr/bin/python3
# coding=utf-8


import sys
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QAction, qApp, QTextEdit, QFileDialog, QShortcut, \
    QPlainTextEdit

# Global variable
file_path = None


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menu = self.menuBar().addMenu('文件')  # 创建一个菜单栏
        self.text = QPlainTextEdit()  # 定义一个文本编辑器
        self.initUI()

    def initUI(self):
        """初始化主界面"""

        # 初始化主界面
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self.text)

        # 菜单项
        self.create_file_menu()

        # 显示
        self.show()

    def create_file_menu(self):
        """创建文件菜单"""
        self.open_file()
        self.save()
        self.save_as()
        self.quit()

    # 打开
    def open_file_dialog(self):
        global file_path
        path = QFileDialog.getOpenFileName(window, 'open')[0]
        if path:
            self.text.setPlainText(open(path, 'r', encoding='utf-8').read())
            file_path = path

    def open_file(self):
        self.open_action = QAction('打开')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.menu.addAction(self.open_action)

        self.menu.addSeparator()

    # 保存
    def save_dialog(self):
        if file_path is None:
            pass
        else:
            with open(file_path, 'w', encoding='utf-8') as fw:
                fw.write(self.text.toPlainText())
            self.text.document().setModified(False)

    def save(self):
        self.save_action = QAction('保存')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_dialog)
        self.menu.addAction(self.save_action)

        self.menu.addSeparator()

    # 另存为
    def save_as_dialog(self):
        global file_path
        path = QFileDialog.getSaveFileName(window, '另存为')[0]
        if path:
            file_path = path
            self.save_dialog()

    def save_as(self):
        self.save_as_action = QAction('另存为')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.save_as_dialog)
        self.menu.addAction(self.save_as_action)

    # 退出
    def quit(self):
        self.menu.addSeparator()
        self.quit_action = QAction('退出')
        self.quit_action.setShortcut(QKeySequence.Quit)
        self.quit_action.triggered.connect(self.close)
        self.menu.addAction(self.quit_action)


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName('文本编辑器')
    window = MainWindow()
    sys.exit(app.exec_())
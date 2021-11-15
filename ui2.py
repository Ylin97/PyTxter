#! /usr/bin/python3
# coding=utf-8


import sys
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QAction, qApp, QTextEdit, QFileDialog, QShortcut, \
    QPlainTextEdit, QMessageBox

# Global variable
file_path = None


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menu = self.menuBar()                  # 创建一个菜单栏
        self.file_menu = self.menu.addMenu('文件')   # 创建文件菜单
        self.help_menu = self.menu.addMenu('帮助')   # 创建帮助菜单
        self.edit_menu = self.menu.addMenu('编辑')   # 创建编辑菜单
        self.text = QPlainTextEdit()                # 定义一个文本编辑器
        self.initUI()

    def initUI(self):
        """初始化主界面"""

        # 初始化主界面
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self.text)

        # 菜单项
        self.create_file_menu()
        self.create_help_menu()
        self.create_edit_menu()

        # 显示
        self.show()

    """---------------文件菜单-------------------
    # DATE: 2021/11/14 Sun
    # Author: Yalin
    # History: Create 'File' menu
    """

    def create_file_menu(self):
        """创建文件菜单"""
        self.open_file()
        self.save()
        self.save_as()
        self.quit()

    # 打开
    def open_file_dialog(self):
        """打开文件会话"""
        global file_path
        path = QFileDialog.getOpenFileName(window, 'open')[0]
        if path:
            self.text.setPlainText(open(path, 'r', encoding='utf-8').read())
            file_path = path

    def open_file(self):
        """打开文件选项"""
        self.open_action = QAction('打开')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()

    # 保存
    def save_dialog(self):
        """保存文件会话"""
        if file_path is None:
            pass
        else:
            with open(file_path, 'w', encoding='utf-8') as fw:
                fw.write(self.text.toPlainText())
            self.text.document().setModified(False)

    def save(self):
        """保存文件选项"""
        self.save_action = QAction('保存')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_dialog)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()

    # 另存为
    def save_as_dialog(self):
        """另存为会话"""
        global file_path
        path = QFileDialog.getSaveFileName(window, '另存为')[0]
        if path:
            file_path = path
            self.save_dialog()

    def save_as(self):
        """另存为选项"""
        self.save_as_action = QAction('另存为')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.save_as_dialog)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()

    # 退出
    def quit(self):
        """退出选项"""
        # self.file_menu.addSeparator()
        self.quit_action = QAction('退出')
        self.quit_action.setShortcut(QKeySequence.Quit)
        self.quit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.quit_action)

    """---------------编辑菜单-------------------
    # DATE: 2021/11/15 Mon
    # Author: Yalin
    # History: Create 'Edit' menu
    """

    def create_edit_menu(self):
        """创建编辑菜单"""
        self.click2format()
        self.chapter_name_format()
        self.clean_space_line()
        self.ban_char_substitute()
        self.punctuation_correct()
        self.convert2utf8()
        self.convert2utf8bom()
        self.find()
        self.replace()

    def click2format_dialog(self):
        """一键格式化会话"""
        print('一键格式化')

    def click2format(self):
        """一键格式化"""
        self.click2format_action = QAction('一键格式化')
        self.click2format_action.triggered.connect(self.click2format_dialog)
        self.edit_menu.addAction(self.click2format_action)
        self.edit_menu.addSeparator()

    def chapter_name_format_dialog(self):
        """章节名格式化会话"""
        print('章节名格式化')

    def chapter_name_format(self):
        """章节名格式化"""
        self.chapter_name_action = QAction("章节名格式化")
        self.chapter_name_action.triggered.connect(self.chapter_name_format_dialog)
        self.edit_menu.addAction(self.chapter_name_action)
        self.edit_menu.addSeparator()

    def clean_space_line_dialog(self):
        """清除空白行会话"""
        print('清除空白行')

    def clean_space_line(self):
        """清除空白行"""
        self.clean_space_line_action = QAction('清除空白行')
        self.clean_space_line_action.triggered.connect(self.clean_space_line_dialog)
        self.edit_menu.addAction(self.clean_space_line_action)
        self.edit_menu.addSeparator()

    def ban_char_substitute_dialog(self):
        """屏蔽字替换会话"""
        print('屏蔽字替换')

    def ban_char_substitute(self):
        """屏蔽字替换"""
        self.ban_char_action = QAction("屏蔽字替换")
        self.ban_char_action.triggered.connect(self.ban_char_substitute_dialog)
        self.edit_menu.addAction(self.ban_char_action)
        self.edit_menu.addSeparator()

    def punctuation_correct_dialog(self):
        """中英标点纠正会话"""
        print('中英标点纠正')

    def punctuation_correct(self):
        """中英标点纠正"""
        self.punc_correct_action = QAction("中英标点纠正")
        self.punc_correct_action.triggered.connect(self.punctuation_correct_dialog)
        self.edit_menu.addAction(self.punc_correct_action)
        self.edit_menu.addSeparator()

    def convert2utf8_dialog(self):
        """转换编码为 utf-8 会话"""
        print('转换编码为 utf-8')

    def convert2utf8(self):
        """转换编码为 utf-8"""
        self.conver2utf8_action = QAction('转换编码为 utf-8')
        self.conver2utf8_action.triggered.connect(self.convert2utf8_dialog)
        self.edit_menu.addAction(self.conver2utf8_action)
        self.edit_menu.addSeparator()

    def convert2utf8bom_dialog(self):
        """转换编码为 utf-8 with BOM 会话"""
        print('转换编码为 utf-8 with bom')

    def convert2utf8bom(self):
        """转换编码为 utf-8 with BOM"""
        self.convert2utf8bom_action = QAction("转换编码为 utf-8 with bom")
        self.convert2utf8bom_action.triggered.connect(self.convert2utf8bom_dialog)
        self.edit_menu.addAction(self.convert2utf8bom_action)
        self.edit_menu.addSeparator()

    def find_dialog(self):
        """查找会话"""
        print('查找')

    def find(self):
        """查找"""
        self.find_action = QAction('查找')
        self.find_action.triggered.connect(self.find_dialog)
        self.edit_menu.addAction(self.find_action)
        self.edit_menu.addSeparator()

    def replace_dialog(self):
        print('替换')

    def replace(self):
        """替换"""
        self.replace_action = QAction('替换')
        self.replace_action.triggered.connect(self.replace_dialog)
        self.edit_menu.addAction(self.replace_action)

    """
    # ----------------帮助菜单-------------------
    # DATE: 2021/11/15 Mon 
    # Author: Yalin
    # History: Create 'Help' menu
    """

    def create_help_menu(self):
        """创建帮助菜单"""
        self.about()

    def about_dialog(self):
        """关于会话"""
        about_text = "<center>这是一个txt小说编辑器</center><p>版本：0.01 beta</p>"
        QMessageBox.about(window, '说明', about_text)

    def about(self):
        """关于选项"""
        self.about_action = QAction('关于')
        self.about_action.triggered.connect(self.about_dialog)
        self.help_menu.addAction(self.about_action)


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName('文本编辑器')
    window = MainWindow()
    sys.exit(app.exec_())
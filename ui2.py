##! /usr/bin/python3
# coding=utf-8


import sys
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog,\
    QPlainTextEdit, QMessageBox
from tools import *
from format import *

# Global variable
file_path = '.\\未命名文件.txt'
file_name = '未命名文件.txt'
file_codec = 'utf-8'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menu = self.menuBar()                  # 创建一个菜单栏
        self.file_menu = self.menu.addMenu('文件')   # 创建文件菜单
        self.edit_menu = self.menu.addMenu('编辑')   # 创建编辑菜单
        self.help_menu = self.menu.addMenu('帮助')   # 创建帮助菜单
        self.text_formatted = ''                    # 格式化之后的字符串
        self.initUI()

    def closeEvent(self, a0) -> None:
        """关闭事件"""
        if not self.text.document().isModified():
            return
        answer = QMessageBox.question(self, '退出程序', '关闭之前是否保存文件',
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                                      )
        # print(answer)
        if answer & QMessageBox.Save:
            self.save_dialog()
        elif answer & QMessageBox.Cancel:
            a0.ignore()

    # def quitEvent(self, ):

    def initUI(self):
        """初始化主界面"""

        # 初始化主界面
        self.setMinimumSize(800, 600)
        self.text = QPlainTextEdit()   # 定义一个文本编辑器
        self.setCentralWidget(self.text)
        self.setWindowTitle('未命名文件.txt')
        self.statusBar().showMessage(f'新建文件 - {file_name}', 5000)

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
        self.file_new()
        self.open_file()
        self.save()
        self.save_as()
        self.save2utf8()
        self.save2utf8bom()
        self.quit()

    def file_new_dialog(self):
        """新建文件会话"""
        # print('新建文件')
        global file_path
        global file_name

        # print(str(self.text).strip())
        if file_name == '未命名文件.txt' and self.text.toPlainText().strip():
            self.save_as_dialog()
        elif file_name != '未命名文件.txt':
            self.save_dialog(dialog=True)
        self.text.clear()
        file_name = '未命名文件.txt'
        file_path = '.\\未命名文件.txt'
        self.setWindowTitle(file_name)
        self.statusBar().showMessage(f'新建文件 - {file_name}', 5000)

    def file_new(self):
        """新建文件选项"""
        self.new_action = QAction('新建')
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.triggered.connect(self.file_new_dialog)
        self.file_menu.addAction(self.new_action)
        self.file_menu.addSeparator()

    def open_file_dialog(self):
        """打开文件会话"""
        global file_path
        global file_name
        global file_codec
        path = QFileDialog.getOpenFileName(self, 'open')[0]
        file_name = str(path).split('\\')[-1]
        # print(file_name)
        if path:
            file_codec = detect_encoding(path)[0]
            with open(path, 'r', encoding=file_codec) as fr:
                text = fr.read()
            self.text.setPlainText(text)
            # self.text.document().setModified(False)
            self.setWindowTitle(file_name)
            file_path = path
            self.statusBar().showMessage(f'打开文件 - {file_name}\t编码：{file_codec}')

    def open_file(self):
        """打开文件选项"""
        self.open_action = QAction('打开')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()

    # 保存
    def save_dialog(self, dialog=False):
        """保存文件会话"""
        # if file_path is None or not self.text.document().isModified():
        if dialog:  # 是否弹出关闭文件前保存对话框
            if not self.text.document().isModified():
                return
            answer = QMessageBox.question(self, '关闭文件', '关闭之前是否保存文件？',
                                          QMessageBox.Yes | QMessageBox.No)
            # print(answer)
            if answer & QMessageBox.Save:
                self.save_dialog()

        if not self.text.document().isModified():
            print('文件未修改，不需要保存！')
            pass
        else:
            with open(file_path, 'w', encoding=file_codec) as fw:
                fw.write(self.text.toPlainText())
            self.text.document().setModified(False)
            print(f'文件: {file_path}\t保存成功！')
            self.statusBar().showMessage(f'文件: {file_name}\t保存成功！', 5000)
            self.statusBar().showMessage(f'打开文件 - {file_name}\t编码：{file_codec}')

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
        path = QFileDialog.getSaveFileName(self, '另存为')[0]
        if path:
            file_path = path
            self.save_dialog()
            self.statusBar().showMessage('另存文件为')

    def save_as(self):
        """另存为选项"""
        self.save_as_action = QAction('另存为')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.save_as_dialog)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()

    def save2utf8_dialog(self):
        """以 utf-8 编码保存会话"""
        print('以 utf-8 编码保存')

    def save2utf8(self):
        """以 utf-8 编码保存"""
        self.save2utf8_action = QAction('以 utf-8 编码保存')
        self.save2utf8_action.triggered.connect(self.save2utf8_dialog)
        self.file_menu.addAction(self.save2utf8_action)
        self.file_menu.addSeparator()

    def save2utf8bom_dialog(self):
        """以 utf-8 with BOM 编码保存会话"""
        print('以 utf-8 with BOM 编码保存会话')

    def save2utf8bom(self):
        """以 utf-8 with BOM 编码保存"""
        self.save2utf8bom_action = QAction("以 utf-8 with bom 编码保存")
        self.save2utf8bom_action.triggered.connect(self.save2utf8bom_dialog)
        self.file_menu.addAction(self.save2utf8bom_action)
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
        self.find()
        self.replace()

    def click2format_dialog(self):
        """一键格式化会话"""
        print('一键格式化')
        file_to_utf8(file_path)
        remove_extra_line_break(file_path)
        with open(file_path, 'r', encoding='utf-8') as fr:
            text = fr.read()
        self.text.setPlainText(text)
        # self.text.document().setModified(False)
        self.setWindowTitle(file_name)
        self.statusBar().showMessage(f'打开文件 - {file_name}\t编码：utf-8')

    def click2format(self):
        """一键格式化"""
        self.click2format_action = QAction('一键格式化')
        self.click2format_action.triggered.connect(self.click2format_dialog)
        self.edit_menu.addAction(self.click2format_action)
        self.edit_menu.addSeparator()

    def chapter_name_format_dialog(self):
        """章节名格式化会话"""
        # print('章节名格式化')
        # print(self.text.toPlainText().split('\n'))
        lines = [line + '\n' for line in self.text.toPlainText().split('\n')]
        lines = chapter_name_normalize(lines)
        # print(lines)
        text = ''
        for line in lines:
            if line:
                text += line
        self.text.setPlainText(text)

    def chapter_name_format(self):
        """章节名格式化"""
        self.chapter_name_action = QAction("章节名格式化")
        self.chapter_name_action.triggered.connect(self.chapter_name_format_dialog)
        self.edit_menu.addAction(self.chapter_name_action)
        self.edit_menu.addSeparator()

    def clean_space_line_dialog(self):
        """清除空白行会话"""
        print('清除空白行')
        lines = clean_line(line + '\n' for line in self.text.toPlainText().split('\n'))
        text = ''
        for line in lines:
            text += line
        self.text.setPlainText(text)
        self.statusBar().showMessage('清除空白行成功！', 5000)

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
        self.text.setPlainText(sub_punctuation(self.text.toPlainText()))

    def punctuation_correct(self):
        """中英标点纠正"""
        self.punc_correct_action = QAction("中英标点纠正")
        self.punc_correct_action.triggered.connect(self.punctuation_correct_dialog)
        self.edit_menu.addAction(self.punc_correct_action)
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
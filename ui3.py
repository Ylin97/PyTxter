##! /usr/bin/python3
# coding=utf-8


import sys
import copy
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog,\
    QPlainTextEdit, QMessageBox
from tools import *
from format import *

# Global variable
# file_path = '.\\未命名文件.txt'
# file_name = '未命名文件.txt'
# file_codec = 'utf-8'
# is_modified = False


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.text_origin = ''                         # 文件原始内容
        self.file_path = './Untitled.txt'
        self.file_name = 'Untitled.txt'
        self.file_codec = 'utf-8'
        self.is_modified = False
        self.initUI()

    def closeEvent(self, a0) -> None:
        """关闭事件"""
        if self.file_name == 'Untitled.txt' and self.text.toPlainText().isspace():
            return
        if not self.is_modified:
            return
        answer = QMessageBox.question(self, '退出程序', '文件已修改，退出程序前是否保存文件？',
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                                      )
        # print(answer)
        if answer & QMessageBox.Save:
            self.save_triggered()
        elif answer & QMessageBox.Cancel:
            a0.ignore()

    def initUI(self):
        """初始化主界面"""

        # 初始化主界面
        self.setMinimumSize(1000, 800)
        self.text = QPlainTextEdit()   # 定义一个文本编辑器
        self.setCentralWidget(self.text)
        self.setWindowTitle('Untitled.txt')
        self.statusBar().showMessage(f'New - {self.file_name}', 2000)
        self.show_statusbar_msg()
        self.text.textChanged.connect(self.text_changed)  # 实时监控编辑区内容是否发生更改

        # 菜单项
        self.create_file_menu()
        self.create_edit_menu()
        self.create_help_menu()

        # 显示
        self.show()

    """---------------文件菜单-------------------
    # DATE: 2021/11/14 Sun
    # Author: Yalin
    # History: Create 'File' menu
    """

    def create_file_menu(self):
        """创建文件菜单"""
        menu = self.menuBar().addMenu("文件(&F)")

        new_file         = menu.addAction("新建(&N)", self.new_file_triggered)
        open_file        = menu.addAction("打开(&O)", self.open_file_triggered)
        save_file        = menu.addAction("保存(&S)", self.save_triggered)
        save_fileas      = menu.addAction("另存为(&A)...", self.save_as_triggered)
        save2utf8        = menu.addAction("以utf-8编码保存", self.save2utf8_triggered)
        save2utf8bom     = menu.addAction("以utf-8 with BOM保存", self.save2utf8bom_triggered)
        exit_file        = menu.addAction("退出(&X)", self.close)

        # 绑定快捷键
        new_file. setShortcut("Ctrl+N")
        open_file.setShortcut("Ctrl+O")
        save_file.setShortcut("Ctrl+S")
        save_fileas.setShortcut("Ctrl+Shift+S")
        exit_file.setShortcut(QKeySequence.Quit)

    def new_file_triggered(self):
        """新建文件"""
        # print('新建文件')
        # if self.file_name == 'Untitled.txt' and self.is_modified:
        #     self.save_as_triggered()
        if self.file_name == 'Untitled.txt' and self.is_modified\
            or self.file_name != 'Untitled.txt':
            self.save_triggered(dialog=True)
        self.text.clear()
        self.file_name = 'Untitled.txt'
        self.file_path = './Untitled.txt'
        self.text_origin = ''
        self.setWindowTitle(self.file_name)
        # self.text.document().setModified(False)
        self.is_modified = False
        self.statusBar().showMessage(f'新建文件 - {self.file_name}', 2000)
        self.show_statusbar_msg()

    def open_file_triggered(self):
        """打开文件"""
        if self.is_modified:
            self.save_triggered(dialog=True)
        path = QFileDialog.getOpenFileName(self, '打开文件')[0]
        self.file_name = str(path).split('/')[-1]
        # print(file_name)
        if path:
            self.file_codec = detect_encoding(path)[0]
            with open(path, 'r', encoding=self.file_codec) as fr:
                text = fr.read()
            self.text.setPlainText(text)
            self.text_origin = copy.copy(text)   # 保存文件原始内容副本
            # self.text.document().setModified(False)
            self.is_modified = False
            self.setWindowTitle(self.file_name)
            self.file_path = path
            self.show_statusbar_msg()

    def save_triggered(self, dialog=False):
        """保存文件"""
        # if file_path is None or not self.text.document().isModified():
        if dialog:  # 是否弹出关闭文件前保存对话框
            if not self.is_modified:
                return
            answer = QMessageBox.question(self, '关闭文件', '文件已修改，关闭前是否保存文件？',
                                          QMessageBox.Yes | QMessageBox.No)
            # print(answer)
            if answer & QMessageBox.Save:
                self.save_triggered()
            else:
                # self.text.document().setModified(False)
                self.is_modified = False
                return

        if not self.is_modified:
            # print('文件未修改，不需要保存！')
            self.statusBar().showMessage("文件未修改，不需要保存！", 2000)
        else:
            with open(self.file_path, 'w', encoding=self.file_codec) as fw:
                fw.write(self.text.toPlainText())
            # self.text.document().setModified(False)
            self.is_modified = False
            # print(f'文件: {self.file_path}\t保存成功！')
            self.setWindowTitle(self.file_name)
            msg1 = f'文件: {self.file_name}\t保存成功！'
            self.statusBar().showMessage(msg1, 2000)
            self.show_statusbar_msg()

    def save_as_triggered(self):
        """另存为"""
        path = QFileDialog.getSaveFileName(self, '另存为')[0]
        if path:
            with open(path, 'w', encoding='utf-8') as fw:
                fw.write(self.text.toPlainText())
                # self.text.document().setModified(False)
                # self.is_modified = False
                # print(f'文件: {self.file_path}\t另存成功！')
                # self.setWindowTitle(self.file_name)
                msg1 = f'文件: {self.file_name}\t另存成功！'
                self.statusBar().showMessage(msg1, 2000)
                self.show_statusbar_msg()

    def save2utf8_triggered(self):
        """以 utf-8 编码保存会话"""
        # print('以 utf-8 编码保存')
        with open(self.file_path, 'w', encoding='utf-8') as fw:
            fw.write(self.text.toPlainText())
            # self.text.document().setModified(False)
            # self.is_modified = False
            # print(f'文件: {self.file_path}\t以 utf-8 编码保存成功！')
            self.setWindowTitle(self.file_name)
            msg1 = f'文件: {self.file_name}\t以 utf-8 编码保存成功！'
            self.statusBar().showMessage(msg1, 2000)
            self.show_statusbar_msg()

    def save2utf8bom_triggered(self):
        """以 utf-8 with BOM 编码保存会话"""
        # print('以 utf-8 with BOM 编码保存会话')
        with open(self.file_path, 'w', encoding='utf-8-sig') as fw:
            fw.write(self.text.toPlainText())
            # self.text.document().setModified(False)
            # self.is_modified = False
            # print(f'文件: {self.file_path}\t以 utf-8 with BOM 编码保存成功！')
            self.setWindowTitle(self.file_name)
            msg1 = f'文件: {self.file_name}\t以 utf-8 with BOM 编码保存成功！'
            self.statusBar().showMessage(msg1, 2000)
            self.show_statusbar_msg()

    """---------------编辑菜单-------------------
    # DATE: 2021/11/15 Mon
    # Author: Yalin
    # History: Create 'Edit' menu
    """

    def create_edit_menu(self):
        """创建编辑菜单"""
        menu = self.menuBar().addMenu("编辑(&E)")

        click2format        = menu.addAction("一键格式化(&G)", self.click2format_triggered)
        chapter_name_format = menu.addAction("章节名格式化", self.chapter_name_format_triggered)
        clean_null_line     = menu.addAction("清除空白行", self.clean_null_line_triggered)
        ban_char_replace    = menu.addAction("屏蔽字替换", self.ban_char_replace_triggered)
        punc_replace        = menu.addAction("中英标点纠正", self.punctuation_correct_triggered)
        menu.addSeparator() 
        revokeEdit          = menu.addAction("撤销(&U)", self.revoke_triggered)
        recoveryEdit        = menu.addAction("恢复(&R)", self.recovery_triggered)
        cutEdit             = menu.addAction("剪切(&T)", self.cut_triggered)
        copyEdit            = menu.addAction("复制(&C)", self.copy_triggered)
        pasteEdit           = menu.addAction("粘贴(&P)", self.paste_triggered)
        menu.addSeparator()
        findEdit            = menu.addAction("查找(&F)", self.find_triggered)
        findNextEdit        = menu.addAction("查找下一个(&N)")
        replaceEdit         = menu.addAction("替换(&E)...")
        # gotoEdit            = menu.addAction("转到(&D)...")
        menu.addSeparator()
        checkAllEdit        = menu.addAction("全选(&A)")
        clean               = menu.addAction("清空编辑区(&L)", self.clean_triggered)
        recovery2origin     = menu.addAction("还原文件内容", self.recovery2origin)

        click2format.setShortcut("Ctrl+G")
        revokeEdit.setShortcut("Ctrl+Z") #设置快捷键
        recoveryEdit.setShortcut("Ctrl+Shift+Z")
        cutEdit.setShortcut("Ctrl+X")
        copyEdit.setShortcut("Ctrl+C")
        pasteEdit.setShortcut("Ctrl+V")
        clean.setShortcut("Ctrl+L")
        findEdit.setShortcut("Ctrl+F")
        findNextEdit.setShortcut("F3")
        replaceEdit.setShortcut("Ctrl+H")
        # gotoEdit.setShortcut("Ctrl+G")
        checkAllEdit.setShortcut("Ctrl+A")

    def click2format_triggered(self):
        """一键格式化会话"""
        text = auto_format(self.get_lines())
        self.text.setPlainText(text)
        # self.text.document().setModified(False)
        # self.setWindowTitle(self.file_name)
        self.show_statusbar_msg()
        self.is_modified = True

    def chapter_name_format_triggered(self):
        """章节名格式化"""
        # print('章节名格式化')
        lines = chapter_name_normalize(self.get_lines())
        # print(lines)
        text = ''
        for line in lines:
            if line:
                text += line
        self.text.setPlainText(text)
        self.statusBar().showMessage("格式化章节名成功！", 2000)
        self.show_statusbar_msg()
        self.is_modified = True

    def clean_null_line_triggered(self):
        """清除空白行"""
        # print('清除空白行')
        lines = clean_line(self.get_lines())
        text = ''
        for line in lines:
            text += line
        self.text.setPlainText(text)
        # self.text.document().setModified(True)
        self.statusBar().showMessage('清除空白行成功！', 2000)
        self.show_statusbar_msg()
        self.is_modified = True

    def ban_char_replace_triggered(self):
        """屏蔽字替换会话"""
        print('屏蔽字替换')

    def punctuation_correct_triggered(self):
        """中英标点纠正会话"""
        # print('中英标点纠正')
        lines = correct_punctuation(self.get_lines())
        text = ''
        for line in lines:
            text += line
        self.text.setPlainText(text)
        self.statusBar().showMessage('标点纠正成功！', 2000)
        self.show_statusbar_msg()
        self.is_modified = True

    def find_triggered(self):
        """查找会话"""
        print('查找')

    def replace_triggered(self):
        """替换"""
        print('替换')

    def revoke_triggered(self):
        """撤销"""
        self.text.undo()

    def recovery_triggered(self):
        """恢复"""
        self.text.redo()

    def cut_triggered(self):
        """剪切"""
        self.text.cut()

    def copy_triggered(self):
        """复制"""
        self.text.copy()

    def paste_triggered(self):
        """粘贴"""
        self.text.paste()

    def clean_triggered(self):
        """清空编辑区"""
        self.text.clear()

    def recovery2origin(self):
        """还原编辑区到初始态"""
        self.text.setPlainText(self.text_origin)
        self.statusBar().showMessage(f'还原成功！', 2000)
        self.setWindowTitle(f'{self.file_name}')
        self.show_statusbar_msg()
        self.is_modified = False

    """
    # ----------------帮助菜单-------------------
    # DATE: 2021/11/15 Mon 
    # Author: Yalin
    # History: Create 'Help' menu
    """

    def create_help_menu(self):
        """创建帮助菜单"""
        # self.about()
        menu = self.menuBar().addMenu("帮助(&H)")
        menu.addAction("关于", self.about_triggered)

    def about_triggered(self):
        """关于会话"""
        about_text = "<center>这是一个txt小说编辑器</center><p>版本：0.01 beta</p>"
        QMessageBox.about(window, '说明', about_text)

    """--------------辅助方法-------------------
    # DATE: 2021/11/25
    # Author: yalin
    # History: add show_statusbar_msg function
    """
    def text_changed(self):
        """如果编辑区内容发生更改，则标题栏显示*号"""
        self.setWindowTitle('*' + self.file_name)
        self.is_modified = True

    def get_lines(self) ->list:
        """拆分行"""
        return [line + '\n' for line in self.text.toPlainText().split('\n')]

    def show_statusbar_msg(self):
        """状态栏常留信息"""
        msg2 = f'打开文件 - {self.file_path}\t编码：{self.file_codec}'
        self.statusBar().showMessage(msg2)


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName('文本编辑器')
    window = MainWindow()
    sys.exit(app.exec_())
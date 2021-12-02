##! /usr/bin/python3
# coding=utf-8


import os
import sys
import copy
import ctypes
import configparser

from PyQt5.QtCore import Qt, QRect, QSize, QTextCodec
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QFont, QPainter, QTextCursor, QTextFormat
from PyQt5.QtWidgets import QApplication, QBoxLayout, QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,\
    QPlainTextEdit, QMessageBox, QFontDialog, QPushButton, QAction, QFileDialog, QSplitter, QTextEdit, QVBoxLayout, QWidget
# from tools import *
from qcodeeditor import QCodeEditor
from format import *
from chapter_tree import TOC


# 常量
CONFIG_FILE_PATH = "notepad.ini"

# Global variable
# file_path = '.\\未命名文件.txt'
# file_name = '未命名文件.txt'
# file_codec = 'utf-8'
# is_modified = False

# 解决任务栏图标问题
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("notepad")
# QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf-8"))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.text_origin = ''                         # 文件原始内容
        self.last_search = ''
        self.last_goto = 1
        self.file_path = './Untitled.txt'
        self.file_name = 'Untitled.txt'
        self.file_codec = 'utf-8'
        self.chapter_names = {}
        self.is_modified = False
        self.initUI()

    def initUI(self):
        """初始化主界面"""

        # 初始化主界面
        # self.text = QPlainTextEdit()             # 定义一个文本编辑器
        self.text = QCodeEditor()                  # 定义一个编辑器
        self.toc = TOC(self)   # 定义一个侧边栏
        # self.setFixedSize

        mainlayout = QHBoxLayout()            # 定义水平Box布局
        # mainlayout.addWidget(self.toc)
        # mainlayout.addWidget(self.text)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.toc)
        splitter.addWidget(self.text)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        mainlayout.addWidget(splitter)

        mainwidget = QWidget()
        mainwidget.setLayout(mainlayout)

        # self.setCentralWidget(self.text)
        self.setCentralWidget(mainwidget)
        # self.setCentralWidget(QWidget().setLayout(mainlayout))
        # 载入配置信息
        self.config = Config(self, self.text)
        # self.font_cfg = MyFont()
        self.config.judge_config()
        self.config.read_settings()

        # self.setMinimumSize(1000, 800)
        # self.font = QFont()
        # self.text.setFont(self.font)
        self.setWindowTitle('Untitled.txt')
        self.setWindowIcon(QIcon('icons/notepad.png'))
        self.show_statusbar_msg()

        # 菜单项
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.create_help_menu()

        # 工具栏
        self.create_toolbar()
        # 搜索相关项
        self.search_content = ''
        self.search_key = None
        self.search_count = 0
        self.search_current = 0

        # 信号绑定
        self.text.textChanged.connect(self.text_changed)  # 实时监控编辑区内容是否发生更改
        self.text.textChanged.connect(self.find_enable) 
        self.text.textChanged.connect(self.reset_search_content)

        # 显示
        self.show()

    def closeEvent(self, a0) -> None:
        """关闭事件"""
        if self.file_name == 'Untitled.txt' and self.text.toPlainText().isspace():
            self.config.write_setting()
            return
        if not self.is_modified:
            self.config.write_setting()
            return
        answer = QMessageBox.question(self, '退出程序', '文件已修改，退出程序前是否保存文件？',
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                                      )
        # print(answer)
        if answer & QMessageBox.Save:
            self.save_triggered()
        elif answer & QMessageBox.Cancel:
            a0.ignore()
        # 写入配置文件
        self.config.write_setting()

    """---------------文件菜单-------------------
    # DATE: 2021/11/14 Sun
    # Author: Yalin
    # History: Create 'File' menu
    """

    def create_file_menu(self):
        """创建文件菜单"""
        menu = self.menuBar().addMenu("文件(&F)")

        self.new_act     = menu.addAction("新建(&N)", self.new_file_triggered)
        self.open_act    = menu.addAction("打开(&O)", self.open_file_triggered)
        self.save_act    = menu.addAction("保存(&S)", self.save_triggered)
        self.saveas_act  = menu.addAction("另存为(&A)...", self.save_as_triggered)
        save2utf8        = menu.addAction("以utf-8编码保存", self.save2utf8_triggered)
        save2utf8bom     = menu.addAction("以utf-8 with BOM保存", self.save2utf8bom_triggered)
        exit_file        = menu.addAction("退出(&X)", self.close)

        # 绑定快捷键
        self.new_act. setShortcut("Ctrl+N")
        self.open_act.setShortcut("Ctrl+O")
        self.save_act.setShortcut("Ctrl+S")
        self.saveas_act.setShortcut("Ctrl+Shift+S")
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
            self.chapter_names = get_all_chapter_name(self.get_lines())
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

        self.click2format_act = menu.addAction("一键格式化(&G)", self.click2format_triggered)
        self.chapter_name_act = menu.addAction("章节名格式化", self.chapter_name_format_triggered)
        self.clean_line_act   = menu.addAction("清除空白行", self.clean_null_line_triggered)
        ban_char_act          = menu.addAction("屏蔽字替换", self.ban_char_replace_triggered)
        self.punc_replace_act = menu.addAction("中英标点纠正", self.punctuation_correct_triggered)
        menu.addSeparator() 
        self.undo_act       = menu.addAction("撤销(&U)", self.text.undo)
        self.redo_act     = menu.addAction("恢复(&R)", self.text.redo)
        self.cut_act          = menu.addAction("剪切(&T)", self.text.cut)
        self.copy_act         = menu.addAction("复制(&C)", self.text.copy)
        self.paste_act        = menu.addAction("粘贴(&P)", self.text.paste)
        menu.addSeparator()
        self.find_act         = menu.addAction("查找(&F)", self.find_triggered)
        self.find_next_act    = menu.addAction("查找下一个(&N)")
        replace_act           = menu.addAction("替换(&E)", self.replace_triggered)
        goto_act              = menu.addAction("转到(&D)...", self.goto)
        menu.addSeparator()
        check_all_act         = menu.addAction("全选(&A)", self.text.selectAll)
        self.clean_act        = menu.addAction("清空编辑区(&L)", self.text.clear)
        self.re2origin_act    = menu.addAction("还原文件内容", self.recovery2origin)

        # 动作属性设置
        self.find_act.setEnabled(False)  # 暂时将find、findnex设置为无效，有效时再激活
        self.find_next_act.setEnabled(False)

        # 绑定快捷键
        self.click2format_act.setShortcut("Ctrl+G")
        self.undo_act.setShortcut("Ctrl+Z") #设置快捷键
        self.redo_act.setShortcut("Ctrl+Shift+Z")
        self.cut_act.setShortcut("Ctrl+X")
        self.copy_act.setShortcut("Ctrl+C")
        self.paste_act.setShortcut("Ctrl+V")
        self.clean_act.setShortcut("Ctrl+L")
        self.find_act.setShortcut("Ctrl+F")
        self.find_next_act.setShortcut("F3")
        replace_act.setShortcut("Ctrl+H")
        # gotoEdit.setShortcut("Ctrl+G")
        check_all_act.setShortcut("Ctrl+A")

    def click2format_triggered(self):
        """一键格式化会话"""
        text = auto_format(self.get_lines())
        # self.text.clear()
        # self.text.setPlainText(text)
        self.update_edit_content(text)
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
        # self.text.setPlainText(text)
        self.update_edit_content(text)
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
        # self.text.setPlainText(text)
        self.update_edit_content(text)
        # self.text.document().setModified(True)
        self.statusBar().showMessage('清除空白行成功！', 2000)
        self.show_statusbar_msg()
        self.is_modified = True

    def ban_char_replace_triggered(self):
        """屏蔽字替换会话"""
        # print('屏蔽字替换')
        #TODO:计划使用阅读的净化规则
        QMessageBox.information(self, '提示', '此功能还未能实现╮(╯▽╰)╭', QMessageBox.Ok)

    def punctuation_correct_triggered(self):
        """中英标点纠正会话"""
        # print('中英标点纠正')
        lines = correct_punctuation(self.get_lines())
        text = ''
        for line in lines:
            text += line
        # self.text.setPlainText(text)
        self.update_edit_content(text)
        self.statusBar().showMessage('标点纠正成功！', 2000)
        self.show_statusbar_msg()
        self.is_modified = True

    def find_triggered(self):
        """查找字符串"""
        self.find_dialog = QDialog(self)
        self.find_dialog.setWindowTitle('查找')
        search_label = QLabel('查找：')
        self.search_qle = QLineEdit(self.last_search)
        search_label.setBuddy(self.search_qle)
        self.search_btn = QPushButton('查找下一个')
        self.search_btn.setDefault(True)

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(search_label)
        layout.addWidget(self.search_qle)
        layout.addWidget(self.search_btn)

        self.search_btn.clicked.connect(self.search_triggered)
        self.find_dialog.setLayout(layout)
        self.find_dialog.show()

    def find_enable(self):
        # 当textEdit不为空时，findAction才生效
        if self.text.toPlainText():
            self.find_act.setEnabled(True)
        else:
            self.find_act.setEnabled(False)
            self.find_next_act.setEnabled(False)

    def reset_search_content(self):
        """改变待搜索内容"""
        self.search_content = None
        self.search_count = 0
        self.search_current = 0

    def select(self, start, length):
        """选中文字,高亮显示"""
        cur = QTextCursor(self.text.textCursor())
        cur.setPosition(start)
        cur.setPosition(start + length, QTextCursor.KeepAnchor)
        self.text.setTextCursor(cur)

    def search_triggered(self, key_word = None):
        """查找字符串
        Args:
            key_word: 将要搜索的关键字
        Return:
            start: 要替换字符串的在编辑区文本中的开始位置，
                   -1 表示未找到， -2 表示为输入关键字
        """
        # print('查找')
        start = -1
        if not key_word:
            key_word = self.search_qle.text()
            if len(key_word) == 0:  # 没有输入查找关键字
                QMessageBox.warning(self, '警告', '请输入查找关键字！', QMessageBox.Ok)
                return -2
        if key_word != self.search_key:
            self.search_key = key_word
            self.search_count = 0
            self.search_current = 0
        if not self.search_content:
            self.search_content = self.text.toPlainText()
        if not self.search_count:  # 第一次查找
            self.search_count = self.search_content.count(key_word) 
            if self.search_count != 0:
                start = self.search_content.index(key_word)
                self.select(start, len(key_word))
                self.search_current += 1
            else:
                QMessageBox.warning(self, '查找', '未找到内容！', QMessageBox.Ok)
        else:
            if self.search_current < self.search_count:
                start = self.search_content.find(key_word, self.text.textCursor().position())
                if start != -1:
                    self.select(start, len(key_word))
                    self.search_current += 1
            else:
                answer = QMessageBox.question(self, '查找', '已到达文件结尾，是否从头开始查找？',
                                          QMessageBox.Yes | QMessageBox.No)
                if answer & QMessageBox.Yes:
                    self.search_count = 0
                    self.search_current = 0
                    self.search_triggered()
        self.text.setFocus()
        self.statusBar().showMessage("匹配[{}/{}]".format(self.search_current, self.search_count))
        return start

    def replace_triggered(self):
        """替换"""
        # print('替换')
        self.replace_dialog = QDialog(self)
        self.replace_dialog.setWindowTitle('替换')
        search_label = QLabel('查找内容：')
        self.search_qle = QLineEdit()
        search_label.setBuddy(self.search_qle)
        replace_label = QLabel('替换为：')
        # 默认替换为空格
        self.replace_content = QLineEdit()
        replace_label.setBuddy(self.replace_content)
        self.find_button = QPushButton('查找下一个')
        self.replace_button = QPushButton('替换')
        self.replace_all_button = QPushButton('全部替换')

        self.replace_button.setEnabled(False)
        self.replace_all_button.setEnabled(False)

        self.find_button.clicked.connect(self.replace_text)
        self.replace_button.clicked.connect(self.replace_text)
        self.replace_all_button.clicked.connect(self.replace_all)
        self.search_qle.textChanged.connect(self.replace_enable)

        layout = QGridLayout()
        layout.addWidget(search_label, 0, 0)
        layout.addWidget(self.search_qle, 0, 1)
        layout.addWidget(self.find_button, 0, 2)
        layout.addWidget(replace_label, 1, 0)
        layout.addWidget(self.replace_content, 1, 1)
        layout.addWidget(self.replace_button, 1, 2)
        layout.addWidget(self.replace_all_button, 2, 2)
        self.replace_dialog.setLayout(layout)
        self.replace_dialog.show()

    def replace_enable(self):
        if not self.search_qle.text():
            self.replace_button.setEnabled(False)
            self.replace_all_button.setEnabled(False)
        else:
            self.replace_button.setEnabled(True)
            self.replace_all_button.setEnabled(True)

    def replace_text(self):
        cursor = self.text.textCursor()
        start = cursor.anchor()
        text = self.search_qle.text()
        text_len = len(text)
        context = self.text.toPlainText()
        # index = context.find(text, start)
        index = self.search_triggered(text)
        sender = self.sender()
        # 如果sender是替换按钮，替换选中文字
        if sender is self.replace_button:
            if text == cursor.selectedText():
                position = cursor.anchor()
                cursor.removeSelectedText()
                replace_text = self.replace_content.text()
                cursor.insertText(replace_text)
                # 替换文字后要重新搜索，这个时候cursor还未修改
                self.replace_text()
                return
        if -1 == index:
            QMessageBox.information(
                self.replace_dialog, '记事本', '找不到\"%s\"' % text)
        else:
            start = index
            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start + text_len)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, text_len)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

    def replace_all(self):
        context = self.text.toPlainText()
        search_word = self.search_qle.text()
        replace_word = self.replace_content.text()
        new_context = context.replace(search_word, replace_word)
        doc = self.text.document()
        curs = QTextCursor(doc)
        # 选择整个文档
        curs.select(QTextCursor.Document)
        # curs.removeSelectedText()
        curs.insertText(new_context)

    def goto(self):
        """跳转到指定行"""
        #TODO:参考 test/test007.py
        goto_dialog = QDialog(self)
        goto_dialog.setWindowTitle('跳转')

        goto_label = QLabel('跳转:')
        self.goto_qle = QLineEdit(str(self.last_goto))
        goto_label.setBuddy(self.goto_qle)
        self.goto_btn = QPushButton('确定')
        self.goto_btn.setDefault(True)
        self.goto_btn.clicked.connect(self.goto_confirm_triggered)

        goto_layout = QBoxLayout(QBoxLayout.LeftToRight)
        goto_layout.addWidget(goto_label)
        goto_layout.addWidget(self.goto_qle)
        goto_layout.addWidget(self.goto_btn)
        
        goto_dialog.setLayout(goto_layout)
        goto_dialog.show()
        
    def goto_confirm_triggered(self, text=None):
        """跳转行确定"""
        # print('goto line')
        if not text:
            text = self.goto_qle.text()
        try:
            n = int(text)
        except ValueError:
            print("Cannot convert '{}' to integer number".format(text))
        else:
            if n < 1:
                print("The number must be greater than 1")
                return
            doc = self.text.document()
            self.text.setFocus()
            if n > doc.blockCount():
            #     self.text.insertPlainText("\n" * (n - doc.blockCount()))
                cursor = QTextCursor(doc.findBlockByNumber(doc.blockCount() - 1))
            else:
            # cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
                cursor = QTextCursor(doc.findBlockByNumber(n - 1))
            self.text.setTextCursor(cursor)

    def recovery2origin(self):
        """还原编辑区到初始态"""
        self.text.setPlainText(self.text_origin)
        self.statusBar().showMessage(f'还原成功！', 2000)
        self.setWindowTitle(f'{self.file_name}')
        self.show_statusbar_msg()
        self.is_modified = False

    """----------------格式菜单-------------------
    # DATE: 2021/11/25
    # Author: yalin
    # History: add format_menu
    """
    def create_format_menu(self):
        """创建格式菜单"""
        menu = self.menuBar().addMenu("格式(&O)")

        font           = menu.addAction("字体(&F)", self.font_select_triggered)
        self.word_wrap = menu.addAction("自动换行(&W)", self.format_wrap_triggered)

        # 设置是否可勾选
        self.word_wrap.setCheckable(True)
        self.word_wrap.setChecked(True)
    
    def font_select_triggered(self):
        font, ok = QFontDialog.getFont(self.text.font(), self, '字体')
        if ok:
            # self.font = font
            self.text.setFont(font)
        self.show_statusbar_msg()
    
    def format_wrap_triggered(self):
        if self.word_wrap.isChecked():
            self.text.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.show_statusbar_msg()

    """----------------帮助菜单-------------------
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
        about_text = """
                    <h2 align="center">这是一个txt小说编辑器</h2><center>版本：0.01 beta</center>
                    <p>by yalin <a href="https://github.com/Ylin97/txtbook-editor">https://github.com/Ylin97/txtbook-editor</a></p>
                    <h3>感谢以下作者：</h3>
                    <p>likui911: <a href="https://github.com/likui911/notepad_pyqt5">https://github.com/likui911/notepad_pyqt5</a></p>
                    <p>Aloe_n: <a href="https://www.cnblogs.com/aloe-n/p/8175757.html">https://www.cnblogs.com/aloe-n/p/8175757.html</a></p>
                    """
        QMessageBox.about(window, '关于', about_text)

    """--------------工具栏--------------------
    # DATA：2021/11/26 22:00
    # Author: yalin
    # History: create toolbar
    """
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar('File')
        toolbar.addAction(QIcon('icons/new.svg'),'新建文件', self.new_file_triggered)
        toolbar.addAction(QIcon('icons/open.svg'), '打开文件', self.open_file_triggered)
        toolbar.addAction(QIcon('icons/save80.png'), '保存文件', self.save_triggered)
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/undo.svg'), '撤销', self.text.undo)
        toolbar.addAction(QIcon('icons/redo.svg'), '重做', self.text.redo)
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/cut80.png'), '剪切', self.text.cut)
        toolbar.addAction(QIcon('icons/copy96.png'), '复制', self.text.copy)
        toolbar.addAction(QIcon('icons/paste96.png'), '粘贴', self.text.paste)
        toolbar.addAction(QIcon('icons/clear.png'), '清空编辑区', self.text.clear)
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/punc_trans.svg'), '中英标点纠正', self.punctuation_correct_triggered)
        toolbar.addAction(QIcon('icons/chpt_name.svg'), '章节名格式化', self.chapter_name_format_triggered)
        toolbar.addAction(QIcon('icons/clear_line.svg'), '清除空白行', self.clean_null_line_triggered)
        toolbar.addAction(QIcon('icons/click2format.svg'), '一键格式化', self.click2format_triggered)
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/reset64.png'), '还原文件内容', self.recovery2origin)
        

    """--------------辅助方法-------------------
    # DATE: 2021/11/25
    # Author: yalin
    # History: add show_statusbar_msg function
    """
    def text_changed(self):
        """如果编辑区内容发生更改，则标题栏显示*号，同时更新章节名记录"""
        self.setWindowTitle('*' + self.file_name)
        self.chapter_names = get_all_chapter_name(self.get_lines())
        self.toc.update(self.chapter_names)
        self.is_modified = True

    def get_lines(self) ->list:
        """拆分行"""
        return [line + '\n' for line in self.text.toPlainText().split('\n')]

    def update_edit_content(self, text: str):
        """更新编辑区内容"""
        self.text.selectAll()
        self.text.insertPlainText(text)

    def show_statusbar_msg(self):
        """状态栏常留信息"""
        msg2 = f'打开文件 - {self.file_path}  编码：{self.file_codec}'
        self.statusBar().showMessage(msg2)

"""
# ---------------配置信息------------------
# DATA: 2021/11/26 21:44
# Author: yalin
# History: Create Config and Font class
"""
class Config:
    """配置类"""
    def __init__(self, main_window: MainWindow, text_obj: QPlainTextEdit) -> None:
        self.text = text_obj
        self.window = main_window
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH, 'utf-8')

        # Font attribute
        self.font_family = 'Consolas'
        self.font_size = '16'
        self.font_bold = 'False'
        self.font_italic = 'False'
        self.font_strikeOut = 'False'
        self.font_underline = 'False'

    def judge_config(self):
        """如果配置文件不存在，则新建"""
        if not os.path.exists(CONFIG_FILE_PATH):
            f = open(CONFIG_FILE_PATH, 'w', encoding='utf-8')
            f.close()

    def read_settings(self):
        # 调节窗口大小
        width = self.get_config('Display', 'width', 1000)
        height = self.get_config('Display', 'height ', 800)
        px = self.get_config('Display', 'x', 0)
        py = self.get_config('Display', 'y', 0)
        self.window.move(int(px), int(py))
        self.window.resize(int(width), (height))

        self.default_dir = self.get_config('Setting', 'dir', '')

        self.font_family = self.get_config('Font', 'family', 'Consolas')
        self.font_size = self.get_config('Font', 'size', '10')
        self.font_bold = self.get_config('Font', 'bold', '0')
        self.font_italic = self.get_config('Font', 'italic', '0')
        self.font_strikeOut = self.get_config('Font', 'strikeOut', '0')
        self.font_underline = self.get_config('Font', 'underline', '0')
        font = QFont(self.font_family, int(self.font_size))
        font.setBold(int(self.font_bold))
        font.setItalic(int(self.font_italic))
        font.setStrikeOut(int(self.font_strikeOut))
        font.setUnderline(int(self.font_underline))
        self.text.setFont(font)
        # self.window.font = font

    def write_setting(self):
        """写入用户自定义设置信息到配置文件"""
        # 窗口位置信息
        self.write_config('Display', 'width', str(self.window.size().width()))
        self.write_config('Display', 'height', str(self.window.size().height()))
        self.write_config('Display', 'x', str(self.window.pos().x()))
        self.write_config('Display', 'y', str(self.window.pos().y()))

        self.write_config('Setting', 'dir', self.default_dir)

        self.write_config('Font', 'family', self.text.font().family())
        self.write_config('Font', 'size', str(self.text.font().pointSize()))
        self.write_config('Font', 'bold', int(self.text.font().bold()))
        self.write_config('Font', 'italic', int(self.text.font().italic()))
        self.write_config('Font', 'strikeOut', int(
            self.text.font().strikeOut()))
        self.write_config('Font', 'underline', int(
            self.text.font().underline()))

        # 写入文件
        self.config.write(open(CONFIG_FILE_PATH, 'w', encoding='utf-8'))

    def get_config(self, section, key, default):
        # 返回配置信息，如果获取失败返回默认值
        try:
            return self.config[section][key]
        except:
            return default
    
    def write_config(self, section, key, value):
        # 向config写入信息
        if not self.config.has_section(section):
            self.config.add_section(section)
        # value必须是str，否则会抛TypeError
        self.config.set(section, key, str(value))


class MyFont:
    """字体类"""
    def __init__(self) -> None:
        self.family = 'Consolas'
        self.size = '16'
        self.bold = 'False'
        self.italic = 'False'
        self.strikeOut = 'False'
        self.underline = 'False'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('文本编辑器')
    window = MainWindow()
    sys.exit(app.exec_())
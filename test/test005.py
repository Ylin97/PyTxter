# coding=utf-8
 
from PyQt5.QtGui import  QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTextCodec
import sys
from Ui_main import Ui_MainWindow
from importlib import reload
 
"""初始化QT编码设置"""
reload(sys)
# sys.setdefaultencoding('utf-8')
# QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf-8"))
 
 
def Qstring2Str(qStr):
    """转换Qstring类型为str类型"""
    return qStr.toUtf8()
 
 
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
    
        # 文本框
        self.textBrowser.setText("这是测试文字...测试,测试,测试,一共多少个测试?")
        # 文本框内容变化重设被搜索内容
        self.textBrowser.textChanged.connect(self.reset_search_content)
        # 点击按钮开始搜索
        self.search_btn.clicked.connect(self.search)
 
        # 搜索相关项
        self.search_content = None
        self.search_key = None
        self.search_count = 0
        self.search_current = 0
 
    def select(self, start, length):
        """选中文字,高亮显示"""
        cur = QTextCursor(self.textBrowser.textCursor())
        cur.setPosition(start)
        cur.setPosition(start + length, QTextCursor.KeepAnchor)
        self.textBrowser.setTextCursor(cur)
 
    def reset_search_content(self):
        """改变待搜索内容"""
        self.search_content = None
        self.search_count = 0
        self.search_current = 0
 
    def search(self):
        """搜索"""
        key_word = Qstring2Str(self.search_edit.text())
        if key_word != self.search_key:
            self.search_key = key_word
            self.search_count = 0
            self.search_current = 0
        if not self.search_content:
            self.search_content = Qstring2Str(self.textBrowser.toPlainText())
        if not self.search_count:
            self.search_count = self.search_content.count(key_word)
            if self.search_count != 0:
                start = self.search_content.index(key_word)
                self.select(start, len(key_word))
                self.search_current += 1
        else:
            if self.search_current < self.search_count:
                start = self.search_content.find(key_word, self.textBrowser.textCursor().position())
                if start != -1:
                    self.select(start, len(key_word))
                    self.search_current += 1
            else:
                self.search_count = 0
                self.search_current = 0
                self.search()
        self.textBrowser.setFocus()
        self.search_res.setText("{}/{}".format(self.search_current, self.search_count))
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
# coding=utf-8
import sys

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QAction, qApp, QTextEdit, QFileDialog, QShortcut


class MainFace(QMainWindow):
    """主界面"""

    def __init__(self):
        super().__init__()
        self.initUI()

        # # 快捷键定义
        # QShortcut(QKeySequence(self.tr("Ctrl+S")), self, self.close)

    def initUI(self):
        """初始化界面"""

        # 菜单栏
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("文件")
        self.edit_menu = menu_bar.addMenu("编辑")
        self.view_menu = menu_bar.addMenu("视图")
        self.format_menu = menu_bar.addMenu("格式")
        self.tool_menu = menu_bar.addMenu("工具")
        self.help_menu = menu_bar.addMenu("帮助")

        # file_menu菜单
        file_menu_items = {'new': ['新建', self.new_dialog, 'Ctrl+N', 'New'],
                           'open': ['打开', self.openfile_dialog, 'Ctrl+O', 'Open file', 'open.png'],
                           'save': ['保存', self.savefile_dialog, 'Ctrl+S', 'Save file'],
                           'save_as': [],
                           'save_with': [],
                           'quit': ['退出', qApp.exit, 'Ctrl+Q', 'Exit application', 'exit.png']}
        # file_menu_list = ['新建  Ctrl+N', '打开  Ctrl+O', '另存为  Ctrl+Shift+S',
        #                   '另存为指定编码', '退出  Ctrl+Q']

        # 退出
        self.quit(file_menu_items['quit'])

        # 打开
        self.openfile(file_menu_items['open'])

        # 新建
        self.new(file_menu_items['new'])

        # 保存
        self.savefile(file_menu_items['save'])

        # edit_menu菜单
        edit_menu_list = ['一键格式化', '章节名格式化', '清除空白行', '屏蔽字替换',
                          '清除异常换行符', '中英标点纠正', '转换编码为 utf-8',
                          '转换编码为 utf-8 with BOM', '查找', '替换']
        edit_actions = [QAction(item, self) for item in edit_menu_list]
        self.edit_menu.addActions(edit_actions)

        # view_menu菜单
        view_menu_list = []
        view_actions = [QAction(item, self) for item in view_menu_list]
        self.view_menu.addActions(view_actions)

        # format_menu菜单
        format_menu_list = []
        format_actions = [QAction(item, self) for item in format_menu_list]
        self.format_menu.addActions(format_actions)

        # tool_menu菜单
        tool_menu_list = []
        tool_actions = [QAction(item, self) for item in tool_menu_list]
        self.tool_menu.addActions(tool_actions)

        # help_menu菜单
        help_menu_list = ['关于', '反馈', '请作者喝咖啡']
        help_actions = [QAction(item, self) for item in help_menu_list]
        self.help_menu.addActions(help_actions)

        # 工具栏
        # self.tool_bar = self.addToolBar("章节名格式化")

        # 状态栏
        status_bar = self.statusBar()

        # 显示
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowTitle('txt小说格式化器')
        self.show()

    def action(self, act_name, slot, shortcut=None, status_tip=None, icon=None):
        """定义动作"""
        act = QAction(QIcon(icon), act_name, self)
        act.setShortcut(shortcut)
        act.setStatusTip(status_tip)
        act.triggered.connect(slot)
        return act

    def new(self, params):
        """新建文件"""
        new_act = self.action(*params)
        self.file_menu.addAction(new_act)

    def new_dialog(self):
        """新建文件会话"""
        self.text_edit = QTextEdit()  # 创建一个文本编辑区
        self.setCentralWidget(self.text_edit)  # 并将其放在窗口中央
        self.setWindowTitle('未命名.txt')

    def openfile(self, params):
        """打开文件"""
        open_act = self.action(*params)
        self.file_menu.addAction(open_act)

    def openfile_dialog(self):
        """打开文件会话"""
        self.text_edit = QTextEdit()  # 创建一个文本编辑区
        self.setCentralWidget(self.text_edit)  # 并将其放在窗口中央

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Txt files(*.txt)")  # 打开文件筛选器选择文件
        # print(fname)
        if fname[0]:
            with open(fname[0], 'r', encoding='utf-8') as fr:
                self.text_edit.setText(fr.read())

    def savefile(self, params):
        """保存文件"""
        save_act = self.action(*params)
        self.file_menu.addAction(save_act)

    def savefile_dialog(self):
        """保存文件对话"""
        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        print(fname)
        if fname[0]:
            with open(fname[0] + '.txt', 'w', encoding='utf-8', errors='ignore') as fw:
                fw.write(self.text_edit.toPlainText())

    def quit(self, params):
        """退出程序"""
        exit_act = self.action(*params)
        self.file_menu.addAction(exit_act)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    face = MainFace()
    sys.exit(app.exec_())

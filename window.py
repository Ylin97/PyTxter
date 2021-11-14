from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *


# 主界面
class MainWindow(QMainWindow):
    def closeEvent(self, a0) -> None:
        if not text.document().isModified():
            return
        answer = QMessageBox.question(window, '退出程序', '关闭之前是否保存文件',
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                                      )
        # print(answer)
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            a0.ignore()


app = QApplication([])
app.setApplicationName("文本编辑器")
text = QPlainTextEdit()
window = MainWindow()
window.setMinimumSize(800, 600)
window.setCentralWidget(text)

# 文件路径
file_path = None

# 菜单项
menu = window.menuBar().addMenu('文件')


# 打开
def open_file():
    global file_path
    path = QFileDialog.getOpenFileName(window, 'open')[0]
    if path:
        text.setPlainText(open(path, 'r', encoding='utf-8').read())
        file_path = path


open_action = QAction('打开')
open_action.setShortcut(QKeySequence.Open)
open_action.triggered.connect(open_file)
menu.addAction(open_action)

menu.addSeparator()


# 保存
def save():
    if file_path is None:
        pass
    else:
        with open(file_path, 'w', encoding='utf-8') as fw:
            fw.write(text.toPlainText())
        text.document().setModified(False)


save_action = QAction('保存')
save_action.setShortcut(QKeySequence.Save)
save_action.triggered.connect(save)
menu.addAction(save_action)

menu.addSeparator()


# 另存为
def save_as():
    global file_path
    path = QFileDialog.getSaveFileName(window, '另存为')[0]
    if path:
        file_path = path
        save()


save_as_action = QAction('另存为')
save_as_action.setShortcut(QKeySequence.SaveAs)
save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)

# 退出
menu.addSeparator()
quit_action = QAction('退出')
quit_action.setShortcut(QKeySequence.Quit)
quit_action.triggered.connect(window.close)
menu.addAction(quit_action)

# 帮助
help_menu = window.menuBar().addMenu('帮助')
about_action = QAction('关于')


def show_about_dialog():
    about_text = "<center>这是一个文本编辑器</center><p>版本：1.0</p>"
    QMessageBox.about(window, '说明', about_text)


about_action.triggered.connect(show_about_dialog)
help_menu.addAction(about_action)

window.show()
app.exec_()

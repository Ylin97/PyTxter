import sys
from PyQt5 import QtWidgets
from window import Ui_TextEdit

# 加载窗体
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = Ui_TextEdit()
ui.setupUi(window)

# 加载按钮事件
ui.tool_open.clicked.connect(ui.open_file)
ui.tool_save.clicked.connect(ui.save_file)
ui.tool_clear.clicked.connect(ui.clear_content)
ui.tool_exit.clicked.connect(ui.exit_window)
ui.tool_save_as.clicked.connect(ui.save_as_other_file)
ui.tool_recover.clicked.connect(ui.recover_content)
ui.tool_unmake.clicked.connect(ui.unmake_content)

window.show()
sys.exit(app.exec_())

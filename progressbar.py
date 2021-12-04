import sys
from PyQt5.QtCore import QBasicTimer, QRect, QTimerEvent, Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QDialog, QHBoxLayout, QLayout, QPushButton, QVBoxLayout, QWidget, QProgressBar


class ProgressBar(QDialog):
    """进度条类"""
    def __init__(self,  parent=None):
        super(ProgressBar, self).__init__(parent)
 
        # Qdialog窗体的设置
        self.setWindowTitle("正在处理中")
        self.resize(500, 64) # QDialog窗的大小
 
        # 创建并设置 QProcessbar
        self.progressBar = QProgressBar(self) # 创建
        self.progressBar.setMinimum(0) #设置进度条最小值
        self.progressBar.setMaximum(100)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 进度条初始值为0
        self.progressBar.setGeometry(QRect(1, 3, 499, 28)) # 设置进度条在 QDialog 中的位置 [左，上，右，下]
        self.show()
 
    def set_value(self, value): # 设置总任务进度
        self.progressBar.setValue(value)
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    progress_bar = ProgressBar()
    sys.exit(app.exec_())

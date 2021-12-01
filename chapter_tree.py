import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QWidget


class TOC(QWidget):
    def __init__(self, parent=None, chapter_names: dict=None) -> None:
        super().__init__(parent)
        self.chapter_names = chapter_names
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('目录')

        # 设置根节点
        # self.root = QTreeWidgetItem(self.tree)
        
        self.update()
        # self.tree.addTopLevelItem(self.root)
        # 目录全部展开
        self.tree.clicked.connect(self.clicked_event)
        self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        self.show()

    def add_item(self, chapter_name: str):
        """添加目录项"""
        item = QTreeWidgetItem(self.tree)
        item.setText(0, chapter_name)
        # self.root.addChild(item)

    def update(self):
        """更新目录"""
        for chapter_name in self.chapter_names.keys():
            self.add_item(chapter_name)

    def clicked_event(self):
        """目录项点击事件"""
        item = self.tree.currentItem()
        print(item.text(0))
        
if __name__ == '__main__':
    chap_names = {'第一章 开始': 0,
                  '第二章 继续': 5,
                  '第三章 觉醒': 10}
    app = QApplication(sys.argv)
    tree = TOC(chapter_names=chap_names)
    # tree.show()
    sys.exit(app.exec_())
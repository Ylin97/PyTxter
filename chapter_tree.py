import sys

from PyQt5.QtWidgets import QApplication, QBoxLayout, QHBoxLayout, QLayout, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget


class TOC(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.resize(800, 600)
        self.parent = parent
        self.chapter_names = {}
        self.tree = QTreeWidget()
        # self.tree.setWindowTitle('小说目录')
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('目录')
        # 必须为 self 设置布局，否则 self.tree 不会显示到 TOC 的实例中
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.tree)
        # self.setMinimumWidth(100)
        self.setLayout(mainlayout)

        # 设置根节点
        # self.root = QTreeWidgetItem(self.tree)
        
        self.update(None)
        # self.tree.addTopLevelItem(self.root)
        # 目录全部展开
        self.tree.clicked.connect(self.clicked_event)
        self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        # self.show()

    def add_item(self, chapter_name: str):
        """添加目录项"""
        item = QTreeWidgetItem(self.tree)
        item.setText(0, chapter_name)
        # self.root.addChild(item)

    def delete_all_item(self):
        """删除所有节点"""
        items = [self.tree.topLevelItem(idx) for idx in range(self.tree.topLevelItemCount())]
        for item in items:
            self.delete_item(item)

    def delete_item(self, item: QTreeWidgetItem):
        """递归删除节点"""
        count = item.childCount()
        if not count:
            idx = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(idx)
            return
        
        for i in range(count):
            child_item = item.child(0)
            self.delete_item(child_item)
        del item

    def update(self, chapter_names: dict):
        """更新目录"""
        self.chapter_names = chapter_names
        if not self.chapter_names:
            return
        # self.tree.selectAll()
        self.delete_all_item()
        for chapter_name in self.chapter_names.keys():
            self.add_item(chapter_name)

    def clicked_event(self):
        """目录项点击事件"""
        item = self.tree.currentItem()
        # print(item.text(0))
        self.parent.goto_confirm_triggered(self.chapter_names[item.text(0)])
        
if __name__ == '__main__':
    chap_names = {'第一章 开始': 0,
                  '第二章 继续': 5,
                  '第三章 觉醒': 10}
    app = QApplication(sys.argv)
    tree = TOC()
    tree.update(chap_names)
    tree.show()
    sys.exit(app.exec_())
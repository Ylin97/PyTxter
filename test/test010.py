import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
 
 
class ModifyTree(QWidget):
    def __init__(self,parent=None):
        super(ModifyTree, self).__init__(parent)
        self.setWindowTitle('增加修改和删除树控件中的节点')
        self.resize(400,300)
 
        operatorLayout=QHBoxLayout()#水平布局
 
        addBtn=QPushButton('添加节点')
        updateBtn=QPushButton('修改节点')
        deleteBtn=QPushButton('删除节点')
 
        operatorLayout.addWidget(addBtn)
        operatorLayout.addWidget(updateBtn)
        operatorLayout.addWidget(deleteBtn)
 
        addBtn.clicked.connect(self.addNode)
        updateBtn.clicked.connect(self.updateNode)
        deleteBtn.clicked.connect(self.deleteNode)
 
        # 树
        self.tree = QTreeWidget()
        # 为树控件指定列数
        self.tree.setColumnCount(2)
        # 指定列标签
        self.tree.setHeaderLabels(['Key', 'Value'])
 
        # 根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'root')  # 0代表第一列，即Key列,值为root
        root.setText(1, '0')
 
        # 添加子节点child1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, '1')
 
        # 添加子节点child2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '2')
 
        # 为child2添加一个子节点child3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, '3')
 
        # 信号和槽
        self.tree.clicked.connect(self.onTreeClicked)
 
        mainLayout=QVBoxLayout(self)
        mainLayout.addLayout(operatorLayout)
        mainLayout.addWidget(self.tree)
        self.setLayout(mainLayout)
 
    def onTreeClicked(self, index):  # index是被点击节点的索引
        item = self.tree.currentItem()  # 获得当前单击项
        print('当前处于第%d行' % index.row())  # 输出当前行（自己父节点的第几个值）
        print('key=%s，value=%s' % (item.text(0), item.text(1)))
        print()
 
    def addNode(self):
        print('添加节点')
        item=self.tree.currentItem()# 获得当前结点
        print('当前节点是：',item)
        node=QTreeWidgetItem(item)
        node.setText(0,'新节点')
        node.setText(1,'新值')
 
    def updateNode(self):
        print('修改节点')
        item=self.tree.currentItem()
        item.setText(0,'修改节点')
        item.setText(1,'值已经被修改')
 
    def deleteNode(self):
        print('删除节点')
        #防止item是root时，root无父结点报错，要使用下面的写法
        rootFather=self.tree.invisibleRootItem()#获得根节点root的不可见的父节点
        for item in self.tree.selectedItems():
            #父节点不为空
            (item.parent() or rootFather).removeChild(item)
 
 
if __name__=='__main__':
    app=QApplication(sys.argv)
    main=ModifyTree()
    main.show()
    sys.exit(app.exec_())
 
import sys
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QTextFormat

from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QMainWindow, QPlainTextEdit, QSplitter, QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,\
    QTextEdit

# from ../qcodeeditor import QCodeEditor

class MainWindow(QMainWindow):
    def __init__(self, chapter_names):
        super().__init__()

        editor_layout = QHBoxLayout()

        self.editor = QCodeEditor()
        self.toc = TOC(chapter_names=chapter_names)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.toc)
        splitter.addWidget(self.editor)

        editor_layout.addWidget(splitter)
        # editor_layout.addWidget(self.toc)
        # editor_layout.addWidget(self.editor)
        # editor_layout.setStretch(0, 1)
        # editor_layout.setStretch(1, 3)

        # edit_widget = QWidget()
        # edit_widget.setLayout(editor_layout)
        # self.setCentralWidget(edit_widget)

        self.setCentralWidget(QCodeEditor())
        # self.setCentralWidget(self.toc)


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
        # self.show()
        tree_layout = QVBoxLayout()
        tree_layout.addWidget(self.tree)
        self.setLayout(tree_layout)

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


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
 
    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space
 
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
 
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
 
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
 
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
 
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        color = QColor("#f0f0f0")
        # painter.fillRect(event.rect(), Qt.lightGray)
        painter.fillRect(event.rect(), color)
 
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
 
        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor("#008080"))
                painter.setFont(QFont('Consolas', 9))
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
                # painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
 
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
 

class QLineNumberArea(QWidget):
    """行号区域类"""
    def __init__(self, editor: QCodeEditor):
        super().__init__(editor)
        self.codeEditor = editor
 
    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)
 
    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
        
        
if __name__ == '__main__':
    chap_names = {'第一章 开始': 0,
                  '第二章 继续': 5,
                  '第三章 觉醒': 10}
    app = QApplication(sys.argv)
    # tree = TOC(chapter_names=chap_names)
    window = MainWindow(chap_names)
    window.show()
    # tree.show()
    sys.exit(app.exec_())
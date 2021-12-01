import typing
from PyQt5.QtWidgets import QTreeWidget, QWidget

class TOC(QTreeWidget):
    """目录树"""
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent=parent)
    

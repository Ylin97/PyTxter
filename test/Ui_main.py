from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QTextBrowser, QWidget
 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.search_edit = QLineEdit(self.centralWidget)
        self.search_edit.setObjectName(_fromUtf8("search_edit"))
        self.horizontalLayout.addWidget(self.search_edit)
        self.search_btn = QPushButton(self.centralWidget)
        self.search_btn.setObjectName(_fromUtf8("search_btn"))
        self.horizontalLayout.addWidget(self.search_btn)
        self.search_res = QLabel(self.centralWidget)
        self.search_res.setObjectName(_fromUtf8("search_res"))
        self.horizontalLayout.addWidget(self.search_res)
        spacerItem = QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QTextBrowser(self.centralWidget)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralWidget)
 
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.search_btn.setText(_translate("MainWindow", "搜索", None))
        self.search_res.setText(_translate("MainWindow", "0/0", None))
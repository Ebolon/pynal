#!/usr/bin/env python
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        tabMenu = self.menuBar().addMenu("&Tabs")
        tabMenu.addAction(self.createAction("Add Tab", self.addTab))
        tabMenu.addAction(self.createAction("Rotate", self.rotate))

        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(QtGui.QWidget(), "new Tab 1")
        self.tabs.addTab(QtGui.QWidget(), "new Tab 2")
        self.tabs.addTab(QtGui.QWidget(), "new Tab 3")
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.connect(self.tabs, SIGNAL("tabCloseRequested(int)"), self.close)

        self.setCentralWidget(self.tabs)

        self.resize(500, 700)

    def createAction(self, text, slot):
        action = QtGui.QAction(text, self)
        self.connect(action, SIGNAL("triggered()"), slot)
        return action

    def addTab(self):
        self.tabs.addTab(QtGui.QWidget(), "new Tab " + str(self.tabs.count()+1))

    def rotate(self):
        pos = (self.tabs.tabPosition() + 1) % 4
        self.tabs.setTabPosition(pos)

    def close(self, index):
        self.tabs.removeTab(index)

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

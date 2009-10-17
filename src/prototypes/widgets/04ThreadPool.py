#!/usr/bin/env python
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.num = 0

        button = QtGui.QPushButton(self)
        button.setText("Start")
        self.connect(button, SIGNAL("clicked()"), self.threads)

        self.setCentralWidget(button)

        self.pool = QtCore.QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(4)

    def threads(self):
        thread = TestThread(self.num)
        self.num += 1
        self.pool.start(thread)
        thread = TestThread(self.num)
        self.num += 1
        self.pool.start(thread)

class TestThread(QtCore.QRunnable):

    def __init__(self, num):
        QtCore.QRunnable.__init__(self)
        self.num = num

    def run(self):
        print self.num

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

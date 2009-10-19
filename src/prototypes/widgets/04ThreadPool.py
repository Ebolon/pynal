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

        self.pool = Pool()
        self.pool.setMaxThreadCount(4)

    def threads(self):
        thread1 = TestThread(self.num)
        self.num += 1
        self.pool.start(thread1)
        thread2 = TestThread(self.num)
        self.num += 1
        self.pool.start(thread2)

class TestThread(QtCore.QThread):

    def __init__(self, num):
        QtCore.QRunnable.__init__(self)
        self.num = num

    def run(self):
        print self.num

class Pool():
    def __init__(self, parent=None):
        self.pool = QtCore.QThreadPool.globalInstance()

        self.threads = []

    def start(self, runnable):
        self.threads.append(runnable)
        self.pool.start(runnable)

    def setMaxThreadCount(self, num):
        self.pool.setMaxThreadCount(num)

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

#!/usr/bin/env python
'''
Created on 14.05.2009
tabletTest.py
@author: dominik
'@note: super!!!!!
'''
import sys

from PyQt4 import QtCore, QtGui

class Test(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QFrame.__init__(self)
        self.setWindowTitle("Tablet Test")
        containerwidget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        
        labels = QtGui.QVBoxLayout()
        self.posx = QtGui.QLabel("XPos: ")
        self.posy = QtGui.QLabel("YPos: ")
        self.tip = QtGui.QLabel("Tip: ")
        labels.addWidget(self.posx)
        labels.addWidget(self.posy)
        labels.addWidget(self.tip)
        labels.addStretch(1)
        
        self.pres = QtGui.QProgressBar()
        self.pres.setOrientation(QtCore.Qt.Vertical)
        
        layout.addLayout(labels)
        layout.addWidget(self.pres)
        containerwidget.setLayout(layout)
        self.setCentralWidget(containerwidget)
        
    def tabletEvent(self, event):
        stylus = QtGui.QTabletEvent.Pen
        eraser = QtGui.QTabletEvent.Eraser
        if event.pointerType() == stylus:
            self.tip.setText("Tip: Pen")
        elif event.pointerType() == eraser:
            self.tip.setText("Tip: Eraser")
        else:
            self.tip.setText("Tip: unknown")
        self.pres.setValue(event.pressure()*100)
        self.posx.setText("XPos: " + str(event.x()))
        self.posy.setText("YPos: " + str(event.y()))
    

app = QtGui.QApplication(sys.argv)
widget = Test()
widget.show()
sys.exit(app.exec_())

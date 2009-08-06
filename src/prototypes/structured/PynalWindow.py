'''
Created on 27.05.2009

@author: dominik
'''
from PyQt4 import QtGui, QtCore

from widgets.PynalGView import *
from tools.Line import LineTool
from tools.Pen import PenTool

class PynalWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk IV")
        
        self.view = PynalGView()
        self.setCentralWidget(self.view)
        
        self.setPenTool()
        
        bar = self.addToolBar("Tools")
        action = bar.addAction("Line")
        self.connect(action, QtCore.SIGNAL("triggered()"), self.setLineTool)
        action = bar.addAction("Pen")
        self.connect(action, QtCore.SIGNAL("triggered()"), self.setPenTool)
        
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setMaximum(200)
        slider.setMinimum(10)
        slider.setValue(100)
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"), self.view.changeScale)
        bar.addWidget(slider)
        
    def setLineTool(self):
        self.view.setTool(LineTool())
        
    def setPenTool(self):
        self.view.setTool(PenTool())
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    moep = PynalWindow()
    moep.show()
    app.exec_()

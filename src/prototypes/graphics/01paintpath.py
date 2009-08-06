'''
Created on 17.05.2009

Basic registering of a dragging event and visualisation with a line from start
to endpoint.

And some AA for nice view.

@author: dominik
'''
import sys

from PyQt4 import QtGui, QtCore

class PaintTest(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.resize(450, 400)
        self.setWindowTitle("Moep")
        
        self.start = None
        self.end = None
        
    def mouseMoveEvent(self, event):
        if self.start is None:
            self.start = QtGui.QMouseEvent(event)
        else:
            self.end = QtGui.QMouseEvent(event)
        self.update()
        
    def mouseReleaseEvent(self, event):
        self.start = None
            
    def paintEvent(self, event):
        if self.start is not None and self.end is not None:
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            
            painter.drawLine(self.start.x(), self.start.y(), self.end.x(), self.end.y())
            
            painter.end()
        
app = QtGui.QApplication(sys.argv)
p = PaintTest()
p.show()
app.exec_()

'''
Created on 16.05.2009

@author: dominik
'''
import sys, copy

from PyQt4 import QtGui, QtCore

class Moep(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.resize(300, 300)
        self.tablet = None
    
    def tabletEvent(self, event):
        self.tablet = QtGui.QTabletEvent(event) 
        event.ignore()
        
    def mousePressEvent(self, event):
        print event.x()
        if self.tablet is not None and event.x() == self.tablet.x():
            print self.tablet.x(), self.tablet.pressure()
        

app = QtGui.QApplication(sys.argv)
moep = Moep()
moep.show()
app.exec_()

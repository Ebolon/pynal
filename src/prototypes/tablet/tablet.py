'''
Created on 13.05.2009

@author: dominik
'''
import sys

from PyQt4 import QtCore, QtGui

class Test(QtGui.QFrame):

    def __init__(self):
        QtGui.QFrame.__init__(self)
        pass
        
    def tabletEvent(self, event):
        stylus = QtGui.QTabletEvent.Pen
        pres = event.pressure()
        if pres > 0:
            pointer = event.pointerType()
            if pointer == stylus:
                print event.x()
    

app = QtGui.QApplication(sys.argv)
widget = Test()

widget.show()



app.exec_()

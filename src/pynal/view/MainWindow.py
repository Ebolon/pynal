'''
Uh, the main window. Contains more or less useful toolbars, menus and
a heroic status bar.

Oh and some place to display the actual journaling area...
'''
from PyQt4 import QtGui

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, config):
        QtGui.QMainWindow.__init__(self)
        
        self.config = config

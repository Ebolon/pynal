'''
Entry point for the pynal appliaction.

Parses the startup parameters and creates a config object for the app.
'''
import sys

from PyQt4 import QtGui

from models.Config import Config
from view.MainWindow import MainWindow

def load_config(args):
    """ Creates the configuration object that will be used in this instance. """
    return Config(args)

if __name__ == "__main__":
    config = load_config(sys.argv)
    
    app = QtGui.QApplication(sys.argv)
    
    mw = MainWindow(config)
    mw.show()
    
    sys.exit(app.exec_())

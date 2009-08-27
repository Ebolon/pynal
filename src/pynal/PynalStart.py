# -*- coding: utf-8 -*-
'''
Entry point for the pynal appliaction.

Parses the startup parameters and creates a config object for the app.
'''
import sys

from PyQt4 import QtGui

from models import Config
from view.MainWindow import MainWindow

def load_config(args):
    """ Creates the configuration object that will be used in this instance. """
    return Config(args)

if __name__ == "__main__":
    Config.parse_args(sys.argv)
    Config.load_config()

    app = QtGui.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
"""
Module containing the MainWindowControl class.
"""
import os

from PyQt4 import QtGui
from PyQt4 import QtCore

from pynal.control import actions
from pynal.view.PynalDocument import *

class MainWindowControl(QtCore.QObject):
    """
    Provides slots for actions coming from or working with a MainWindow object.

    Extends the QObject for convenient access to tr() and connect().
    """

    def __init__(self, window):
        """ Creates a new MainWindowControl. """
        QtCore.QObject.__init__(self)
        self.window = window
        actions.init(self, window)

    def start(self):
        """
        Called when the window has been set up and is ready to receive
        commands. E.g. opening documents.
        """
        for file in Config.open_files:
            filename = os.path.basename(str(file))
            self.window.tabWidget.addTab(PynalDocument(file), filename)

    def open_file(self):
        """
        Open a dialog to let the user choose pdf files and open
        them in tabs.
        """
        files = QtGui.QFileDialog.getOpenFileNames(
                   self.window, self.tr("Open PDF file"), "", "PDF (*.pdf)")
        if not files:
            return

        for file in files:
            filename = os.path.basename(str(file))
            self.window.tabWidget.addTab(PynalDocument(file), filename)

    def save_file(self):
        """ Save the current document. """
        pass

    def new_file(self):
        """ Create a new document. """
        self.window.tabWidget.addTab(PynalDocument(), "New Document")

    def exit(self):
        """ Exit the application. """
        pass

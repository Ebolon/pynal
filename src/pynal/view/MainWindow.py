# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

from pynal.control import actions
from pynal.models import Config
from pynal.control.MainControl import MainWindowControl

class MainWindow(QtGui.QMainWindow):
    '''
    Uh, the main window. Contains more or less useful toolbars, menus and
    a heroic status bar.

    Oh and some place to display the actual journaling area...
    '''

    def __init__(self):
        """
        Creates a new MainWindow.
        """
        QtGui.QMainWindow.__init__(self)
        self.control = MainWindowControl(self)

        self.setWindowTitle("Pynal")

        self.createTabWidget()
        self.createMenuBar()
        self.createToolbar()

        self.resize(Config.get_int("Main", "window_width"),
                    Config.get_int("Main", "window_height"))

        self.control.start()

    def createToolbar(self):
        """
        Create and popular the toolbar.

        TODO: can this be customized by the user?
        """
        bar = self.addToolBar("File operations")
        bar.addAction(actions.toolbar("new_file_action"))
        bar.addAction(actions.toolbar("open_file_action"))
        bar.addAction(actions.toolbar("save_file_action"))
        bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        zoombar = self.addToolBar("Scaling")
        zoombar.addAction(actions.toolbar("doc_zoom_in"))
        zoombar.addAction(actions.toolbar("doc_zoom_100"))
        zoombar.addAction(actions.toolbar("doc_zoom_out"))
        zoombar.addAction(actions.toolbar("doc_zoom_fit"))
        zoombar.addAction(actions.toolbar("doc_zoom_width"))

        debug = self.addToolBar("Debug")
        # No debug actions atm

    def createMenuBar(self):
        """ Create and populate the menu bar. """
        menu = self.menuBar()
        file = menu.addMenu("&File")
        file.addAction(actions.menu("exit_app_action"))

    def createTabWidget(self):
        """ Create and configure the center widget. """
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setDocumentMode(True)
        self.connect(self.tabWidget, SIGNAL("tabCloseRequested(int)"), self.control.close_document)

        self.tabWidget.tabBar().hide()

        self.setCentralWidget(self.tabWidget)

    def rotate(self):
        """ Rotate the position of the tabs. """
        pos = (self.tabs.tabPosition() + 1) % 4
        self.tabWidget.setTabPosition(pos)

    def closeEvent(self, event):
        """
        Intercept the close event of the main window.
        Check wether the application can be cleanly closed
        and save the current state.
        """
        QtGui.QMainWindow.closeEvent(self, event)
        if event.isAccepted():
            self.save_state()

    def save_state(self):
        """ Save the size of the window to the configuration. """
        Config.set("Main", "window_width", str(self.width()))
        Config.set("Main", "window_height", str(self.height()))

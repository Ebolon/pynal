# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

from PyKDE4 import kdeui
from PyKDE4.kparts import KParts

from pynal.control import actions
from pynal.models import Config
from pynal.control.MainControl import MainWindowControl

class MainWindow(KParts.MainWindow):
    '''
    Uh, the main window. Contains more or less useful toolbars, menus and
    a heroic status bar.

    Oh and some place to display the actual journaling area...
    '''

    def __init__(self):
        """
        Creates a new MainWindow.
        """
        KParts.MainWindow.__init__(self)
        self.control = MainWindowControl(self)

        print "setting gui"
        self.setupGUI()

        self.createTabWidget()

        self.control.start()

    def createToolbar(self):
        """
        Create and popular the toolbar.

        TODO: can this be customized by the user?
        """

        zoombar = self.toolBar("Scaling")
        zoombar.addAction(actions.toolbar("doc_zoom_in"))
        zoombar.addAction(actions.toolbar("doc_zoom_100"))
        zoombar.addAction(actions.toolbar("doc_zoom_out"))
        zoombar.addAction(actions.toolbar("doc_zoom_fit"))
        zoombar.addAction(actions.toolbar("doc_zoom_width"))
        zoombar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        tools = self.toolBar("Tools")
        toolgroup = QtGui.QActionGroup(tools)
        tools.addAction(actions.toolbar("tool_scroll", toolgroup))
        tools.addAction(actions.toolbar("tool_select", toolgroup))
        tools.addAction(actions.toolbar("tool_pen", toolgroup))
        tools.addAction(actions.toolbar("tool_eraser", toolgroup))
        tools.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        debug = self.toolBar("Debug")
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
        """
        Rotate the position of the tabs.
        TODO: currently not used
        """
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
#        Config.set("Main", "window_width", str(self.width()))
#        Config.set("Main", "window_height", str(self.height()))
#        Config.set("Main", "window_maximized", str(self.isMaximized()))
        pass

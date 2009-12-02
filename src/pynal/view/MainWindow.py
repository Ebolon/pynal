# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from PyKDE4 import kdeui
from PyKDE4.kparts import KParts

from pynal.control import actions
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

        self.setupGUI()

        self.createTabWidget()

        self.control.start()

    def createMenuBar(self):
        """ Create and populate the menu bar. """
        menu = self.menuBar()
        file = menu.addMenu("&File")
        file.addAction(actions.menu("exit_app_action"))

    def createTabWidget(self):
        """ Create and configure the center widget. """
        self.tabWidget = kdeui.KTabWidget(self)
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

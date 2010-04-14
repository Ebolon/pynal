# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from PyQt4 import QtCore

from PyKDE4 import kdeui
from PyKDE4.kparts import KParts

from pynal.control import actions
from pynal.control.MainControl import MainWindowControl
from pynal.view.Widgets import ColorPicker

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
        self.createLineStyleComboBox()
        self.createTabWidget()
        self.control.start()


    def createLineStyleComboBox(self):
        """ Create and populate the ComboBox for Stroke Style """
        # TODO: improve speed, style of the ComboBox?
        styles = [QtCore.Qt.SolidLine, QtCore.Qt.DashLine, QtCore.Qt.DotLine, QtCore.Qt.DashDotLine, QtCore.Qt.DashDotDotLine]
        comboBox = QtGui.QComboBox(self)
        self.pen = QtGui.QPen()
        self.pen.setWidth(3)
        pixmap = QtGui.QPixmap(113,3)
        for style in styles:
            self.pen.setStyle(style)
            pixmap.fill()
            painter = QtGui.QPainter(pixmap)
            painter.setPen(self.pen)
            painter.drawLine(0,1, 113,1)
            painter.end()
            icon = QtGui.QIcon(pixmap)
            comboBox.addItem("")
            comboBox.setItemIcon(comboBox.count()-1, icon)
            comboBox.setIconSize(QtCore.QSize(113, 3))
        
        self.connect(comboBox, SIGNAL("currentIndexChanged(int)"),  self.control.changeLineStyle)
        self.toolBar("StrokeToolBar").addWidget(comboBox)
        colorpicker = ColorPicker(self)
        self.toolBar("StrokeToolBar").addWidget(colorpicker)

    def createMenuBar(self):
        """ Create and populate the menu bar. """
        pass

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

# -*- coding: utf-8 -*-
"""
Module containing the MainWindowControl class.
"""
import os, math
import pynal.models.Config as Config

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import KStandardAction, KAction, KIcon
from PyKDE4.kio import KFileDialog
from PyKDE4.kdecore import KUrl, KCmdLineArgs

from pynal.control import actions
from pynal.view.PynalDocument import *

from pynal.models.xournal import Xournal

class MainWindowControl(QtCore.QObject):
    """
    Provides slots for actions coming from or working with a MainWindow object.

    Extends the QObject for convenient access to tr() and connect().
    """

    def __init__(self, window):
        """ Creates a new MainWindowControl. """
        QtCore.QObject.__init__(self)
        self.window = window
        self.createActions()
        actions.init(self, window)

    def createActions(self):
        actionCollection = self.window.actionCollection()
        KStandardAction.openNew(self.new_file, actionCollection)
        KStandardAction.open(self.open_file, actionCollection)
        KStandardAction.save(self.save_file, actionCollection)

        KStandardAction.quit(self.quit, actionCollection)

    def start(self):
        """
        Called when the window has been set up and is ready to receive
        commands. E.g. opening documents.

        This can be extended to auto-reopen documents that were open
        when pynal was closed the last time.
        """
        args = KCmdLineArgs.parsedArgs()

        for i in range(args.count()):
            filename = os.path.basename(str(args.arg(i)))
            if os.path.isfile(args.arg(i)):
                self.open_document(PynalDocument(args.arg(i)), filename)

    def open_file(self):
        """
        Open a dialog to let the user choose pdf files and open
        them in tabs.
        """
        files = KFileDialog.getOpenFileNames(KUrl(), "*.pyn | *.pyn - Pynal File\n *.xoj | *.xoj - Xournal File\n *.pdf| *.pdf - PDF files\n * | All Files")
        if not files:
            return
 
        for file in files:
            filename = os.path.basename(str(file))
            (shortname, extension) = os.path.splitext(filename)
            if (extension == ".pdf"):
                self.open_document(PynalDocument(file), filename)
            elif (extension == ".xoj"):
                document = PynalDocument()
                self.open_document(document, shortname)
                xournal = Xournal(file, document)
                xournal.load() 

    def open_document(self, document, filename):
        """ Shows a PynalDocument in the journaling area. """
        tabwidget = self.window.tabWidget
        newindex = tabwidget.addTab(document, filename)
        tabwidget.setCurrentIndex(newindex)
        if tabwidget.count() > 1:
            tabwidget.tabBar().show()

    def close_document(self, index):
        """
        Closes a tab.

        No idea if there is more work needed to dispose the widgets and
        QtPoppler.Document that lived in this tab.
        """
        tabwidget = self.window.tabWidget

        tabwidget.removeTab(index)

        # When only one tab is displayed hide the tabBar.
        if tabwidget.count() < 2:
            tabwidget.tabBar().hide()

    def save_file(self):
        """ Save the current document. """
        pass

    def new_file(self):
        """ Create a new document. """
        self.open_document(PynalDocument(), "New Document")

    def quit(self):
        """ Exit the application. """
        pass

    def zoom_width(self):
        """ Zoom the current document to the width of the focused page. """
        document = self.window.tabWidget.currentWidget()
        width = document.viewport().width()
        newdpi = width / document.current_page().bg_source.sizeF().width() * Config.pdf_base_dpi
        newdpi = math.floor(newdpi)
        document.zoom(newdpi)

    def zoom_original(self):
        """
        Zoom the current document to 100%.
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        document.zoom(Config.pdf_base_dpi)

    def zoom_fit(self):
        """ Zoom the current document to fit the focused page. """
        document = self.window.tabWidget.currentWidget()
        height = document.height()
        newdpi = height / document.current_page().bg_source.sizeF().height() * Config.pdf_base_dpi
        newdpi = math.floor(newdpi)
        document.zoom(newdpi)

    def zoom_in(self):
        """
        Zoom in.
        TODO: Step depends on current scale or config.
        TODO: Zooming needs limits
        """
        document = self.window.tabWidget.currentWidget()
        document.zoom(document.dpi + 10)

    def zoom_out(self):
        """ Zoom out.
        TODO: Step depends on current scale or config.
        TODO: Zooming needs limits
        """
        document = self.window.tabWidget.currentWidget()
        document.zoom(document.dpi - 10)

    def set_tool_pen(self):
        """ Set the pen tool as the current tool. """
        tools.current_tool = tools.PenTool()

    def set_tool_scroll(self):
        """ Set the scroll tool as the current tool. """
        for i in range(self.window.tabWidget.count()):
            self.window.tabWidget.widget(i).setDragMode(
                          QtGui.QGraphicsView.ScrollHandDrag)
        tools.current_tool = tools.ScrollTool()

    def set_tool_select(self):
        """ Set the selection tool as the current tool. """
        for i in range(self.window.tabWidget.count()):
            self.window.tabWidget.widget(i).setDragMode(
                          QtGui.QGraphicsView.RubberBandDrag)
        tools.current_tool = tools.SelectTool()
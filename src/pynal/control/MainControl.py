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
        self.errorDialog = QtGui.QErrorMessage(window)

    def createActions(self):
        actionCollection = self.window.actionCollection()
        KStandardAction.openNew(self.new_file, actionCollection)
        KStandardAction.open(self.open_file, actionCollection)
        KStandardAction.save(self.save_file, actionCollection)
        KStandardAction.undo(self.undo, actionCollection)
        KStandardAction.redo(self.redo, actionCollection)

        KStandardAction.quit(self.quit, actionCollection)

    def start(self):
        """
        Called when the window has been set up and is ready to receive
        commands. E.g. opening documents.

        This can be extended to auto-reopen documents that were open
        when pynal was closed the last time.
        """
        args = KCmdLineArgs.parsedArgs()

        errors = ""
        for i in range(args.count()):
            filename = os.path.basename(str(args.arg(i)))
            if os.path.isfile(args.arg(i)):
                self.open_document(PynalDocument(args.arg(i)), filename)
            else:
                errors += args.arg(i) + "\n"

        if errors is not "":
            self.errorDialog.showMessage("Could not open file(s):\n" + errors)

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
                xournal = Xournal()
                xournal.load(file, document) 

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
        tabwidget = self.window.tabWidget
        document = tabwidget.currentWidget()
        if(document is not None):
            filename = KFileDialog.getSaveFileName(KUrl(), "*.xoj | *.xoj - Xournal File")
            xournal = Xournal()
            xournal.save(filename, document)

    def new_file(self):
        """ Create a new document. """
        self.open_document(PynalDocument(), "New Document")

    def quit(self):
        """ Exit the application. """
        pass

    def zoom_width(self):
        """
        Zoom the current document to the scene_ of the focused page.
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        scene_width = document.viewport().width()
        new_scale_value = scene_width / document.current_page().bg_source.sizeF().width()
        document.zoom(new_scale_value)

    def zoom_original(self):
        """
        Zoom the current document to 100%.
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        document.zoom(1)

    def zoom_fit(self):
        """
        Zoom the current document to fit the focused page.
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        scene_height = document.height()
        new_scale_value = scene_height / document.current_page().bg_source.sizeF().height()
#        newdpi = math.floor(newdpi)
        document.zoom(new_scale_value)

    def zoom_in(self):
        """
        Zoom in.
        TODO: Zooming needs limits
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        scale_level = document.scale_level
        document.zoom(scale_level + scale_level *  0.1)

    def zoom_out(self):
        """ Zoom out.
        TODO: Zooming needs limits
        TODO: Exception when no tab is open as currentWidget() will return None
        """
        document = self.window.tabWidget.currentWidget()
        scale_level = document.scale_level
        document.zoom(scale_level - scale_level *  0.1)

    def set_tool_pen(self):
        """ Set the pen tool as the current tool. """
        for i in range(self.window.tabWidget.count()):
            self.window.tabWidget.widget(i).setDragMode(
                          QtGui.QGraphicsView.NoDrag)
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

    def undo(self):
        """
        Undo the last action.
        """
        tabwidget = self.window.tabWidget
        document = tabwidget.currentWidget()
        document.undoStack.undo()

    def redo(self):
        """
        Redo the last undone action.
        """
        tabwidget = self.window.tabWidget
        document = tabwidget.currentWidget()
        document.undoStack.redo()

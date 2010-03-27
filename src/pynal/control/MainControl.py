# -*- coding: utf-8 -*-
"""
Module containing the MainWindowControl class.
"""
import os, math

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import KStandardAction, KAction, KIcon
from PyKDE4.kio import KFileDialog
from PyKDE4.kdecore import KUrl, KCmdLineArgs

import pynal.models.Config as Config
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
        #TODO: Move filter to a better place :D
        files = KFileDialog.getOpenFileNames(KUrl(), "*.pdf| PDF files")
        if not files:
            return

        for file in files:
            filename = os.path.basename(str(file))
            self.open_document(PynalDocument(file), filename)

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
        """
        Zoom the current document to the scene_ of the focused page.
        """
        document = self.window.tabWidget.currentWidget()
        if document is None:
            return
        scene_width = document.viewport().width()
        new_scale_value = scene_width / document.current_page().bg_source.sizeF().width()
        document.zoom(new_scale_value)

    def zoom_original(self):
        """
        Zoom the current document to 100%.
        """
        document = self.window.tabWidget.currentWidget()
        if document is None:
            return
        document.zoom(1)

    def zoom_fit(self):
        """
        Zoom the current document to fit the focused page.
        """
        document = self.window.tabWidget.currentWidget()
        if document is None:
            return
        scene_height = document.height()
        new_scale_value = scene_height / document.current_page().bg_source.sizeF().height()
#        newdpi = math.floor(newdpi)
        document.zoom(new_scale_value)

    def zoom_in(self):
        """
        Zoom in.
        TODO: Zooming needs limits
        """
        document = self.window.tabWidget.currentWidget()
        if document is None:
            return
        scale_level = document.scale_level
        document.zoom(scale_level + scale_level *  0.1)

    def zoom_out(self):
        """ Zoom out.
        TODO: Zooming needs limits
        """
        document = self.window.tabWidget.currentWidget()
        if document is None:
            return
        scale_level = document.scale_level
        document.zoom(scale_level - scale_level *  0.1)

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

    def set_tool_pen(self):
        """ Set the pen tool as the current tool. """
        for i in range(self.window.tabWidget.count()):
            self.window.tabWidget.widget(i).setDragMode(
                          QtGui.QGraphicsView.NoDrag)
        tools.current_tool = tools.PenTool()

    def undo(self):
        """
        Undo the last action.
        """
        tabwidget = self.window.tabWidget.currentWidget()
        if tabwidget is None:
            return

        tabwidget.undo_stack.undo()

    def redo(self):
        """
        Redo the last undone action.
        """
        tabwidget = self.window.tabWidget.currentWidget()
        if tabwidget is None:
            return

        tabwidget.undo_stack.redo()

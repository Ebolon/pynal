#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Prototype for a tabbed pdf viewer. Uses QGraphicsScenes in tabs to display the first
10 pages of pdf files.

Will be extended in future prototypes to a usable journal but not splitted into
several modules. A well structured form of this will be used as the fundament
for pynal.
'''
import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import QtPoppler

class MainWindow(QtGui.QMainWindow):
    """ The MainWindow containing the QTabWidget and MenuBar. """
    def __init__(self):
        """ Initialize the content of the window. """
        QtGui.QMainWindow.__init__(self)

        tabMenu = self.menuBar().addMenu("&Tabs")
        tabMenu.addAction(self.createAction("Open PDF", self.loadPDF))
        tabMenu.addAction(self.createAction("Rotate", self.rotate))

        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.connect(self.tabs, SIGNAL("tabCloseRequested(int)"), self.close)

        self.setCentralWidget(self.tabs)

        self.resize(500, 700)

    def createAction(self, text, slot):
        """ Convenience method to create actions for the menu. """
        action = QtGui.QAction(text, self)
        self.connect(action, SIGNAL("triggered()"), slot)
        return action

    def loadPDF(self):
        """
        Open a dialog to let the user choose pdf files and open
        them in tabs.
        """
        files = QtGui.QFileDialog.getOpenFileNames(self, "Open PDF file",
                                                    "", "PDF (*.pdf)")
        if not files:
            return

        for file in files:
            filename = os.path.basename(str(file))
            self.tabs.addTab(PynalDocument(file), filename)

    def rotate(self):
        """ Rotate the position of the tabs. """
        pos = (self.tabs.tabPosition() + 1) % 4
        self.tabs.setTabPosition(pos)

    def close(self, index):
        """
        Closes a tab.

        No idea if there is more work needed to dispose the widgets and
        QtPoppler.Document that lived in this tab.
        """
        self.tabs.removeTab(index)

class PynalDocument(QtGui.QGraphicsView):
    """ Document widget displayed in the QTabWidget. """

    def __init__(self, source_file, parent=None):
        """
        Create a new PynalDocument for the given file.

        parameters:
        source_file -- String path to the pdf that is to be displayed.
        parent -- the parent widget of this widget.
        """
        QtGui.QGraphicsView.__init__(self, parent)
        self.source = source_file
        self.document = QtPoppler.Poppler.Document.load(self.source)
        self.document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and
                                    QtPoppler.Poppler.Document.TextAntialiasing)

        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.thread = PdfLoaderThread(self.document, self.scene)
        self.connect(self.thread, SIGNAL("output(QImage, int)"), self.addPage)

        self.thread.start()
        print "Adding pages..."

    def addPage(self, image, i):
        """
        Callback method for the worker thread.

        Adds the created image as a pixmap to the scene.
        """
        pixmap = QtGui.QPixmap.fromImage(image)
        item = self.scene.addPixmap(pixmap)
        item.setOffset(0, i*1500)

class PdfLoaderThread(QtCore.QThread):
    """
    Creates QImages (or QPixmaps) from all pages in a given Poppler document.
    """
    def __init__(self, doc, scene):
        """
        Creates a new PdfLoaderThread.

        parameterss:
            doc - the QtPoppler.Poppler.Document that is to be loaded.
            scene - the QGraphicsScene that will receive the QImages.
        """
        QtCore.QThread.__init__(self)

        self.doc = doc
        self.scene = scene

    def run(self):
        """ Creates the images and notifies the QGraphicsScene. """
        for i in range(0, self.doc.numPages()):
            image = self.doc.page(i).renderToImage(150, 150)
            self.emit(SIGNAL("output(QImage, int)"), image, i)
            if i > 10:
                break

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

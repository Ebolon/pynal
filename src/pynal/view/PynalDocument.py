# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

import QtPoppler

import pynal.models.Config as Config
from pynal.view.DocumentPage import DocumentPage

class PynalDocument(QtGui.QGraphicsView):
    """ Document widget displayed in the QTabWidget. """

    def __init__(self, source_file=None, parent=None):
        """
        Create a new PynalDocument for the given file.

        Parameters:
        source_file -- String path to the pdf that is to be displayed.
        parent      -- the parent widget of this widget.
        """
        QtGui.QGraphicsView.__init__(self, parent)
        self.configure_scene()

        self.pages = []

        if source_file is not None:
            self.document = QtPoppler.Poppler.Document.load(source_file)
            self.document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and
                                        QtPoppler.Poppler.Document.TextAntialiasing)

            #This can be removed when DocumentPage objects work.
            self.thread = PdfLoaderThread(self.document, self.scene)
            self.connect(self.thread, SIGNAL("output(QImage, int)"), self.addPage)

            self.thread.start()

            # This might want to be moved into an own thread
            # (when numPages is over a certain threshold?)
            for i in range(0, self.document.numPages()):
                self.append_new_page(self.document.page(i))
                # Note that the pdf pages are not rendered
                # now. That happens when the page is to be
                # displayed / cached for displaying.

        else:
            self.append_new_page() # Add an empty page.

    def configure_scene(self):
        """ Create and configure the scene object. """
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(self.ScrollHandDrag) #TODO: should be moved when drawing is enabled.

    def append_new_page(self, bg_source=None):
        """
        Create an empty page and append it to the end of the document.
        """
        self.pages.append(DocumentPage(self, bg_source))


    def addPage(self, image, i):
        """
        Callback method for the worker thread.

        Adds the created image as a pixmap to the scene.

        TODO: This can be removed when DocumentPage objects work.
        """
        pixmap = QtGui.QPixmap.fromImage(image)
        item = self.scene.addPixmap(pixmap)
        item.setOffset(0, i*1500)

class PdfLoaderThread(QtCore.QThread):
    """
    Creates QImages from all pages in a given Poppler document.

    TODO: This can be removed when DocumentPage objects work.
    """
    def __init__(self, doc, scene):
        """
        Create a new PdfLoaderThread.

        parameters:
            doc - the QtPoppler.Poppler.Document that is to be loaded.
            scene - the QGraphicsScene that will receive the QImages.
        """
        QtCore.QThread.__init__(self)

        self.doc = doc
        self.scene = scene

    def run(self):
        """ Create the images and notify the QGraphicsScene. """
        for i in range(0, self.doc.numPages()):
            image = self.doc.page(i).renderToImage(Config.pdf_render_dpi,
                                                   Config.pdf_render_dpi)
            self.emit(SIGNAL("output(QImage, int)"), image, i)
            if i > 10:
                break

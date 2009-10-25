# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtOpenGL
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

        self.dpi = 72 * 2

        self.pages = []

        if Config.use_opengl:
            self.setViewport(QtOpenGL.QGLWidget())

        if source_file is not None:
            self.document = QtPoppler.Poppler.Document.load(source_file)
            self.document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and
                                        QtPoppler.Poppler.Document.TextAntialiasing)

            # This might want to be moved into an own thread
            # (when numPages is over a certain threshold?)
            for i in range(0, self.document.numPages()):
                if not self.pages:
                    self.append_new_page(bg_source=self.document.page(i))
                else:
                    self.append_new_page(self.pages[-1], self.document.page(i))

                # Note that the pdf pages are not rendered
                # now. That happens when the page is to be
                # displayed / cached for displaying.

        else:
            self.append_new_page() # Add an empty page.

    def zoom(self, value):
        self.dpi += value
        print "dpi now:", self.dpi
        for page in self.pages:
            page.update_bounding_rect()

        rect = QtCore.QRectF(self.pages[0].boundingRect().topLeft(),
                             self.pages[-1].boundingRect().bottomRight())

        self.scene.setSceneRect(rect)

    def configure_scene(self):
        """ Create and configure the scene object. """
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(self.ScrollHandDrag) #TODO: should be moved when drawing is enabled.

    def current_page(self):
        """
        The page that has the current focus. This can be the centered or
        last clicked page.
        """
        return self.items(self.contentsRect().center())[-1]

    def append_new_page(self, prevpage=None, bg_source=None):
        """
        Create an empty page and append it to the end of the document.
        """
        self.pages.append(DocumentPage(self, prevpage, bg_source))

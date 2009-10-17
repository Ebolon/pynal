# -*- coding: utf-8 -*-
'''
TODO: Seriously I should think about how I organize classes and modules.
Doing this the java way seems extremely stupid and redundant...
'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import pynal.models.Config as Config

class DocumentPage(QtGui.QGraphicsItem):
    """
    A page of a PynalDocument. Can have a background (like a
    page from a pdf) and contain QGraphicItems drawn by the user.

    Size is either specified by the size of the background image
    or the preceeding image.

    Attributes:
    background -- A rendered version of the background. Will be made
                  on demand. For example a QImage of the pdf page.
    bg_source  -- The source from which the background is created.
                  Can be the poppler document page that is to be
                  rendered.
    """

    def __init__(self, document, bg_source=None):
        QtGui.QGraphicsItem.__init__(self, None, document.scene)

        self.background = None
        self.bg_source = bg_source

    def boundingRect(self):
        """ Return the bounding box of the page. """
        return QtCore.QRectF()

    def paint(self, painter, option, widget=None):
        """
        Nothing to paint as all paintables are children if this item.

        This method is used as the notification to start rendering this
        page's background and pre-caching following/previous pages.
        """
        if self.background is None:
            #TODO: send poppler-render job to ThreadPool?
            self.loader = PdfLoaderThread(self)
            self.loader.connect(self.loader, SIGNAL("output(QImage)"), self.background_ready)
            self.loader.start()

            #TODO: call paint on previous/next page to pre-cache.
            pass
        else:
            pass

    def background_ready(self, image):
        self.loader = None #TODO: To destroy the thread object?
        self.background = image
        self.update()
        """ something like this:
        pixmap = QtGui.QPixmap.fromImage(image)
        item = self.scene.addPixmap(pixmap)
        item.setOffset(0, i*1500)
        """

class PdfLoaderThread(QtCore.QThread):
    """
    Create QImage for a given poppler page.

    TODO: I still don't like creating a new thread for every page.
    """
    def __init__(self, page):
        """
        Create a new PdfLoaderThread.

        parameters:
            doc - the QtPoppler.Poppler.Document that is to be loaded.
            scene - the QGraphicsScene that will receive the QImages.
        """
        QtCore.QThread.__init__(self)

        self.page = page

    def run(self):
        """ Create the images and notify the QGraphicsScene. """
        image = self.page.bg_source.renderToImage(Config.pdf_render_dpi,
                                                   Config.pdf_render_dpi)
        self.emit(SIGNAL("output(QImage)"), image)


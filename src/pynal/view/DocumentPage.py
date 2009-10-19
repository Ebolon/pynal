# -*- coding: utf-8 -*-
'''
TODO: Seriously I should think about how I organize classes and modules.
Doing this the java way seems extremely stupid and redundant...
'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import pynal.models.Config as Config
from pynal.control.threading import semaphore

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
    bounding   -- The boundingRect of this page. Usually specified
                  by the background_source.
    loader     -- The background generating thread of this page.
                  This is checked to be not None to prevent
                  the start of another thread to render the bg
                  which will result in a crash.
    """

    def __init__(self, document, prevpage=None, bg_source=None):
        QtGui.QGraphicsItemGroup.__init__(self, None, document.scene)

        self.background = None
        self.bg_source = bg_source

        if prevpage is None:
            top = 0
        else:
            top = prevpage.boundingRect().bottom() + 100

        size = QtCore.QSize(bg_source.pageSize().width()  * 2,
                            bg_source.pageSize().height() * 2)
        left_pos = -size.width() / 2
        self.bounding = QtCore.QRectF(QtCore.QPointF(left_pos, top),
                                      QtCore.QSizeF(size))

        self.loader = None

    def boundingRect(self):
        """ Return the bounding box of the page. """
        return self.bounding

    def paint(self, painter, option, widget=None):
        """
        Nothing to paint as all paintables are children of this item.

        This method is used as the notification to start rendering this
        page's background and pre-caching following/previous pages.
        """
        if self.background is None:
            if self.loader is not None:
                return

            #TODO: send poppler-render job to ThreadPool?
            self.loader = PdfLoaderThread(self)
            self.loader.connect(self.loader, SIGNAL("output(QImage)"), self.background_ready)
            self.loader.start()

            #TODO: call paint on previous/next page to pre-cache.
            pass
        else:
            pass

    def background_ready(self, image):
        """
        Callback method used by the PdfLoaderThread when the image is ready.
        Creates a pixmap, GraphicsPixmapItem and adds it to this group.
        """
        pixmap = QtGui.QPixmap.fromImage(image)
        self.background = pixmap
        item = QtGui.QGraphicsPixmapItem(pixmap, self)
        item.setCacheMode(item.DeviceCoordinateCache) #makes me feel warm inside
        item.setOffset(self.bounding.topLeft())
        item.setZValue(-1)
        self.loader = None

class PdfLoaderThread(QtCore.QThread):
    """
    Create QImage for a given poppler page.

    TODO: I still don't like creating a new thread for every page.
    """

    def __init__(self, page):
        """
        Create a new PdfLoaderThread.

        Parameters:
          page -- The DocumentPage that the bg is rendered for.
        """
        QtCore.QThread.__init__(self)
        self.page = page

    def run(self):
        """
        Create the background image and emit the
        signal that the image is ready.
        """
        semaphore.acquire()
        image = self.page.bg_source.renderToImage(Config.pdf_render_dpi_x,
                                                  Config.pdf_render_dpi_y)
        semaphore.release()
        self.emit(SIGNAL("output(QImage)"), image)


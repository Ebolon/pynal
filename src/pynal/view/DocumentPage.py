# -*- coding: utf-8 -*-
'''
TODO: Seriously I should think about how I organize classes and modules.
Doing this the java way seems extremely stupid and redundant...
'''
import math

from PyQt4 import QtCore
from PyQt4 import QtGui

import pynal.models.Config as Config
from pynal.control.threading import semaphore

class DocumentPage(QtGui.QGraphicsItem):
    """
    A page of a PynalDocument. Can have a background (like a
    page from a pdf) and contain QGraphicItems drawn by the user.

    Size is either specified by the size of the background image
    or the preceeding image.

    Attributes:
    document    -- The PynalDocument that contains this page.
    bg_source   -- The source from which the background is created.
                   Can be the poppler document page that is to be
                   rendered.
                   Reference kept to quickly exchange the pixmap for a new one.
    bounding    -- The boundingRect of this page. Usually specified
                   by the background_source.
    page_number -- The number of this page. Counting starts at 0
                   and is equal to this page's position in the
                   document's page list.
    loader      -- The background generating thread of this page.
                   This is checked to be not None to prevent
                   the start of another thread to render the bg
                   which will result in a crash.

    bg_graphics_item    -- The QGraphicsItem that contains the background pixmap.
    background_is_dirty -- Flag indicates that the background needs to
                           be re-rendered because the user zoomed or
                           something else made it unneeded.
    """

    def __init__(self, document, page_number, bg_source=None):
        QtGui.QGraphicsItemGroup.__init__(self, None, document.scene())

        self.document = document
        self.bg_source = bg_source
        self.bg_graphics_item = None
        self.page_number = page_number
        self._bounding = None
        self.update_bounding_rect()
        self.loader = None
        self.background_is_dirty = True

    def prevpage(self):
        """
        Return the previous page, or None when there is none.
        """
        try:
            return self.document.pages[self.page_number -1]
        except IndexError:
            return None

    def update_bounding_rect(self):
        """
        Update the bounding rect of this page.
        """
        if self.page_number == 0:
            top = 0
        else:
            space = 20 * self.document.dpi_scaling()
            top = self.prevpage().boundingRect().bottom() + space

        size = QtCore.QSize(math.ceil(self.bg_source.pageSize().width()  * self.document.dpi_scaling()),
                            math.ceil(self.bg_source.pageSize().height() * self.document.dpi_scaling()))
        left_pos = -size.width() / 2

        if self.boundingRect() is not None:
            """
            Find the scaling factor needed to transform
            the page to the needed size.
            Then scale, to transform all children so they stay
            where they are, relatively to the page.
            """
            newwidth = size.width()
            oldwidth = self.boundingRect().width()
            scale = newwidth / oldwidth
            self.scale(scale, scale)

        self._bounding = QtCore.QRectF(QtCore.QPointF(left_pos, top),
                                      QtCore.QSizeF(size))

        if self.bg_graphics_item is not None:
            p = self.bg_graphics_item.pixmap()
            self.bg_graphics_item.setPixmap(p.scaled(size))
            self.move_item_topleft()
            self.background_is_dirty = True

    def scale(self, x, y):
        """
        Reimplementation to prevent the background pixmaps from getting
        scaled. Scaling these Objects will result in an off scale value
        which will distort the re-rendered pdf pages.

        These must always be kept at a 1.0 scale.
        Background detection is done atm by checking the z-level of
        the child item. Background images should be in the back at -1.
        """
        for item in self.children():
            if item.zValue() != -1:
                item.scale(x, y)

    def boundingRect(self):
        """
        Return the bounding box of the page.
        Needed implementation for being a QGraphicsItem
        """
        return self._bounding

    def paint(self, painter, option, widget=None):
        """
        Nothing to paint as all paintables are children of this item.

        This method is used as the notification to start rendering this
        page's background and pre-caching following/previous pages.
        """
        if self.loader is not None:
                if self.loader.isFinished():
                    # New image can be generated.
                    self.loader = None
                else:
                    # Prevent image generation when a thread is still running.
                    return

        if self.background_is_dirty:
            #TODO: send poppler-render job to ThreadPool?
            self.loader = PdfLoaderThread(self, self.document.dpi)
            self.loader.output.connect(self.background_ready)
            self.loader.start()

            #TODO: call paint on previous/next page to pre-cache.
            pass
        else:
            pass


    def background_ready(self, new_image):
        """
        Callback method used by the PdfLoaderThread when the new_image is ready.
        Creates a pixmap, GraphicsPixmapItem and adds it to this page.

        TODO: send the image or a notification to the document to act as a
        central cache store that removes rendered pages at a certain threshold.
        """


        """
        When the rendered new_image does not fit (nearly) exactly in the current
        bounding box, it was an older job that finished. We need a new
        background.

        When the pixmap does get replaced with an unfit one, it creates a
        flickering of weird sized pages in the document.
        """
        if math.fabs(new_image.size().width() - self.boundingRect().size().width()) < 2 :
            self.background_is_dirty = False
        else:
            # Image does not fit. Don't replace the background pixmap.

            if self.isVisible():
                self.update() # To force a new call to paint().
            return

        # Replace the new_pixmap of the background with the new one.
        new_pixmap = QtGui.QPixmap.fromImage(new_image)
        if self.bg_graphics_item is None:
            self.bg_graphics_item = QtGui.QGraphicsPixmapItem(new_pixmap, self)
        else:
            self.bg_graphics_item.setPixmap(new_pixmap)

        self.move_item_topleft()
        self.bg_graphics_item.setZValue(-1)

    def move_item_topleft(self):
        """
        Move the background image to the top left of the
        bounding rect.

        This should be done as a translation transformation
        to move all children correctly.
        """
        self.bg_graphics_item.setOffset(self.boundingRect().topLeft())

class PdfLoaderThread(QtCore.QThread):
    """
    Create QImage for a given poppler page.

    TODO: I still don't like creating a new thread for every page.
    """

    """ Signal to emit when a QImage has been rendered. """
    output = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, page, dpi):
        """
        Create a new PdfLoaderThread.

        Parameters:
          page -- The DocumentPage that the bg is rendered for.
        """
        QtCore.QThread.__init__(self)
        self.page = page
        self.dpi = dpi

    def run(self):
        """
        Create the background image and emit the
        signal that the image is ready.
        """
        semaphore.acquire()
        size = self.page.bg_source.pageSizeF()
        factor = self.dpi / 72.0
        image = self.page.bg_source.renderToImage(self.dpi, self.dpi)
        size = self.page.boundingRect().size()
        self.output.emit(image)
        semaphore.release()

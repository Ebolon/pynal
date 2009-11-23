# -*- coding: utf-8 -*-
'''
This module contains the class definition and convenience methods
to create BackgroundImage objects that can be used as the bg_source
for a PynalDocument. These are similiar to the QtPoppler.Poppler.Page
but don't use a PDF as the backend.

Possible uses are images or patterns for graph or lined paper.
'''
import math

from PyQt4 import QtCore
from PyQt4 import QtGui

from pynal.control.threading import semaphore
import pynal.models.Config as Config

def empty_background(size=None):
    """
    Create and configure a bg_source for a plain
    and empty page.
    """
    bg = PlainBackground(size)
    return bg

def checked_background(size=None):
    bg = CheckedBackground(size)
    return bg

def pdf_page(popplerpage):
    return PdfBackground(popplerpage)

class BackgroundImage():
    """
    Used as a bg_source by the DocumentPage to present a
    single image (or style).
    """

    def __init__(self, size):
        self.setSizeF(size)

    def sizeF(self):
        """
        Return the size of the background or None if the bg
        does not have a preferred size.
        """
        return self.size

    def setSizeF(self, size):
        """ Set the QSizeF of this bg. """
        self.size = size

    def get_image(self, dpi, callback):
        """
        Create an image of this bg that can be displayed,
        and call the callback with the QImage.
        Actually only the pixmap is needed, but that should be
        extracted from the QImage in the GUI-thread.

        Parameters:
          dpi      -- The dpi to render the image with.
          callback -- The method to deliver the generated image.
        """
        pass

    def ready_to_render(self):
        """ Always ready to re-render the bg. """
        return True

class PdfBackground(BackgroundImage):

    def __init__(self, poppler):
        self.poppler = poppler
        self.loader = None
        self.setSizeF(self.poppler.pageSizeF())

    def get_image(self, dpi, callback):
        """
        Create a new render thread and start it.
        """
        self.loader = PdfRenderThread(self.poppler, dpi)
        self.loader.output.connect(callback)
        self.loader.start()

    def ready_to_render(self):
        """
        Check if it is possible to render the bg.

        Return:
          True  -- The background can be rendered.
          False -- The bg cannot be rendered now. A reason for this might be
                   that there is still a thread running which needs to finish first.
                   Or there is just not a need to create a new image.
        """
        if self.loader is not None:
            if self.loader.isFinished():
                # New image can be generated.
                self.loader = None
                return True
            else:
                # Prevent image generation when a thread is still running.
                return False
        else:
            return True

class PlainBackground(BackgroundImage):
    """
    An empty background of a given color.
    """

    def __init__(self, size, brush=QtCore.Qt.white):
        """
        Create a new plain background.

        Parameters:
          brush -- The Color to use for the background
        """
        BackgroundImage.__init__(self, size)
        self.brush = brush

    def get_image(self, dpi, callback):
        """
        A pixmap can be directly created here as this is done in the GUI-Thread
        instead of a dedicated one.

        And creating a white pixmap is easier than creating a QImage first and then
        extract the pixmap.
        """
        factor = dpi / Config.pdf_base_dpi #TODO: get factor from document
        pixmap = QtGui.QPixmap(QtCore.QSize(self.sizeF().width()  * factor,
                                            self.sizeF().height() * factor))
        pixmap.fill(self.brush)
        callback(pixmap)

class CheckedBackground(BackgroundImage):
    """
    A background with boxes :D
    """

    def __init__(self, size, brush=QtCore.Qt.white):
        """
        Create a checked background.

        Parameters:
          brush -- The Color to use for the background
        """
        BackgroundImage.__init__(self, size)
        self.brush = brush

    def setSizeF(self, sizef):
        BackgroundImage.setSizeF(self, sizef)
        if self.sizeF() is not None:
            self.cols = int(math.floor(self.sizeF().width() / Config.get_int("checked background", "size"))) #TODO: move to config
            self.rows = int(math.floor(self.sizeF().height() / Config.get_int("checked background", "size")))

    def get_image(self, dpi, callback):
        """
        A pixmap can be directly created here as this is done in the GUI-Thread
        instead of a dedicated one.

        And creating a white pixmap is easier than creating a QImage first and then
        extract the pixmap.
        """
        factor = dpi / Config.pdf_base_dpi #TODO: get factor from document
        pixmap = QtGui.QPixmap(QtCore.QSize(self.sizeF().width()  * factor,
                                            self.sizeF().height() * factor))
        pixmap.fill(self.brush)

        painter = QtGui.QPainter(pixmap)
        painter.setPen(Config.checked_line_color)

        square_size = pixmap.width() / self.cols
        for i in range(1, self.cols + 1):
            x = i * square_size
            painter.drawLine(x, 0, x, pixmap.height())

        for i in range(1, self.rows + 1):
            y = i * square_size
            painter.drawLine(0, y, pixmap.width(), y)

        painter.end()

        callback(pixmap)

class PdfRenderThread(QtCore.QThread):
    """
    Create QImage for a given poppler page.

    TODO: I still don't like creating a new thread for every page.
    """

    """ Signal to emit when a QImage has been rendered. """
    output = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, page, dpi):
        """
        Create a new PdfRenderThread.

        Parameters:
          page -- The DocumentPage that the bg is rendered for.
          dpi  -- The dpi to render with.
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
        image = self.page.renderToImage(self.dpi, self.dpi)
        self.output.emit(image)
        semaphore.release()

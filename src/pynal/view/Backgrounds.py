# -*- coding: utf-8 -*-
'''
This module contains the class definition and convenience methods
to create BackgroundImage objects that can be used as the bg_source
for a PynalDocument. These are similiar to the QtPoppler.Poppler.Page
but don't use a PDF as the backend.

Possible uses are images or patterns for graph or lined paper.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

from pynal.control.threading import semaphore
import pynal.models.Config as Config

def empty_background():
    """
    Create and configure a bg_source for a plain
    and empty page.
    """
    bg = BackgroundImage()
    return bg

def pdf_page(popplerpage):
    return PdfBackground(popplerpage)

class BackgroundImage():
    """
    Used as a bg_source by the DocumentPage to present a
    single image (or style). Functions resemble the API
    of QtPoppler.Poppler.Page so no typechecking is
    necessary when working with these objects.
    """

    def __init__(self):
        pass

    def pageSizeF(self):
        pass

    def get_image(self, dpix, dpiy):
        pass

    def ready_to_render(self):
        return True

class PdfBackground(BackgroundImage):

    def __init__(self, poppler):
        self.poppler = poppler
        self.loader = None

    def pageSizeF(self):
        return self.poppler.pageSizeF()

    def get_image(self, page, dpi):
        """
        Create an image of this bg that can be displayed.
        Actually only the pixmap is needed, but that should be
        extracted from the QImage in the GUI-thread.

        TODO: this is a lazy and adapted copy of the code that
              lived in DocumentPage. Parameters and object calling
              should be optimized to the new location.

        Parameters:
          page -- The DocumentPage that needs the image as its bg.
          dpi  -- The dpi to render the image with.

        Return:
          QtGui.QImage
        """
        self.loader = PdfRenderThread(page, dpi)
        self.loader.output.connect(page.background_ready)
        self.loader.start()

    def ready_to_render(self):
        """
        Check if it is possible to render the bg.

        Return:
          True  -- The background can be rendered.
          False -- The bg cannot be rendered now. A reason for this might be
                   that there is still a thread running which needs to finish first.
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

class PdfRenderThread(QtCore.QThread):
    """
    Create QImage for a given poppler page.

    TODO: I still don't like creating a new thread for every page.
          This might fit nicely in the Backgrounds class or a wrapper for the
          Poppler.Page object.
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

        TODO: the calculation is not clear and has to be moved somewhere else.
        """
        semaphore.acquire()
        image = self.page.bg_source.poppler.renderToImage(self.dpi, self.dpi)
        self.output.emit(image)
        semaphore.release()
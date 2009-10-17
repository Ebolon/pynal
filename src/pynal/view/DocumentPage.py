# -*- coding: utf-8 -*-
'''
TODO: Seriously I should think about how I organize classes and modules.
Doing this the java way seems extremely stupid and redundant...
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

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
        """
        pass

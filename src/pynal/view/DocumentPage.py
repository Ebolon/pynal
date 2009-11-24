# -*- coding: utf-8 -*-
'''
TODO: Seriously I should think about how I organize classes and modules.
Doing this the java way seems extremely stupid and redundant...
'''
import math

from PyQt4 import QtCore
from PyQt4 import QtGui

import pynal.models.Config as Config
from pynal.view.PageControl import PageControl

class DocumentPage(QtGui.QGraphicsItem):
    """
    A page of a PynalDocument. Can have a background (like a
    page from a pdf) and contain QGraphicItems drawn by the user.

    Size is either specified by the size of the background image
    or the preceding image.

    Attributes:
    document    -- The PynalDocument that contains this page.
    bg_source   -- The source from which the background is created.
                   Can be the poppler document page that is to be
                   rendered.
                   Reference kept to quickly exchange the pixmap for a new one.
    _bounding   -- The boundingRect of this page. Usually specified
                   by the background_source.
                   Marked private to underline that access to this should always
                   go over boundingRect().
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
        self.control_panel = PageControl(self)
        self.loader = None
        self.background_is_dirty = True

        self.update_bounding_rect()

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
            space = Config.min_space_between_pages * self.document.dpi_scaling()

            # Make enough Space for the page control of the previous page.
            space += self.prevpage().control_panel.sizeF().height()

            top = self.prevpage().boundingRect().bottom() + space

        # Determine the size this page in dots
        # Take the preferred size of the bg
        bg_size = self.bg_source.sizeF()

        if bg_size is None: # When the bg has no preference
            if self.page_number > 0:
                bg_size = QtCore.QSizeF(self.prevpage().bg_source.sizeF())
            else:
                bg_size = QtCore.QSizeF(Config.page_size_A4)

            self.bg_source.setSizeF(bg_size)

        # Transform from dots to pixels according to the current zoom/dpi-setting.
        size = QtCore.QSize(math.ceil(bg_size.width()  * self.document.dpi_scaling()),
                            math.ceil(bg_size.height() * self.document.dpi_scaling()))

        # Move to the left by half width so center is on y-axis of scene.
        left_pos = -size.width() / 2

        if self.boundingRect() is not None:
            """
            Find the scaling factor needed to transform
            the page to the needed size.
            Then scale, to transform all children so they stay
            where they are relative to the page.
            """
            newwidth = size.width()
            oldwidth = self.boundingRect().width()
            scale = newwidth / oldwidth
            self.scale(scale, scale)
        else:
            # Create the rect once...
            self._bounding = QtCore.QRectF()

        # ...and change its properties to update it.
        self._bounding.setTopLeft(QtCore.QPointF(left_pos, top))
        self._bounding.setSize(QtCore.QSizeF(size))

        self.control_panel.update_bounding_rect()

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
            if item.zValue() > 0:
                item.scale(x, y)

    def boundingRect(self):
        """
        Return the bounding box of the page.
        """
        return self._bounding

    def paint(self, painter, option, widget=None):
        """
        Nothing to paint as all paintables are children of this item.

        This method is used as the notification to start rendering this
        page's background and pre-caching following/previous pages.
        """
        if not self.bg_source.ready_to_render():
            return

        if self.background_is_dirty:
            self.bg_source.get_image(self.document.dpi, self.background_ready)

            #TODO: call paint on previous/next page to pre-cache.
            pass
        else:
            pass


    def background_ready(self, result):
        """
        Callback method for the bg_source to bring the rendered background to.
        Creates/Uses the given pixmap as a new background for this page.

        TODO: send the image or a notification to the document to act as a
        central cache store that removes rendered pages at a certain threshold.

        Parameters:
          result -- QImage or QPixmap.
        """


        """
        When the rendered result does not fit (nearly) exactly in the current
        bounding box, it was an older job that finished. We need a new
        background.

        When the pixmap does get replaced with an unfit one, it creates a
        flickering of weird sized pages in the document.
        """
        if math.fabs(result.size().width() - self.boundingRect().size().width()) < 2 :
            self.background_is_dirty = False
        else:
            # Image does not fit. Don't replace the background pixmap.

            if self.isVisible():
                self.update() # To force a new call to paint().
            return

        # Replace the new_pixmap of the background with the new one.
        if type(result) is QtGui.QImage:
            new_pixmap = QtGui.QPixmap.fromImage(result)
        else:
            new_pixmap = result

        if self.bg_graphics_item is None:
            self.bg_graphics_item = QtGui.QGraphicsPixmapItem(new_pixmap, self)
        else:
            self.bg_graphics_item.setPixmap(new_pixmap)

        self.move_item_topleft()
        self.bg_graphics_item.setZValue(-1) #TODO: move to constant or config

    def move_item_topleft(self):
        """
        Move the background image to the top left of the
        bounding rect.

        This should be done as a translation transformation
        to move all children correctly.
        """
        self.bg_graphics_item.setOffset(self.boundingRect().topLeft())

    def append(self):
        """ Append a new page after this. """
        self.document.insert_new_page_after(self.page_number, self.bg_source)

    def move_down(self):
        """
        Move this page below the page after this.
        """
        if self.page_number == len(self.document.pages) - 1:
            return
        self.document.switch_pages(self.page_number, self.page_number + 1)

    def move_up(self):
        """ Move this page on top of the one over this. """
        if self.page_number == 0:
            return
        self.document.switch_pages(self.page_number, self.page_number - 1)

    def remove(self):
        """ Remove this page. """
        self.document.remove_page(self.page_number)

    def duplicate(self):
        """ Insert a duplicate of this page below it. """
        pass

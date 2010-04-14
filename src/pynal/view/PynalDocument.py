# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtOpenGL

import math

from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
import QtPoppler

import pynal.control.tools as tools
import pynal.models.Config as Config
import pynal.view.Backgrounds as Backgrounds
from pynal.models.PynalCache import PynalCache
from pynal.view.DocumentPage import DocumentPage

class PynalDocument(QtGui.QGraphicsView):
    """
    Document widget displayed in the QTabWidget.

    Attributes:
    scale_level -- The current dpi used to render the background of pages.
    pages       -- The list of DocumentPage objects of this document.
    document    -- The Poppler Document used as the background
                   source.
    undo_stack  -- The undo stack for this document.
    """

    def __init__(self, source_file=None, parent=None):
        """
        Create a new PynalDocument for the given file.

        Parameters:
        source_file -- String path to the pdf that is to be displayed.
        parent      -- the parent widget of this widget.
        """
        QtGui.QGraphicsView.__init__(self, parent)
        self.max_width = -1
        self.setCursor(tools.current_tool.cursor)

        # Needed for proper rendering of selection box
        #self.setViewportUpdateMode(self.FullViewportUpdate)

        self.configure_scene()

        # Set the default zoom level to 1.0
        self.scale_level = 1

        self.pages = []
        
        self.undoStack = QtGui.QUndoStack(self)


        if Config.get_group("rendering").readEntry("use_opengl", False).toBool():
            self.setViewport(QtOpenGL.QGLWidget())


        if source_file is not None:
            self.document = QtPoppler.Poppler.Document.load(source_file)
            self.document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and
                                        QtPoppler.Poppler.Document.TextAntialiasing)

            # This might want to be moved into an own thread
            # (when numPages is over a certain threshold?)
            for page_number in range(0, self.document.numPages()):
                self.insert_new_page_at(page_number,
                    Backgrounds.pdf_page(self.document.page(page_number)))

                # Note that the pdf pages are not rendered
                # now. That happens when the page is to be
                # displayed / cached for displaying.

        else:
            self.insert_new_page_at(0) # Add an empty page.

        self.undo_stack = kdeui.KUndoStack(self)

        self.removed_pages = []

        # Toolbar
        toolbar = QtGui.QToolBar()

        # Actions
        self.actionAdd = toolbar.addAction("New", self.refresh_viewport_size)
        self.actionEdit = toolbar.addAction("Edit", self.refresh_viewport_size)
        self.actionDelete = toolbar.addAction("Delete", self.refresh_viewport_size)
        
        self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

        # Popup Menu
        self.popMenu = QtGui.QMenu(self)
        self.popMenu.addAction( self.actionEdit )
        self.popMenu.addAction( self.actionDelete )
        self.popMenu.addSeparator()
        self.popMenu.addAction( self.actionAdd )
        
        self.cache = PynalCache()

    def on_context_menu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))
        print "hu"
        

    def refresh_viewport_size(self):
        """
        Extend or shrink the viewport's size to show all pages and not more than needed.
        This stretches from the top-left of the first page (or its control) to the
        bottom right page (page's control).
        """
        lastpage = self.pages[-1]
        bottom = lastpage.sceneBoundingRect().bottomRight()
        bottom.setY(bottom.y() + lastpage.control_panel.sizeF().height())

        """
        When max_width is set to -1, the current max width is unknown and has to be determined.
        """
        if self.max_width == -1:
            for page in self.pages:
                if page.boundingRect().width() > self.max_width:
                    self.max_width = page.boundingRect().width()

        rect = QtCore.QRectF(self.max_width / -2, 0, self.max_width, bottom.y())
        return self.scene().setSceneRect(rect)

    def zoom(self, value):
        """
        Set the relative scale of this document (1 = 100%).
        """
        if self.scale_level == value:
            return
        self.scale_level = value
        print "Scaling now:", self.scale_level
        for page in self.pages:
            page.update_bounding_rect() # TODO: send scale_changed_event /signal

        self.refresh_viewport_size()

    def configure_scene(self):
        """ Create and configure the scene. """
        self.setScene(QtGui.QGraphicsScene(self))
        self.scene().setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setRenderHint(QtGui.QPainter.Antialiasing)

    def get_page(self, number):
        """ Page by number """
        #TODO: safety?
        return self.pages[number]

    def get_pages(self):
        """ Pages """
        return self.pages

    def current_page(self):
        """
        The page that is in the current focus.
        Uses the relative position of the vertical scrollbar to calculate
        the page the user is probably looking at.

        Works best with documents where every page is the
        same size.
        """
        relative_toolbar_pos = float(self.verticalScrollBar().value()) / \
                                     self.verticalScrollBar().maximum()

        current_page = math.floor(len(self.pages) * relative_toolbar_pos)

        return self.pages[int(current_page)]

    def insert_new_page_at(self, index, bg_source=None):
        """
        Insert a new page at the given index.

        Parameters:
          index     -- Index/site number that this page will have.

          bg_source -- The bg_source for this page. None results in a blank page.
        """
        if bg_source is None:
            bg_source = Backgrounds.empty_background()

        new_page = DocumentPage(self, index, bg_source)
        if new_page.boundingRect().width() > self.max_width:
           self.max_width = new_page.boundingRect().width()

        self.pages.insert(index, new_page)

        # Move all pages after this down to accommodate it.
        for i in range(index + 1, len(self.pages)):
            self.pages[i].page_number = i
            self.pages[i].update_bounding_rect()

        self.refresh_viewport_size()

    def insert_new_page_after(self, index, bg_source=None):
        """
        Insert a new page after the page at the given index.
        This is a convenience method for insert_new_page_at.

        Parameters:
          index     -- Index/site number of the page that will precede this.

          bg_source -- The bg_source for this page. None results in a blank page.
        """
        self.insert_new_page_at(index + 1, bg_source)

    def mouseDoubleClickEvent(self, event):
        """
        Delegate the mouse events to the current tool.
        Event is also delegated to super to handle the event in case
        the tool calls event.ignore().
        """
        tools.current_tool.mouseDoubleClickEvent(event, self)
        QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        """
        Delegate the mouse events to the current tool.
        Event is also delegated to super to handle the event in case
        the tool calls event.ignore().
        """
        tools.current_tool.mouseMoveEvent(event, self)
        QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        """
        Delegate the mouse events to the current tool.
        Event is also delegated to super to handle the event in case
        the tool calls event.ignore().
        """
        tools.current_tool.mousePressEvent(event, self)
        QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """
        Delegate the mouse events to the current tool.
        Event is also delegated to super to handle the event in case
        the tool calls event.ignore().
        """
        tools.current_tool.mouseReleaseEvent(event, self)
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)

    def tabletEvent(self, event):
        """
        Delegate the tablet event to the current tool.
        Event is also delegated to super to handle the event in case
        the tool calls event.ignore().
        """
        event.accept()
        tools.current_tool.tabletEvent(event, self)
        #QtGui.QGraphicsView.tabletEvent(self, event)

    def switch_pages(self, index_a, index_b):
        """
        Switch the pages with the given indexes.

        Parameters:
          index_a -- page_number of one page
          index_b -- page_number of the other :D
        """
        if index_a > index_b:
            index_a, index_b = index_b, index_a

        pages = self.pages
        pages[index_a], pages[index_b] = pages[index_b], pages[index_a]

        pages[index_a].page_number = index_a
        pages[index_b].page_number = index_b
        pages[index_a].update_bounding_rect()
        pages[index_b].update_bounding_rect()

    def remove_page(self, index):
        """
        Delete the page at the given index.

        TODO: Page is removed from the scene but the data is not removed.
              A reference has to be kept or the program crashes. The reason
              for this is still under investigation. ->#15
        """
        pages = self.pages
        page_remove = pages[index]
        pages.remove(page_remove)
        self.scene().removeItem(page_remove)
        for i in range(index, len(pages)):
            pages[i].page_number = i
            pages[i].update_bounding_rect()

        self.removed_pages.append(page_remove)

        """
        When this page might have been the widest, set the maximum width to unknown.
        So it is recalculated when needed.
        """
        if page_remove.boundingRect().width() == self.max_width:
            self.max_Width = -1

        self.refresh_viewport_size()

    def page_at(self, point):
        """
        Returns the page at the given coordinate (scene-coordinate).
        Used to filter out other objects that are found in the scene.

        Returns None when no page is found at the given coordinate.
        """
        if not self.pages:
            return None

        for item in self.scene().items(point):
            if item.type() == DocumentPage.TYPE_DOCUMENT_PAGE:
                return item

        return None

# -*- coding: utf-8 -*-
'''
'''
from PyQt4 import QtGui
from PyQt4 import QtCore

import pynal.control.actions as actions
import pynal.models.iconcache as iconcache
import pynal.models.Config as Config

class PageControl(QtGui.QGraphicsItem):
    '''

    '''

    def __init__(self, parent):
        '''

        '''
        QtGui.QGraphicsItem.__init__(self, parent)
        self.setZValue(0)

        self._bounding = None
        self._buttons = None

    def add_buttons(self):
        self._buttons = []
        insert_below = PageButton(self, actions.toolbar("new_file_action"))
        self._buttons.append(insert_below)

    def update_bounding_rect(self):
        """
        Move the panel to the bottom of the page.
        Called after the page has been resized due to a zoom event
        and the physical size in the scene has changed so the panel
        has to be relocated.
        """
        self._bounding = QtCore.QRectF(-100, self.parentItem().boundingRect().bottom(),
                                        200, Config.page_panel_height)

    def boundingRect(self):
        """
        Return the bounding box of the control panel.
        """
        return self._bounding

    def paint(self, painter, option, widget=None):
        """
        Nothing to paint as all paintables are children of this item.

        This method is used as the notification to start rendering this
        page's background and pre-caching following/previous pages.
        """
        if self._buttons is None:
            self.add_buttons()

        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.setPen(QtCore.Qt.white)
        painter.drawRect(self.boundingRect())

class PageButton(QtGui.QGraphicsWidget):

    def __init__(self, parent, action):
        QtGui.QGraphicsWidget.__init__(self, parent)
        self.addAction(action)
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setAcceptsHoverEvents(True)
        self.setHandlesChildEvents(True)

        parent_rect = parent.boundingRect()
        top = parent_rect.top() + 5
        left = parent_rect.left() + 50
        self._bounding = QtCore.QRectF(0, top, 20, 20)

        pixmap = self.actions()[0].icon().pixmap(self.boundingRect().size().width(),
                                                 self.boundingRect().size().height())
        self.icon = QtGui.QGraphicsPixmapItem(pixmap, self)
        self.icon.setOffset(self.boundingRect().topLeft())

    def paint(self, painter, option, widget=None):
        painter.drawRect(self.boundingRect())

    def boundingRect(self):
        return self._bounding

    def mousePressEvent(self, event):
        print "asd!"

    def hoverMoveEvent(self, event):
        print "move"

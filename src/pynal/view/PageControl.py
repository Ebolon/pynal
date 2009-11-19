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

        toolbar = QtGui.QToolBar("page controls")
        #TODO: page specific actions needed here.
        toolbar.addAction(actions.toolbar("page_new_after", callable=self.append))
        toolbar.addAction(actions.toolbar("page_up", callable=self.move_up))
        toolbar.addAction(actions.toolbar("page_down", callable=self.move_down))
        toolbar.addAction(actions.toolbar("page_remove", callable=self.remove))
        toolbar.addAction(actions.toolbar("page_duplicate", callable=self.duplicate))

        #TODO: at this point there are no boundingRects for self and parent
        toolbar_item = QtGui.QGraphicsProxyWidget(self)
        toolbar_item.setWidget(toolbar)
        self.toolbar = toolbar_item

    def append(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def remove(self):
        pass

    def duplicate(self):
        pass

    def update_bounding_rect(self):
        """
        Move the panel to the bottom of the page.
        Called after the page has been resized due to a zoom event
        and the physical size in the scene has changed so the panel
        has to be relocated.
        """
        self._bounding = QtCore.QRectF(-100, self.parentItem().boundingRect().bottom(),
                                        200, Config.page_panel_height)

        if self.toolbar is not None:
            self.toolbar.setPos(-self.toolbar.boundingRect().width() / 2,
                                 self.boundingRect().top())

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
        if self.toolbar is None:
            self.add_buttons()

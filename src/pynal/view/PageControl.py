# -*- coding: utf-8 -*-
'''
'''
from PyQt4 import QtGui
from PyQt4 import QtCore

import pynal.control.actions as actions
import pynal.models.iconcache as iconcache
import pynal.models.Config as Config
import pynal.view.Backgrounds as Backgrounds

class PageControl(QtGui.QGraphicsItem):
    '''
    A control panel/toolbar below every page for quick access to
    page manipulation and management actions.
    '''

    def __init__(self, parent):
        '''
        Creates a new PageControl for the given page.

        Parameters:
          parent -- The DocumentPage that is controlled by this panel.
        '''
        QtGui.QGraphicsItem.__init__(self, parent)
        self.setZValue(0)
        self._bounding = None
        self.toolbar = None

        toolbar = QtGui.QToolBar("page controls")

        toolbar.addAction(actions.toolbar("page_new_after", callable=self.append))
        toolbar.addAction(actions.toolbar("page_up", callable=self.move_up))
        toolbar.addAction(actions.toolbar("page_down", callable=self.move_down))
        toolbar.addAction(actions.toolbar("page_remove", callable=self.remove))
        toolbar.addAction(actions.toolbar("page_duplicate", callable=self.duplicate))
        toolbar.addSeparator()
        toolbar.addAction(actions.toolbar("page_bg_plain", callable=self.plain_bg))
        toolbar.addAction(actions.toolbar("page_bg_checked", callable=self.checked_bg))
        self.toolbar_widget = toolbar

    def reposition_toolbar(self):
        """ Move the toolbar QGraphicsProxyItem below the page. """
        return self.toolbar.setPos(-self.toolbar.boundingRect().width() / 2, self.boundingRect().top())

#        Toolbar can also be left or right aligned.
#        return self.toolbar.setPos(self.parentItem().boundingRect().left(), self.boundingRect().top())
#        return self.toolbar.setPos(
#                    self.parentItem().boundingRect().right() - self.toolbar.boundingRect().width(),
#                    self.boundingRect().top())


    def append(self):
        """ Append a new page after this one. """
        self.parentItem().append()

    def move_up(self):
        """ Move this page above the previous page. """
        self.parentItem().move_up()

    def move_down(self):
        """ Move this page below the next page. """
        self.parentItem().move_down()

    def remove(self):
        """ Remove this page. """
        pass

    def duplicate(self):
        """ Insert a duplicate of this page below it. """
        pass

    def plain_bg(self):
        """ Set the background to plain. """
        parent = self.parentItem()
        parent.bg_source = Backgrounds.empty_background(size=parent.bg_source.sizeF())
        parent.background_is_dirty = True

    def checked_bg(self):
        """ Set the background to checked. """
        pass

    def update_bounding_rect(self):
        """
        Move the panel to the bottom of the page.
        Called after the page has been resized due to a zoom event
        and the physical size in the scene has changed so the panel
        has to be relocated.
        """

        #TODO: these values and the whole bounding_rect should be related to the toolbar
        self._bounding = QtCore.QRectF(-100, self.parentItem().boundingRect().bottom(),
                                        200, 30)

        if self.toolbar is not None:
            self.reposition_toolbar()

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
            toolbar_item = QtGui.QGraphicsProxyWidget(self)
            toolbar_item.setWidget(self.toolbar_widget)
            self.toolbar = toolbar_item
            self.reposition_toolbar()

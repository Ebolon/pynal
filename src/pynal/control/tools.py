'''
Contains the current tool and its configuration and the class definitions for different tools.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from math import hypot

import pynal.view.Item as Item

class Tool():
    '''
    Base class of all tools.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cursor = QtCore.Qt.ArrowCursor

    def mouseDoubleClickEvent(self, event, document):
        """
        Process the event of a double click.
        TODO: The dclick might be useful to display a quick menu.
        """
        event.ignore()

    def mouseMoveEvent(self, event, document):
        """ Process the event of the mouse moving. """
        event.ignore()

    def mousePressEvent(self, event, document):
        """ Process the event of a pressed mouse key. """
        event.ignore()

    def mouseReleaseEvent(self, event, document):
        """ Process the event of a released mouse key. """
        event.ignore()

    def tabletEvent(self, event, document):
        """ Process the event of a tablet event. """
        event.ignore()

class ScrollTool(Tool):
    """
    The scroll tool. Not a full fledged tool as the pen or others as the
    functionality is provided by the QGraphicsView.
    """

    def __init__(self):
        Tool.__init__(self)

class SelectTool(Tool):
    """
    The selection tool. As small as the scroll tool as the logic
    is provided by the QGraphicsView.

    TODO: might want to merge with the scroll tool.
    """

    def __init__(self):
        Tool.__init__(self)

class PenTool(Tool):
    """
    The pen tool.
    """
    def __init__(self):
        Tool.__init__(self)
        self.Line = None
        self.deviceDown = False
        self.lastPoint = None
        self.tabletActive = False
        
    def mousePressEvent(self, event, document):
        self.deviceDown = True
        point_coords = document.mapToScene(event.pos())
        page = document.page_at(point_coords)
        if page is not None:
            self.Line = Item.Line(document, point_coords)
            document.scene().addItem(self.Line)
            self.Line.setParentItem(page)
            self.Line.setZValue(1)
            self.lastPoint = point_coords

    def mouseReleaseEvent(self, event, document):
        self.Line = None
        self.deviceDown = False

    def mouseMoveEvent(self, event, document):
        if not self.deviceDown:
            return
        if self.Line is not None:
            point_coords = document.mapToScene(event.pos())
            x, y = abs(point_coords.x() - self.lastPoint.x()), abs(point_coords.y() - self.lastPoint.y())
            if((x + y) * 0.8 > 3):
                self.Line.addPoint(point_coords)
                self.lastPoint = point_coords

current_tool = Tool()
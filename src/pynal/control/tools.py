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
        
    def mouseDoubleClickEvent(self, event, scene):
        """
        Process the event of a double click.
        TODO: The dclick might be useful to display a quick menu.
        """
        event.ignore()

    def mouseMoveEvent(self, event, scene):
        """ Process the event of the mouse moving. """
        event.ignore()

    def mousePressEvent(self, event, scene):
        """ Process the event of a pressed mouse key. """
        event.ignore()

    def mouseReleaseEvent(self, event, scene):
        """ Process the event of a released mouse key. """
        event.ignore()

    def tabletEvent(self, event, view):
        """ Process the event of a tablet event. """
        event.ignore()
    
    def mapToPage(self, point):
        return QtCore.QPointF(self.view.mapToScene(point))


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
        self.Page = None
        self.view = None
        self.lastPoint = None
        
    def tabletEvent(self, event, view):
        """
        Handle TabletEvent
        """
        if(event.pressure()*100 > 50):
            self.view = view
            point = self.mapToPage(event.pos())
            # check if we are in DocumentPage
            inPage = False
            items = view.scene().items(point)
            for i in items:
                if(i.zValue() == -42):
                    self.Page = i
                    inPage = True
                    break
            if not (inPage):
                self.deviceDown = False
                return
            # Begin line
            if(self.deviceDown == False):
                self.deviceDown = True
                self.Line = Item.Line(view, point)
                view.scene().addItem(self.Line)
                self.Line.setParentItem(self.Page)
                self.lastPoint = point
            # Continue Line
            else:
                if not(self.Line is None):
                    '''
                    instead of calculating the exact value with sqrt(x**2+y**2) estimate the 
                    distance with (abs(x) +abs(y))*0.8 for better performance. The estimation 
                    diverges from the exact value by an averageof 8.3%
                    '''
                    print abs(point.x() - self.lastPoint.x()) + abs(point.y() - self.lastPoint.y())*0.8
                    if(abs(point.x() - self.lastPoint.x()) + abs(point.y() - self.lastPoint.y())*0.8 > 3):
                        self.Line.addPoint(point)
                        self.lastPoint = point
        else: self.deviceDown = False


current_tool = Tool()
'''
Contains the current tool and its configuration and the class definitions for different tools.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

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
    Pen with some debug functionality. Not really usable as a free hand
    pen.
    """

    def __init__(self):
        Tool.__init__(self)
        self.deviceDown = False

    def tabletEvent(self, event, document):
        if event.pressure() > 0.5:
            if self.deviceDown:
                self.mouseMoveEvent(event, document)
            else:
                self.mousePressEvent(event, document)
        else:
            if self.deviceDown:
                self.mouseReleaseEvent(event, document)
            else:
                self.mouseMoveEvent(event, document)

    def mousePressEvent(self, event, document):
        self.devideDown = True
        point_coords = document.mapToScene(event.pos())
        page = document.page_at(point_coords)
        item = document.scene().addEllipse(point_coords.x() - 20, point_coords.y() - 20, 40, 40)
        item.setZValue(1)
        item.setParentItem(page)

    def mouseReleaseEvent(self, event, document):
        self.deviceDown = False

    def mouseMoveEvent(self, event, document):
        if not self.deviceDown:
            return

current_tool = Tool()
'''
Contains the current tool and its configuration and the class definitions for different tools.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

import pynal.view.Object as Object

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
        #cursorBmp = QtGui.QBitmap()
        #cursorBmp.fromImage("../cursor.bmp")
        #cursor = QtGui.QCursor(cursorBmp)
        self.cursor = QtCore.Qt.CrossCursor
        self.view = None
        
    def tabletEvent(self, event, view):
        """
        Handle TabletEvent
        """
        #TODO: Collision detection with Scene

        if(event.pressure()*100 > 50):
            inPage = False
            items = view.scene().items(QtCore.QPointF(view.mapToScene(event.pos())))
            print items
            for i in items:
                if(i.zValue() == -42):
                    inPage = True
            if not (inPage):
                self.deviceDown = False
                return
            if(self.deviceDown == False):
                self.deviceDown = True
                self.view = view
                   
                self.Line = Object.Line(view, QtCore.QPointF(view.mapToScene(event.pos())))
            else:
                if not(self.Line is None):
                    self.Line.addPoint(QtCore.QPointF(self.view.mapToScene(event.pos())))
        else: self.deviceDown = False


current_tool = Tool()
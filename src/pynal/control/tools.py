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
    Pen
    """

    def __init__(self):
        Tool.__init__(self)
        self.cursor = QtCore.Qt.CrossCursor
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(4)
        self.item = None
        self.deviceDown = False
        #
        
    def tabletEvent(self, event, view):
        if(event.pressure()*100 > 50):
            if(self.deviceDown == False):
                self.path = QtGui.QPainterPath(QtCore.QPointF(view.mapToScene(event.pos())))
                view.scene().addPath(self.path, self.pen)
                self.deviceDown = True
            else:
                self.path.lineTo(QtCore.QPointF(view.mapToScene(event.pos())))
                view.scene().removeItem(self.item)
                self.item = view.scene().addPath(self.path, self.pen)
                #scene.update()
        else: self.deviceDown = False
            
            

current_tool = Tool()
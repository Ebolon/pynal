from PyQt4 import QtCore
from PyQt4 import QtGui

class Object():
    '''
    Base class of all Drawing Objects.
    '''
    def __init__(self, view):
        '''
        Constructor
        '''
        self.view = view

class Line(Object):
    def __init__(self, view, point=None):
        """
        Create a new Line Object

        Parameters:
        view  -- the  document view.
        point -- a QPointF where the Line begin
        """
        Object.__init__(self, view)
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(4)
        self.item = None
        self.path = QtGui.QPainterPath(point) 
        self.item = view.scene().addPath(self.path, self.pen)
        self.item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        
        
    def addPoint(self, point):
        """
        Add a new Point to the Line

        Parameters:
        point -- a QPointF where the Line begin
        """
        #TODO: need improvement
        self.path.lineTo(QtCore.QPointF(point))
        self.view.scene().removeItem(self.item)
        self.item = self.view.scene().addPath(self.path, self.pen)
        self.item.update()
        self.item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
 
    def setWidth(self, width):
        """
        Set the width to the given value and resize the Pen.
        """
        self.pen.setWidth(width)
    
    def setColor(self, color):
        """
        Set the Pen Color to the given QColor.
        """
        self.pen.setColor(color)
    
    def setCapStyle(self, capstyle):
        """
        Set the Pen CapStyle to the given CapStyle.
        """        
        self.pen.setCapStyle(capstyle)
    
    def setJoinStyle(self, joinstyle):
        """
        Set the Pen JoinStyle to the given JoinStyle.
        """
        self.pen.setJoinStyle(joinstyle)

class Shape(Object):
    def __init__(self, view, point=None):
        """
        Create a new shape object

        Parameters:
        view  -- the  document view.
        point -- a QPointF where the shape begin
        """
        Object.__init__(self, view)

class Text(Object):
    def __init__(self, view, point=None):
        """
        Create a new text object

        Parameters:
        view  -- the  document view.
        point -- a QPointF where the text begin
        """
        Object.__init__(self, view)

class Picture(Object):
    def __init__(self, view, point=None):
        """
        Create a new picture object

        Parameters:
        view  -- the  document view.
        point -- a QPointF where the picture begin
        """
        Object.__init__(self, view)
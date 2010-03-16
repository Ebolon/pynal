from PyQt4 import QtCore
from PyQt4 import QtGui
from math import sqrt

class Item:
    '''
    Base class of all Drawing Objects.
    '''
    def __init__(self, view):
        """
        Constructor
        """
        self.view = view

class Line(Item, QtGui.QGraphicsPathItem):
    def __init__(self, view, point=None):
        """
        Create a new Line Object

        Parameters:
        view  -- the  document view.
        point -- a QPointF where the Line begin
        """
        Item.__init__(self, view)
        QtGui.QGraphicsPathItem.__init__(self)
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(4)
        self.path = QtGui.QPainterPath(point)
        self.setPath(self.path)
        self.setPen(self.pen)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.lastPoint = point
        
    def addPoint(self, point):
        """
        Add a new Point to the Line

        Parameters:
        point -- a QPointF where the Line begin
        """
        #TODO: need improvement
        if(3 < sqrt((point.x() - self.lastPoint.x()) ** 2 + (point.y() - self.lastPoint.y()) ** 2)):
            self.path.lineTo(QtCore.QPointF(point))
            self.setPath(self.path)
            self.update()
            self.lastPoint = point
 
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

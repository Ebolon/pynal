from PyQt4 import QtCore
from PyQt4 import QtGui

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
    def __init__(self, document, point=None):
        """
        Create a new Line Object

        Parameters:
        document  -- the  document view.
        point -- a QPointF where the Line begin
        """
        Item.__init__(self, document)
        QtGui.QGraphicsPathItem.__init__(self)
        self.document = document
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(4)
        self.path = QtGui.QPainterPath(point)
        self.setPen(self.pen)
        self.setPath(self.path)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

    def addPoint(self, point):
        """
        Add a new Point to the Line

        Parameters:
        point -- a QPointF where the Line begin
        """
        #print "h", point
        self.path.lineTo(QtCore.QPointF(point))
        self.setPath(self.path)
        self.update()
        self.lastPoint = point

    def finalize(self):
        pass
   
    def setWidth(self, width):
        """
        Set the width to the given value and resize the Pen.
        """
        self.pen.setWidth(width)
        self.setPen(self.pen)
        self.update()
    
    def setColor(self, color):
        """
        Set the Pen Color to the given QColor.
        """
        self.pen.setColor(color)
        self.setPen(self.pen)
        self.update()
  
    def setStyle(self, style):
        """
        Set the Pen Style to the given Style.
        """        
        self.pen.setStyle(style)
        self.setPen(self.pen)
        self.update()      
    
    def setCapStyle(self, capstyle):
        """
        Set the Pen CapStyle to the given CapStyle.
        """        
        self.pen.setCapStyle(capstyle)
        self.setPen(self.pen)
        self.update()
    
    def setJoinStyle(self, joinstyle):
        """
        Set the Pen JoinStyle to the given JoinStyle.
        """
        self.pen.setJoinStyle(joinstyle)
        self.setPen(self.pen)
        self.update()
    
    def getPoints(self):
        points = []
        for i in range(0, self.path.elementCount() -1):
            points.append(self.path.elementAt(i))
        return points

    def type(self):
        #TODO: standardize type codes
        return 65555
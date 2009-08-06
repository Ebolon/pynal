'''
Created on 27.05.2009

@author: dominik
'''
from PyQt4 import QtGui, QtCore

class PenTool():
    def __init__(self):
        self.path = None
        self.Gpath = None
        self.active = False
        self.event = 0
        self.lastPoint = None
        
        # atm the nicest settings for the pen.
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(2)
        
    def start(self, startpoint, scene):
        self.path = QtGui.QPainterPath(startpoint)
        self.Gpath = scene.addPath(self.path, self.pen)
        
        self.active = True
        self.lastPoint = None
        
    def isActive(self):
        return self.active
    
    def mouseMove(self, cursorPos):
        if self.lastPoint is not None:
            self.addPoint(cursorPos)
            self.lastPoint = None
        elif self.lastPoint != cursorPos:
            self.lastPoint = QtCore.QPointF(cursorPos)
    
    def end(self, endpos):
        self.path.lineTo(endpos) #quad
        self.Gpath.setPath(self.path)
        self.__init__()
    
    def addPoint(self, pos):
        startpoint = self.path.currentPosition()
        c21, c23 = self.cpoints(startpoint, self.lastPoint, pos)
        
        self.path.cubicTo(c21, c23, self.lastPoint)
        self.Gpath.setPath(self.path)
        
    def cpoints(self, p1, p2, p3):
        v = 1
        vektor = [p3.x() - p1.x(), p3.y() - p1.y()]
        lg = vektor[0] + vektor[1]
        
        evektor = [v*x/lg for x in vektor]
        c21 = QtCore.QPointF(p2.x() - evektor[0], p2.y() - evektor[1])
        c23 = QtCore.QPointF(p2.x() + evektor[0], p2.y() + evektor[1])
        return c21, c23
    
    # Stops the tool when the pen has left
    # the tablet and no endclick was send.
    # Will be moved to the Tool superclass.
    def pressure(self, pres):
        if self.isActive() and pres <= 0.1:
            self.__init__()
        
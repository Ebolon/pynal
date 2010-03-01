'''
Created on 24.02.2010

@author: simon
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

class Object():

    def __init__(self, view):
        self.view = view

class Line(Object):
    def __init__(self, view, point):
        Object.__init__(self, view)
        self.cursor = QtCore.Qt.CrossCursor
        self.pen = QtGui.QPen()
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.pen.setWidth(4)
        self.item = None
        self.path = QtGui.QPainterPath(QtCore.QPointF(point)) 
        self.item = view.scene().addPath(self.path, self.pen)
        
        
    def addPoint(self, point):
        self.path.lineTo(QtCore.QPointF(point))
        self.view.scene().removeItem(self.item)
        self.item = self.view.scene().addPath(self.path, self.pen)
 
        
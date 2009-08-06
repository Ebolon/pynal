'''
Created on 27.05.2009

@author: dominik
'''
import os

from PyQt4 import QtGui, QtCore

class PynalGView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        
        self.scene = QtGui.QGraphicsScene()
        greenpen = QtCore.Qt.green
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        
        self.addPages()
        
        self.setScene(self.scene)
        
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.curPage = None
        
        self.tool = None
        
        self.scaleValue = 1.0
        
    def setTool(self, tool):
        self.tool = tool
        
    def tabletEvent(self, event):
        self.tool.pressure(event.pressure())
        event.ignore()
        
    def addPages(self):
        self.pages = set()
        brush = QtGui.QBrush(QtGui.QPixmap(os.path.join("images", "boxes.png")))
        scene = self.scene.addRect(0, 0, 800, 1200, QtCore.Qt.black, brush)
        scene.setZValue(-1)
        self.pages.add(scene)
        scene = self.scene.addRect(0, 1250, 800, 1200)
        scene.setBrush(brush)
        scene.setZValue(-1)
        self.pages.add(scene)
        
    def getPage(self, pos):
        if len(self.items(pos)) == 0:
            return None
        else:
            return self.items(pos)[-1]
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.curPage = self.getPage(event.pos())
            if self.curPage is None:
                return
            self.tool.start(self.mapToScene(event.pos()), self.scene)
            
        elif event.button() == QtCore.Qt.MidButton:
            if int(event.modifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
                self.scaleValue = 1.0
                self.resetMatrix()
                self.scale(self.scaleValue, self.scaleValue)
                
    def changeScale(self, int):
        self.scaleValue = int / 100.0
        self.resetMatrix()
        self.scale(self.scaleValue, self.scaleValue)
        
    def mouseMoveEvent(self, event):
        bottom = self.getPage(event.pos())
        
        if self.tool.isActive():
            if bottom is not self.curPage:
                return
            self.tool.mouseMove(self.mapToScene(event.pos()))
            
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.tool.isActive():
                self.tool.end(self.mapToScene(event.pos()))
            
    def wheelEvent(self, event):
        if int(event.modifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
            if event.delta() < 0:
                if self.scaleValue <= 0.2:
                    add = 0
                else:
                    add = -0.1
            else:
                if self.scaleValue < 4:
                    add = 0.1
            
            self.scaleValue += add
            self.resetMatrix()
            self.scale(self.scaleValue, self.scaleValue)
        else:
            QtGui.QGraphicsView.wheelEvent(self, event)
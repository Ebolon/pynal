'''
Created on 24.05.2009

#1
Can now zoom and reset that zoom. Also a test on needed effort to use multi button
behaviour. With proper and simple class design this should be very easy.

#2
in progress

@author: dominik
'''
import sys, os

from PyQt4 import QtCore, QtGui
from math import sqrt

class PenTool():
    def __init__(self):
        self.path = None
        self.Gpath = None
        self.active = False
        self.event = 0
        self.lastPoint = None
        self.secndLastPoint = None
        
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
        self.secndLastPoint = None
        self.lastCPoint = None
        
    def isActive(self):
        return self.active
    
    def mouseMove(self, cursorPos):
        if (self.lastPoint != cursorPos and self.secndLastPoint != cursorPos):
            if self.secndLastPoint is not None:
                self.smoothPoint(cursorPos)
                self.addPoint(cursorPos)
            self.secndLastPoint = self.lastPoint
            self.lastPoint = cursorPos
    
    def end(self, endpos):
#        if self.lastPoint is not None:
#            self.path.lineTo(self.lastPoint)
#        self.path.lineTo(endpos) #Deactivated to remove stylus hook
#        self.Gpath.setPath(self.path)
        print self.path.elementCount()
        self.__init__()
    
    def addPoint(self, pos):
        c21, c23 = self.cpoints(self.secndLastPoint, self.lastPoint, pos)
        
        if self.lastCPoint is None:
            self.path.quadTo(c21, self.lastPoint)
        else:
            self.path.cubicTo(self.lastCPoint, c21, self.lastPoint)
        self.Gpath.setPath(self.path)
        self.lastCPoint = c23
        
    def cpoints(self, p1, p2, p3):
        v = 5
        vektor = [p3.x() - p1.x(), p3.y() - p1.y()]
        lg = self.vectorLength(vektor)
        p12 = [p1.x() - p2.x(), p1.y() - p2.y()]
        p32 = [p3.x() - p2.x(), p3.y() - p2.y()]
        if p12 < p32:
            l = self.vectorLength(p12)/v
        else:
            l = self.vectorLength(p32)/v
        
        evektor = [l*x/lg for x in vektor]
        c21 = QtCore.QPointF(p2.x() - evektor[0], p2.y() - evektor[1])
        c23 = QtCore.QPointF(p2.x() + evektor[0], p2.y() + evektor[1])
        return c21, c23
    
    def vectorLength(self, v):
        return 0.8*(abs(v[0]) + abs(v[1]))
        #return sqrt(v[0]*v[0] + v[1]*v[1])
    
    def smoothPoint(self, cursorPos, scale):
        a = 0.5
        lfpx, lfpy = self.lotFussPoint(self.lastPoint, self.secndLastPoint, cursorPos)
        self.lastPoint.setX(lfpx*a + self.lastPoint.x()*(1-a))
        self.lastPoint.setY(lfpy*a + self.lastPoint.y()*(1-a))
    
    def lotFussPoint(self, p, s ,e):
        b = [s.x(), s.y()]
        a = [e.x() - s.x(), e.y() - s.y()]
        x = (a[0]*(p.x() - b[0]) + a[1]*(p.y() - b[1])) / (a[0]*a[0] + a[1]*a[1])
        return b[0] + a[0]*x, b[1] + a[1]*x
    
    # Stops the tool when the pen has left
    # the tablet and no endclick was send.
    # Will be moved to the Tool superclass.
    def pressure(self, pressure, pos):
        if self.isActive() and pressure <= 0.1:
            self.end(pos)
        
class LineTool():
    def __init__(self):
        self.line = None
        self.Gline = None
        self.active = False
        
    def start(self, startpoint, scene):
        self.line = QtCore.QLineF(startpoint, startpoint)
        self.Gline = scene.addLine(self.line)
        
        self.active = True
        
    def isActive(self):
        return self.active
    
    def mouseMove(self, cursorPos, scale):
        self.endPoint(cursorPos)
    
    def end(self, endpos):
        self.endPoint(endpos)
        self.__init__()
    
    def endPoint(self, pos):
        self.line.setP2(pos)
        self.Gline.setLine(self.line)
        
    def pressure(self, pressure, pos):
        pass

#===============================================================================
# GraphicsScene
#  The GraphicsScene used in the MainWindow.
#===============================================================================
class PaintTest(QtGui.QGraphicsView):
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
        
        self.tool = PenTool()
        
        self.scaleValue = 1.0
        
    def tabletEvent(self, event):
        if self.tool.isActive():
            self.tool.pressure(event.pressure(), self.mapToScene(event.pos()))
        QtGui.QGraphicsView.tabletEvent(self, event)
        
    def addPages(self):
        self.scenes = set()
        brush = QtGui.QBrush(QtGui.QPixmap(os.path.join("images", "boxes.png")))
        scene = self.scene.addRect(0, 0, 800, 1200, QtCore.Qt.black, brush)
        scene.setZValue(-1)
        self.scenes.add(scene)
        scene = self.scene.addRect(0, 1250, 800, 1200)
        scene.setBrush(brush)
        scene.setZValue(-1)
        self.scenes.add(scene)
        
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
            self.tool.mouseMove(self.mapToScene(event.pos()), self.scaleValue)
            
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
            
#===============================================================================
# MainWindow Class.
#===============================================================================
class TestWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk IV")
        
        self.view = PaintTest()
        self.setCentralWidget(self.view)
        
        bar = self.addToolBar("Tools")
        action = bar.addAction("Line")
        self.connect(action, QtCore.SIGNAL("triggered()"), self.setLineTool)
        action = bar.addAction("Pen")
        self.connect(action, QtCore.SIGNAL("triggered()"), self.setPenTool)
        
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setMaximum(200)
        slider.setMinimum(10)
        slider.setValue(100)
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"), self.view.changeScale)
        bar.addWidget(slider)
        
    def setLineTool(self):
        self.view.tool = LineTool()
        
    def setPenTool(self):
        self.view.tool = PenTool()
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
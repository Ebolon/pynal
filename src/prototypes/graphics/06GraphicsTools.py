'''
Created on 24.05.2009

#1
Can now zoom and reset that zoom. Also a test on needed effort to use multi button
behaviour. With proper and simple class design this should be very easy.

@author: dominik
'''
import sys, os

from PyQt4 import QtCore, QtGui

class PenTool():
    def __init__(self):
        self.path = None
        self.Gpath = None
        self.active = False
        self.event = 0
        
    def start(self, startpoint, scene):
        self.path = QtGui.QPainterPath(startpoint)
        
        # atm the nicest settings for the pen.
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        pen.setWidth(2)
        self.Gpath = scene.addPath(self.path, pen)
        
        self.active = True
        
    def isActive(self):
        return self.active
    
    def mouseMove(self, cursorPos):
        self.event += 1
        if self.event >= 2: #2 seems best atm
            self.addPoint(cursorPos)
            self.event = 0
            
    
    def end(self, endpos):
        self.addPoint(endpos)
        self.__init__()
    
    def addPoint(self, pos):
        self.path.lineTo(pos)
        self.Gpath.setPath(self.path)
    
    # Stops the tool when the pen has left
    # the tablet and no endclick was send.
    # Will be moved to the Tool superclass.
    def pressure(self, pres):
        if self.isActive() and pres <= 0.1:
            self.__init__()
        
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
    
    def mouseMove(self, cursorPos):
        self.endPoint(cursorPos)
    
    def end(self, endpos):
        self.endPoint(endpos)
        self.__init__()
    
    def endPoint(self, pos):
        self.line.setP2(pos)
        self.Gline.setLine(self.line)
        
    def pressure(self, pres):
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
        
        self.start = None
        self.end   = None
        
        self.previewObject = None
        
        self.curPage = None
        
        self.tool = LineTool()
        
        self.scaleValue = 1.0
        
    def tabletEvent(self, event):
        self.tool.pressure(event.pressure())
        event.ignore()
        
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
            
#===============================================================================
# MainWindow Class.
#===============================================================================
class TestWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk IV")
        
        self.view = PaintTest()
        self.setCentralWidget(self.view)
        
        style = self.style()
        
        bar = self.addToolBar("Tools")
        action = bar.addAction("Line")
        action.setIcon(QtGui.QIcon(style.standardPixmap(QtGui.QStyle.SP_BrowserReload)))
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
        print "ar"
        self.view.tool = PenTool()
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
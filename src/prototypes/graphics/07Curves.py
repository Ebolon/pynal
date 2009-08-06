'''
Created on 24.05.2009

#1
Can now zoom and reset that zoom. Also a test on needed effort to use multi button
behaviour. With proper and simple class design this should be very easy.

@author: dominik
'''
import sys, os

from PyQt4 import QtCore, QtGui

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
        
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        pen.setWidth(2)
        
        point1 = QtCore.QPointF(10, 10)
        point2 = QtCore.QPointF(13, 13)
        point3 = QtCore.QPointF(15, 11)
        point4 = QtCore.QPointF(18, 15)
        path = QtGui.QPainterPath(point1)
        path.lineTo(point2)
        path.lineTo(point3)
        path.lineTo(point4)
        self.scene.addPath(path, pen)
        
        p1 = QtCore.QPointF(10, 30)
        p2 = QtCore.QPointF(13, 33)
        p3 = QtCore.QPointF(15, 31)
        p4 = QtCore.QPointF(18, 35)
        
        c21, c23 = self.cpoints(p1, p2, p3)
        c32, c34 = self.cpoints(p2, p3, p4)
        
        path = QtGui.QPainterPath(p1)
        path.quadTo(c21, p2)
        path.cubicTo(c23, c32, p3)
        path.quadTo(c34, p4)
        self.scene.addPath(path, pen)
        
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.scaleValue = 1.0
        
    def cpoints(self, p1, p2, p3):
        v = 1
        vektor = [p3.x() - p1.x(), p3.y() - p1.y()]
        lg = 0.8 * vektor[0] + vektor[1]
        evektor = [v*x/lg for x in vektor]
        c21 = QtCore.QPointF(p2.x() - evektor[0], p2.y() - evektor[1])
        c23 = QtCore.QPointF(p2.x() + evektor[0], p2.y() + evektor[1])
        return c21, c23
        
    def addPages(self):
        self.scenes = set()
        brush = QtGui.QBrush(QtGui.QPixmap(os.path.join("images", "boxes.png")))
        scene = self.scene.addRect(0, 0, 800, 800, QtCore.Qt.black, brush)
        scene.setZValue(-1)
        self.scenes.add(scene)
        
    def getPage(self, pos):
        if len(self.items(pos)) == 0:
            return None
        else:
            return self.items(pos)[-1]
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            if int(event.modifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
                self.scaleValue = 1.0
                self.resetMatrix()
                self.scale(self.scaleValue, self.scaleValue)
                
    def changeScale(self, int):
        self.scaleValue = int / 100.0
        self.resetMatrix()
        self.scale(self.scaleValue, self.scaleValue)
        
    def wheelEvent(self, event):
        if int(event.modifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
            add = 0
            if event.delta() < 0:
                if self.scaleValue > 0.2:
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
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk V")
        
        self.view = PaintTest()
        self.setCentralWidget(self.view)
        
        bar = self.addToolBar("moep")
        slider = QtGui.QSlider()
        bar.addWidget(slider)
        
        slider.setMaximum(200)
        slider.setMinimum(1)
        slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"), self.curve)
        
    def curve(self, int):
        self.view.curve(int)
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
#===============================================================================
# Created on 24.05.2009
#
# Created from 02 experiences.
#
# Aims of this prototype:
#  * Extending 02 to provide a live preview of the line the user is drawing
#    by using a timer based approach.
#
# Conclusion:
#  It works. Might need some cleanup and code can probably be simplified and
#  fine tuned. Will work if other methods fail, but there are still other
#  possibilities.
#
#  Depending on the timer resolution the drawing lags but I could not observe
#  spikes in system load when decreasing the time between redraws.
#  This might change when there are many other objects to draw, though.
#
# @author: dominik
#===============================================================================
import sys

from PyQt4 import QtCore, QtGui

class PaintTest(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        
        self.scene = QtGui.QGraphicsScene()
        greenpen = QtCore.Qt.green
        self.scene.addLine(0, -500, 0, 500, greenpen)
        self.scene.addLine(-500, 0, 500, 0, greenpen)
        self.scene.addEllipse(-10, -10, 20, 20, greenpen)
        self.scene.addText("(0,0)")
        self.scene.setSceneRect(100, 100, 100, 100)
        self.setScene(self.scene)
        
        self.setSceneRect(0, 0, 200, 200)
        
        #I just love that blurry look of the lines with AA...
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.start = None
        self.end   = None
        
        self.timer = QtCore.QBasicTimer()
        self.previewObject = None
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start = QtGui.QMouseEvent(event)
            self.end = self.start
            self.timer.start(10, self)
            
    def mouseMoveEvent(self, event):
        if self.start is not None:
            self.end = QtGui.QMouseEvent(event)
            
    def timerEvent(self, event):
        p1 = self.mapToScene(self.start.x(), self.start.y())
        p2 = self.mapToScene(self.end.x(), self.end.y())
        if self.previewObject is None:
            self.previewObject = self.scene.addLine(
                                    QtCore.QLineF(p1.x(), p1.y(),
                                                  p2.x(), p2.y()))
        else:
            self.previewObject.setLine(
                                   QtCore.QLineF(p1.x(), p1.y(),
                                                 p2.x(), p2.y()))

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.timer.stop()
            self.scene.removeItem(self.previewObject)
            self.previewObject = None
            self.end = QtGui.QMouseEvent(event)
            if self.start is None or self.end is None:
                print event
                return
            
            p1 = self.mapToScene(self.start.x(), self.start.y())
            p2 = self.mapToScene(self.end.x(), self.end.y())
            self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())

class TestWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(700, 800)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk II")
        self.view = PaintTest(self)
        self.setCentralWidget(self.view)
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()

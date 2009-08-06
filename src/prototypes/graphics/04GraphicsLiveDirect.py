'''
Created on 24.05.2009

Based on experiences and the base model of 03.

Aims of this prototype:
 Develop a method to display a live line by using only as many lines as
 needed. This direct approach should be more efficient than the timer based variant.
 
 In a good world it will also be clean.
 
 This might actually be achievable by using SIGNALS and SLOTS but at the moment
 I have no idea how to limit this to a left click action except for always checking
 in a dedicated method which would actually kill the reason for the slots
 mechanism.
 
 ==========================================================================
 To date this is the preferrable method of drawing a live line when working
 with the graphics scene and view.
 =========================================================================

@author: dominik
'''
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
        
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.start = None
        self.end   = None
        
        self.previewObject = None
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start = self.end = QtGui.QMouseEvent(event)
            self.end = self.start
            
            self.start = self.mapToScene(self.start.pos())
            self.previewObject = self.scene.addLine(QtCore.QLineF(self.start, self.start))
        
        else:
            print self.scene.get
                        
    def mouseMoveEvent(self, event):
        if self.previewObject is not None:
            end = QtGui.QMouseEvent(event)
            end = self.mapToScene(event.pos())
            self.previewObject.setLine(QtCore.QLineF(self.start, end))
            
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.previewObject = None
            
class TestWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(700, 800)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk III")
        self.view = PaintTest(self)
        self.setCentralWidget(self.view)
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
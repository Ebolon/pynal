#===============================================================================
# Created on 23.05.2009
#
# Created from 01paintpath.py experiences.
#
# Lines are rendered into a GraphicsScene and displayed through a GraphicsView for
# better performance.
#
# Aims of this prototype are:
#  * Combine a QGraphicsScene and -View to display QGraphicsItems form external
#    sources.
#  * Developing a custom widget that inherits QGraphicsView or -Scene to achieve
#    said results.
#  * Displaying the live preview of a line as in 01.paintpath.py by using a layer
#    on top the custom widget. (This has been moved to 03!
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
        moep = self.scene.addText("(0,0)")
        self.scene.setSceneRect(100, 100, 100, 100)
        self.setScene(self.scene)
        
        self.setSceneRect(0, 0, 200, 200)
        
        #I just love that blurry look of the lines with AA...
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.start = None
        self.end   = None
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start = QtGui.QMouseEvent(event)

# Deactivated and moved to prototype 03!
#    def mousMoveEvent(self, event):
#        if self.start is not None:
#            self.end = QtGui.QMouseEvent(event)
#            self.update()
                
# Deactivated and moved to prototype 03!
#    def paintEvent(self, event):
#        QtGui.QGraphicsView.paintEvent(self, event)
#        painter = QtGui.QPainter()
#        painter.begin(self)
#        painter.setPen(QtCore.Qt.red)
#        
#        painter.drawLine(self.start.x(), self.start.y(),
#                         self.end.x(), self.end.y())
#        
#        painter.end()
        
    def mouseReleaseEvent(self, event):
        #Still working on that shit.
        if event.button() == QtCore.Qt.LeftButton:
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
        self.setWindowTitle("I suck so hard, it's not even funny anymore.")
        self.view = PaintTest(self)
        self.setCentralWidget(self.view)
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()

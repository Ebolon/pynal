'''
Created on 24.05.2009

This prototype aims to create a properly configured graphics scene and view that
can display and manage different pages.

#1
I don't think that there is a bultin possibility to divide the scene into pages,
they have to be added as normal items. This might add some confusion when editing
items (don't erase the page when removing items, don't select etc) but opens many
opportunities for neat functions using pages. (drag&drop moving of pages, resizing
and stretching etc).

I still need to find a way to restrict the scene in its size.

#2
Pages get a more or less small ZValue. -1 Should suffice for now as the value
normally starts at 0 and the only change that might happen automatically is
that it grows.

#3
A general method for displaying pages stands, the painting area is not restricted,
though.

#4
A crude way of restricting operations on the current page has been achieved. Would
be nicer if one could actually draw from one Page on another while drawing in the
void between them are not shown. This is not really necessary but might be expected
behaviour.

When it comes to moving items from one page to another this method stands in the
way but for the moment it is sufficient.

#5
Development will continue in 06 as this single file has produced enough single
achievements.

@author: dominik
'''
import sys

from PyQt4 import QtCore, QtGui

class PaintTest(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        
        self.scene = QtGui.QGraphicsScene()
        greenpen = QtCore.Qt.green
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        
        self.addPage()
        
        self.scene.addLine(0, -500, 0, 500, greenpen)
        self.scene.addLine(-500, 0, 500, 0, greenpen)
        self.scene.addEllipse(-10, -10, 20, 20, greenpen)
        self.scene.addText("(0,0)")
        
        self.setScene(self.scene)
        
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.start = None
        self.end   = None
        
        self.previewObject = None
        
        self.curPage = None
        
    def addPage(self):
        self.scenes = set()
        scene = self.scene.addRect(0, 0, 800, 1200, QtCore.Qt.black, QtCore.Qt.white)
        scene.setZValue(-1)
        self.scenes.add(scene)
        scene = self.scene.addRect(0, 1250, 800, 1200, QtCore.Qt.black, QtCore.Qt.white)
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
                        
            self.start = self.end = QtGui.QMouseEvent(event)
            self.end = self.start
            
            self.start = self.mapToScene(self.start.pos())
            self.previewObject = self.scene.addLine(QtCore.QLineF(self.start, self.start))
                        
    def mouseMoveEvent(self, event):
        bottom = self.getPage(event.pos())
        
        if self.previewObject is not None:
            
            if bottom is not self.curPage:
                return
            
            end = QtGui.QMouseEvent(event)
            end = self.mapToScene(event.pos())
            self.previewObject.setLine(QtCore.QLineF(self.start, end))
            
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.previewObject = None
            
class TestWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("I suck so hard, it's not even funny anymore. Mk III")
        
        self.view = PaintTest()
        self.setCentralWidget(self.view)
        
        
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
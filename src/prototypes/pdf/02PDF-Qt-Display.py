#!/usr/bin/env python
#===============================================================================
# Loads and displays a PDF file in a QGraphicsScene to be able to draw on it.
#
# TODO:
#    + Load pdf in background
#    + quality/performance tests with dpi+scaling
#    + Load pages only when needed (isn't this done by the graphicsscene?)
# TODOs moved to 03.
#===============================================================================
import sys

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import QtPoppler

#dpi resolution used to render the pdf into a QImage.
dpi = 150

if len(sys.argv) < 2:
    print "Usage:\n\tpython 02PDF-Qt-Display.py <filename>"
    sys.exit(1)


class PdfScene(QtGui.QGraphicsView):
    def __init__(self, document, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        
        self.document = document
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        
        self.addPages()
        
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
                
    def addPages(self):
        print "Adding pages..."
        self.pages = set()
        for i in range(0, self.document.numPages()):
            image = self.document.page(i).renderToImage(dpi, dpi)
            print "Size of image: " + str(image.width()) + "x"+ str(image.height())
            
            pixmap = QtGui.QPixmap.fromImage(image)
            item = self.scene.addPixmap(pixmap)
            item.setOffset(0, i*1800)
            item.setVisible(True)
            print "Added page to scene."
            
class TestWindow(QtGui.QMainWindow):

    def __init__(self, document):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Displaying PDF in GraphicsScene")
        
        self.view = PdfScene(document)
        self.setCentralWidget(self.view)
        
app = QtGui.QApplication(sys.argv)

doc = QtPoppler.Poppler.Document.load(sys.argv[1])
doc.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and QtPoppler.Poppler.Document.TextAntialiasing)
window = TestWindow(doc)
window.show()
app.exec_()
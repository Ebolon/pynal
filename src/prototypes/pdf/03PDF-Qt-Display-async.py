#!/usr/bin/env python
#===============================================================================
# Loads and displays a PDF file in a QGraphicsScene to be able to draw on it.
#
# Adding images to the QGraphicsScene from the worker thread results in a warning:
# QPixmap: It is not safe to use pixmaps outside the GUI thread
#
# Adding the images from within the gui thread after they have been created by
# the worker thread(pool) should be possible by emitting a signal whenever
# an image has been created.
#
# A suitable mechanism to keep the correct order of images when displaying them
# is needed then.
#===============================================================================
import sys

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import QtPoppler

#dpi resolution used to render the pdf into a QImage.
dpi = 150

if len(sys.argv) < 2:
    print "Usage:\n\tpython 03PDF-Qt-Display-async.py <filename>"
    sys.exit(1)


class PdfScene(QtGui.QGraphicsView):
    """ A QGraphicsScene used to display the pdf pages. """

    def __init__(self, document, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)

        self.document = document
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))

        self.addPages()

        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

    def addPages(self):
        """
        Keeping a reference to the thread is necessary to prevent
        the thread object from getting destroyed while it still runs,
        resulting in
        "It is not safe to use pixmaps outside the GUI thread"

        The object should be removed using the signal QThread.finished()
        or QThread.terminated().
        """
        self.thread = PdfLoaderThread(self.document, self.scene)
        self.thread.start()
        print "Adding pages..."

class TestWindow(QtGui.QMainWindow):
    """ Creates and Displays a QGraphicsScene """
    def __init__(self, document):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Displaying PDF in GraphicsScene")

        self.view = PdfScene(document)
        self.setCentralWidget(self.view)

class PdfLoaderThread(QtCore.QThread):
    """
    Creates QImages (or QPixmaps) from all pages in a given Poppler document.
    """
    def __init__(self, doc, scene):
        """
        Creates a new PdfLoaderThread.

        Params:
            doc - the QtPoppler.Poppler.Document that is to be loaded
            scene - the QGraphicsScene that will receive the pixmaps.
        """
        QtCore.QThread.__init__(self)

        self.doc = doc
        self.scene = scene

    def run(self):
        """ Creates and adds the pixmaps to the QGraphicsScene. """
        for i in range(0, self.doc.numPages()):
            image = self.doc.page(i).renderToImage(dpi, dpi)
            print "Size of image: " + str(image.width()) + "x"+ str(image.height())

            """ Move this into a signal/slot.
            pixmap = QtGui.QPixmap.fromImage(image)
            item = self.scene.addPixmap(pixmap)
            item.setOffset(0, i*1800)
            item.setVisible(True)
            """
            print "Added page to scene."

app = QtGui.QApplication(sys.argv)

doc = QtPoppler.Poppler.Document.load(sys.argv[1])
doc.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and QtPoppler.Poppler.Document.TextAntialiasing)
window = TestWindow(doc)
window.show()
app.exec_()

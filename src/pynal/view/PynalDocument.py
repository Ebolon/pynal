from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

import QtPoppler

import models.Config as Config

class PynalDocument(QtGui.QGraphicsView):
    """ Document widget displayed in the QTabWidget. """

    def __init__(self, source_file, parent=None):
        """
        Create a new PynalDocument for the given file.

        parameters:
        source_file -- String path to the pdf that is to be displayed.
        parent -- the parent widget of this widget.
        """
        QtGui.QGraphicsView.__init__(self, parent)
        self.source = source_file
        self.document = QtPoppler.Poppler.Document.load(self.source)
        self.document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and
                                    QtPoppler.Poppler.Document.TextAntialiasing)

        self.scene = QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.gray))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(self.ScrollHandDrag)

        self.thread = PdfLoaderThread(self.document, self.scene)
        self.connect(self.thread, SIGNAL("output(QImage, int)"), self.addPage)

        self.thread.start()

    def addPage(self, image, i):
        """
        Callback method for the worker thread.

        Adds the created image as a pixmap to the scene.
        """
        pixmap = QtGui.QPixmap.fromImage(image)
        item = self.scene.addPixmap(pixmap)
        item.setOffset(0, i*1500)

class PdfLoaderThread(QtCore.QThread):
    """
    Creates QImages from all pages in a given Poppler document.
    """
    def __init__(self, doc, scene):
        """
        Creates a new PdfLoaderThread.

        parameters:
            doc - the QtPoppler.Poppler.Document that is to be loaded.
            scene - the QGraphicsScene that will receive the QImages.
        """
        QtCore.QThread.__init__(self)

        self.doc = doc
        self.scene = scene

    def run(self):
        """ Creates the images and notifies the QGraphicsScene. """
        for i in range(0, self.doc.numPages()):
            image = self.doc.page(i).renderToImage(Config.pdf_render_dpi,
                                                   Config.pdf_render_dpi)
            self.emit(SIGNAL("output(QImage, int)"), image, i)
            if i > 10:
                break

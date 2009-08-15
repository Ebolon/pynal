#!/usr/bin/env python
#===============================================================================
# Loads a PDF file with PyPoppler-Qt4 and creates a new PDF with a QPrinter.
# Args:
#    1. <filename> - The pdf to load.
#
# Quality is shit but might improve when playing with parameters for
# renderToImage(dpi, dpi), RenderHints, PrinterResoultion etc.
#===============================================================================
import sys

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import QtPoppler

if len(sys.argv) < 2:
    print "Usage:\n\tpython 01PDF-Qt-copier.py <filename>"
    sys.exit(1)

app = QtGui.QApplication(sys.argv)

document = QtPoppler.Poppler.Document.load(sys.argv[1])
document.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and QtPoppler.Poppler.Document.TextAntialiasing)
print document.numPages(), "Pages found."

printer = QtGui.QPrinter(QtGui.QPrinter.PrinterResolution)
printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
printer.setOutputFileName("/tmp/output.pdf")
print "Initialized printer. Output to: /tmp/output.pdf"

painter = QtGui.QPainter(printer)
print "Starting to print..."
for i in range(0, document.numPages()):
    image = document.page(i).renderToImage()
    print "Size of page: " + str(image.width()) + "x"+ str(image.height())
    
    painter.drawImage(0, 0, image)
    printer.newPage()
    print "Printed page #" + str(i)
    
painter.end()
print "Finished."
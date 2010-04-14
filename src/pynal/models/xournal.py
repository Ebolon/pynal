'''
Created on 01.03.2010

@author: simon
'''
import gzip
import xml.sax
import pprint

from PyQt4 import QtCore
from PyQt4 import QtGui
from pynal.view import Item

import pynal.view.Item as Item

class Xournal():
    
    def load(self, filename, document):
        f = gzip.open(filename, 'rb')
        file_content = f.read()
        f.close()

        handler = XornalHandler(document)
        xml.sax.parseString(file_content, handler)

    def save(self, filename, document):
        # TODO: clean up move logic in class?
        file_content = "<?xml version=\"1.0\" standalone=\"no\"?>\n"
        file_content += "<xournal version=\"0.4.5\">\n"
        file_content += "<title>Xournal document - see http://math.mit.edu/~auroux/software/xournal/</title>\n"
        for page in document.get_pages():
            file_content += "<page width=\"612.00\" height=\"792.00\">\n"
            file_content += "<background type=\"solid\" color=\"white\" style=\"graph\" />\n"
            file_content += "<layer>\n"
            offset = page.boundingRect().topLeft()
            scale_x = float(page.boundingRect().width()) / 612
            scale_y = float(page.boundingRect().height()) / 792
            for c in page.childItems():
                if c.type() == 2:
                    path = c.path
                    file_content += "<stroke tool=\"pen\" color=\"black\" width=\"1.41\">\n"
                    for i in range(0, path.elementCount() -1):
                        x = abs(float(path.elementAt(i).x) / scale_x - offset.x())
                        y = abs(float(path.elementAt(i).y) / scale_y - offset.y())
                        file_content += str(round(x,2)) + " " + str(round(y,2)) + " "
                    if not path.elementCount() % 2:
                        file_content += str(round(x,2)) + " " + str(round(y,2)) + " "
                    file_content += "\n</stroke>\n"
            file_content += "</layer>\n"
            file_content += "</page>\n"
        file_content += "</xournal>\n"
        f = gzip.open(str(filename), 'wb')
        f.write(file_content)
        f.close()
        
class XornalHandler(xml.sax.handler.ContentHandler):
    def __init__(self, view):
        self.inStroke = False
        self.view = view
        self.page = {}
        self.strokeAtt = {}
        self.stroke = ""
        self.pages = []
        self.Line = None
        self.pageNumb = 0
        self.pageWidth = 0
        self.pageHeight = 0
        self.colors = {"red": QtGui.QColor(255, 0, 0), "blue":QtGui.QColor(51, 51, 204), "green":QtGui.QColor(0, 128, 0),
                       "gray":QtGui.QColor(128, 128, 128), "lightblue": QtGui.QColor(0, 196, 255),
                       "lightgreen":QtGui.QColor(0, 255, 0), "magenta": QtGui.QColor(255, 0, 255),
                       "orange":QtGui.QColor(255, 128, 0) , "yellow":QtGui.QColor(255, 255, 0), 
                       "white":QtGui.QColor(255, 255, 255), "black":QtGui.QColor(0, 0, 0)
                       }

    def startElement(self, name, attributes):
        if name == "page":
            self.pageWidth = attributes["width"]
            self.pageHeight = attributes["height"]
            if(self.pageNumb > 0):
                self.view.insert_new_page_at(self.pageNumb)
            self.pageNumb += 1
            
        elif name == "stroke":
            self.buffer = ""
            self.strokeAtt["tool"] = attributes["tool"]
            self.strokeAtt["color"] = attributes["color"]
            self.strokeAtt["width"] = float(attributes["width"])
            self.Line = None
            self.inStroke = True
 
    def characters(self, data):
        if self.inStroke:
            self.stroke += data
 
    def endElement(self, name):
        if name == "page":
            self.pages.append(self.page)
            self.page = {}
            self.strokes = []
        if name == "stroke":
            self.inStroke = False
            self.stroke.strip()
            
            strokeArr = self.stroke.split(" ")
            self.stroke = ""
            page= self.view.get_page(self.pageNumb - 1)
            # offset where page begin (0,0)
            offset = page.boundingRect().topLeft()
            scale_x = float(page.boundingRect().width())/float(self.pageWidth)
            scale_y = float(page.boundingRect().height())/float(self.pageHeight)
            x = offset.x() + float(strokeArr[0]) * scale_x
            y = offset.y() + float(strokeArr[1]) * scale_y
            self.Line = Item.Line(self.view, QtCore.QPointF(x,y)) # err?
            # TODO: Pynal standard pen size?
            self.Line.setWidth(int(self.strokeAtt["width"]))
            strokeColor = self.colors[self.strokeAtt["color"]]
            strokeColor.setAlpha(255)
            if self.strokeAtt["tool"] == "highlighter":
                self.Line.setZValue(6)
                strokeColor.setAlpha(100)
            self.Line.setColor(strokeColor)
            self.Line.setZValue(1)
            
            self.view.scene().addItem(self.Line)
            self.Line.setParentItem(page)
            for i in range(0, len(strokeArr)-1, 2):
                if(strokeArr[i] != "" and strokeArr[i+1] != ""):
                    x = offset.x() + float(strokeArr[i]) * scale_x
                    y = offset.y() + float(strokeArr[i+1]) * scale_y
                    self.Line.addPoint(QtCore.QPoint(x,y))

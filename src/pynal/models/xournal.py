'''
Created on 01.03.2010

@author: simon
'''
import gzip
import xml.sax
import pprint

from PyQt4 import QtCore
from PyQt4 import QtGui

import pynal.view.Item as Item

class Xournal():
    def __init__(self, filename, document):
        self.filename = filename
        self.view = document
        self.Line = None
        
    def load(self):
        f = gzip.open(self.filename, 'rb')
        file_content = f.read()
        f.close()

        handler = XornalHandler(self.view)
        xml.sax.parseString(file_content, handler)
                
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
            offset_x = float(page.scenePos().x() - page.boundingRect().width() / 2)
            offset_y = page.boundingRect().y()
            scale_x = float(page.boundingRect().width())/float(self.pageWidth)
            scale_y = float(page.boundingRect().height())/float(self.pageHeight)
            x = offset_x + float(strokeArr[0]) * scale_x
            y = offset_y + float(strokeArr[1]) * scale_y
            self.Line = Item.Line(self.view, QtCore.QPointF(x,y))
            # TODO: Pynal standard pen size?
            self.Line.setWidth(int(self.strokeAtt["width"]))
            self.Line.setParentItem(page)
            self.view.scene().addItem(self.Line)
            for i in range(0, len(strokeArr)-1, 2):
                if(strokeArr[i] != "" and strokeArr[i+1] != ""):
                    x = offset_x + float(strokeArr[i]) * scale_x
                    y = offset_y + float(strokeArr[i+1]) * scale_y
                    self.Line.addPoint(QtCore.QPoint(x,y))

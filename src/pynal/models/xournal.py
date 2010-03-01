'''
Created on 01.03.2010

@author: simon
'''
import gzip
import xml.sax.handler
import xml.sax
import pprint

from PyQt4 import QtCore
from PyQt4 import QtGui

import pynal.view.Object as Object

class Xournal():
    def __init__(self, filename, view):
        self.filename = filename
        self.view = view
        self.Line = None
        
    def load(self):
        f = gzip.open(self.filename, 'rb')
        file_content = f.read()
        f.close()

        handler = XornalHandler()
        xml.sax.parseString(file_content, handler)
        pprint.pprint(handler.strokes[0]["stroke"])
        for strokeDict in handler.strokes:
            strokeArr = strokeDict["stroke"].split(" ")
            self.Line = Object.Line(self.view, QtCore.QPointF(float(strokeArr[0]), float(strokeArr[1])))
            
            for i in range(0, len(strokeArr)-1, 2):
                print i, "p:", strokeArr[i], strokeArr[i+1]

                self.Line.addPoint(QtCore.QPointF(float(strokeArr[i]), float(strokeArr[i+1])))
                
class XornalHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inStroke = 0
        self.mapping = {}
        self.strokes = []
 
    def startElement(self, name, attributes):
        if name == "stroke":
            self.buffer = ""
            self.mapping["stroke"] = ""
            self.mapping["tool"] = attributes["tool"]
            self.mapping["color"] = attributes["color"]
            self.mapping["width"] = attributes["width"]
            self.inStroke = 1
 
    def characters(self, data):
        if self.inStroke:
            self.mapping["stroke"] += data
 
    def endElement(self, name):
        if name == "stroke":
            self.inStroke = 0
            self.mapping["stroke"].strip()
            self.strokes.append(self.mapping)

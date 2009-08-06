'''
Created on 27.05.2009

@author: dominik
'''
from PyQt4 import QtCore

class LineTool():
    def __init__(self):
        self.line = None
        self.Gline = None
        self.active = False
        
    def start(self, startpoint, scene):
        self.line = QtCore.QLineF(startpoint, startpoint)
        self.Gline = scene.addLine(self.line)
        
        self.active = True
        
    def isActive(self):
        return self.active
    
    def mouseMove(self, cursorPos):
        self.endPoint(cursorPos)
    
    def end(self, endpos):
        self.endPoint(endpos)
        self.__init__()
    
    def endPoint(self, pos):
        self.line.setP2(pos)
        self.Gline.setLine(self.line)
        
    def pressure(self, pres):
        pass
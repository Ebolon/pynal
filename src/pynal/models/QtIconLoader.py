# -*- coding: utf-8 -*-
'''
'''
import os
from collections import defaultdict

from PyQt4 import QtGui
from PyQt4 import QtCore

def icon(name, fallback=None):
    icon = loadIcon(name)
    
    if icon is None:
        return fallback
    
    return icon
    
def loadIcon(name):
    theme = themeName()
    
    if theme is None:
        visited = []
        entries = findIconHelper(theme, name, visited)
        for entry in entries:
            size = entry.size()
            icon.addFile(entry.filename,
                         QtCore.QSize(size, size),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return icon

def themeName():
    global userTheme
    global systemTheme
    
    if userTheme is None:
        return systemTheme
    else:
        kde4 = kdeVersion() >= 4
        if kde4:
            defaultPath = "/usr/share/icons/default.kde4"
        else:
            defaultPath = "/usr/share/icons/default.kde"
            
            
def systemThemeName():
    if sessionIsGnome():
        pass
    else:
        kde4 = kdeVersion() >= 4
        if kde4:
            defaultPath = "/usr/share/icons/default.kde4"
        else:
            defaultPath = "/usr/share/icons/default.kde"
            
def sessionIsGnome():
    return False

def kdeVersion():
    try:
        return os.environ["KDE_SESSION_VERSION"]
    except:
        pass
    
def findIconHelper(theme, name, visited):
    
    
systemTheme = systemThemeName()
userTheme = systemTheme       
    
if __name__ == '__main__':
    moep = icon("document-new")
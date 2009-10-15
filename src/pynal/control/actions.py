# -*- coding: utf-8 -*-
'''
Module containing actions that can be displayed in a toolbar or menu.

For the moment all actions will be created here. Distribution to submodules
will be done when it gets stupidly crowded in this one.
'''
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction

import pynal.models.fdIconLoader as iconloader
#===========================================================================
# File management actions
#===========================================================================
""" Create a new file/document. """
new_file_action = None

""" Open an existing file/document. """
open_file_action = None

""" Save the currently open file/document. """
save_file_action = None

def init(parent):
    """ Create the action objects with the given MainWindow as the parent. """
    create_file_actions(parent)

def create_file_actions(parent):
    """ Create the actions categorized as file_actions :D """
    global open_file_action
    open_file_action = QAction(parent)
    open_file_action.setText("Open")
    open_file_action.setIcon(QtGui.QIcon(iconloader.find_icon("document-open", 32)))
    QAction.connect(open_file_action, SIGNAL("triggered()"), parent.open_file)

    global new_file_action
    new_file_action = QAction(parent)
    new_file_action.setText("New")
    new_file_action.setIcon(QtGui.QIcon(iconloader.find_icon("document-new", 32)))
    QAction.connect(new_file_action, SIGNAL("triggered()"), parent.new_file)

    global save_file_action
    save_file_action = QAction(parent)
    save_file_action.setText("Save")
    save_file_action.setIcon(QtGui.QIcon(iconloader.find_icon("document-save", 32)))
    QAction.connect(save_file_action, SIGNAL("triggered()"), parent.save_file)
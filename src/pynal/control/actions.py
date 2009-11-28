# -*- coding: utf-8 -*-
'''
Module containing actions that can be displayed in a toolbar or menu.

For the moment all actions will be created here. Distribution to submodules
will be done when it gets stupidly crowded in this one.

TODO: extend action_definitions for: tooltip, accelerator, shortcut
'''
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyKDE4 import kdeui
from PyKDE4 import kdecore
from PyKDE4.kdeui import KAction

import pynal.models.iconcache as iconcache

action_definitions = {} # Contains the definitions for all actions
toolbar_actions = {}    # action_name -> KAction for all created toolbar actions
menu_actions = {}       # action_name -> KAction for all created menu actions

parent = None # The global parent for all actions (usually the MainWindow)

def init(control, window):
    """
    Create the action objects with the given MainWindow as the parent.

    control -- the MainWindowControl object that receives the actions signals.
    parent  -- the MainWindow that is used as a parent for the actions.
    """
    global parent
    parent = window

    global action_definitions
    action_definitions.clear()

    create_app_actions(control, parent)
    create_file_actions(control, parent)
    create_document_actions(control, parent)
    create_debug_actions(control, parent)
    create_tools(control, parent)
    create_page_actions(control, parent)

def create_tools(control, parent):
    global action_definitions

    """ Selects the scroll tool to navigate the document. """
    action_definitions["tool_scroll"] = {
         "text"   : "Scroll",
         "icon"   : "transform-move",
         "action" : control.set_tool_scroll,
         "checkable" : True
     }

    action_definitions["tool_pen"] = {
         "text"   : "Pen tool",
         "icon"   : "draw-freehand",
         "action" : control.set_tool_scroll,
         "checkable" : True
     }

    action_definitions["tool_eraser"] = {
         "text"   : "Eraser",
         "icon"   : "draw-eraser",
         "action" : control.set_tool_scroll,
         "checkable" : True
     }

    action_definitions["tool_select"] = {
         "text"   : "Box select",
         "icon"   : "select-rectangular",
         "action" : control.set_tool_select,
         "checkable" : True
     }

def create_page_actions(control, parent):
    global action_definitions

    """ Zoom the document to the width of the current document/page. """
    action_definitions["page_new_after"] = {
         "text"   : "Append a new page after this",
#         "icon"   : "document-new",
         "icon"   : "archive-insert",
     }

    """ Zoom the document to the width of the current document/page. """
    action_definitions["page_up"] = {
         "text"   : "Move this page up",
         "icon"   : "go-up",
     }

    """ Zoom the document to the width of the current document/page. """
    action_definitions["page_down"] = {
         "text"   : "Move this page down",
         "icon"   : "go-down",
    }

    action_definitions["page_remove"] = {
         "text"   : "Remove this page",
#         "icon"   : "edit-delete",
         "icon"   : "archive-remove",
    }

    action_definitions["page_duplicate"] = {
         "text"   : "Duplicate this page",
         "icon"   : "edit-copy",
    }

    action_definitions["page_bg_plain"] = {
         "text"   : "Set a plain background.",
         "icon"   : "page-simple",
     }

    action_definitions["page_bg_checked"] = {
         "text"   : "Set a checked background.",
         "icon"   : "page-2sides",
     }

def create_document_actions(control, parent):
    global action_definitions

    """ Zoom the document to the width of the current document/page. """
    action_definitions["doc_zoom_width"] = {
         "text"   : "Zoom to page width",
         "icon"   : "zoom-fit-width",
         "action" : control.zoom_width
     }

    """ Zoom the document to 100%. """
    action_definitions["doc_zoom_100"] = {
         "text"   : "Zoom to original size",
         "icon"   : "zoom-original",
         "action" : control.zoom_original
     }

    """ Zoom the document to fit the whole page on screen. """
    action_definitions["doc_zoom_fit"] = {
         "text"   : "Zoom to fit",
         "icon"   : "zoom-fit-best",
         "action" : control.zoom_fit
     }

    """ Zoom the document to a bigger scale. """
    action_definitions["doc_zoom_in"] = {
         "text"   : "Zoom in",
         "icon"   : "zoom-in",
         "action" : control.zoom_in
     }

    """ Zoom the document to a smaller scale. """
    action_definitions["doc_zoom_out"] = {
         "text"   : "Zoom out",
         "icon"   : "zoom-out",
         "action" : control.zoom_out
     }

def create_debug_actions(control, parent):
    global action_definitions
    pass # No debug actions atm


def create_app_actions(control, parent):
    global action_definitions

    """ Create a new file/document. """
    action_definitions["exit_app_action"] = {
         "text"   : "Exit",
         "action" : control.exit
    }

def create_file_actions(control, parent):
    """
    action definitions for file actions are created here.

    TODO: might remove the parent parameter as it does not seem to be used.
    """
    global action_definitions

    """ Create a new file/document. """
    action_definitions["new_file_action"] = {
         "text"   : "New",
         "icon"   : "document-new",
         "action" : control.new_file
     }

    """ Open a file/document. """
    action_definitions["open_file_action"] = {
         "text"   : "Open",
         "icon"   : "document-open",
         "action" : control.open_file
     }

    """ Save the current file/document. """
    action_definitions["save_file_action"] = {
         "text"   : "Save",
         "icon"   : "document-save",
         "action" : control.save_file
     }

def toolbar(name, group=None, callable=None):
    """
    Returns the action with the given name for toolbar use.

    Toolbar use means that there is an icon without text.

    Needed configuration keys:
    icon, action

    Ignored keys:
    text

    Parameters:
      name     -- The name of the action.

      group    -- The QActionGroup to add this action to.
      callable -- The callable to call when the action is triggered.
                  Can be used to override the action in the definition or provide one.
    """
    global toolbar_actions
    action = toolbar_actions.get(name, None)

    if action is None:
        # Create the toolbar action and insert it into the toolbar_actions dict
        global parent
        global action_definitions

        config = action_definitions.get(name, None)
        if config is None:
            return None #Without the config no action can be created

        if group is None:
            action = KAction(parent)
        else:
            action = KAction(group)

        # Will result in a KeyError when the icon is not set in the config.
        # This is slightly wanted behaviour, as the icon is needed for a
        # toolbar action.
        action.setIcon(iconcache.get(config["icon"], 32))

        if "checkable" in config:
            action.setCheckable(True)

        # Same exception is wanted here. As an alternative one can specify a callable as a parameter.
        if callable is not None:
            action.triggered.connect(callable)
        else:
            action.triggered.connect(config["action"])

        if "text" in config:
            action.setText(config["text"])

        toolbar_actions["name"] = action

    return action

def menu(name):
    """
    Returns the action with the given name for menu use.

    Menu use that the action has a text and might have an icon.

    Needed configuration keys:
    text, action

    Optional keys:
    icon

    Parameters:
      name -- The name of the action,
    """
    global menu_actions
    action = menu_actions.get(name, None)

    if action is None:
        # Create the toolbar action and insert it into the toolbar_actions dict
        global parent
        global action_definitions

        config = action_definitions.get(name, None)
        if config is None:
            return None #Without the config no action can be created

        action = KAction(parent)

        if "icon" in config:
            action.setIcon(QtGui.QIcon(iconloader.find_icon(config["icon"], 48)))

        if "checkable" in config:
            action.setCheckable(True)

        # Will result in a KeyError when the text is not set in the config.
        # This is slightly wanted behaviour, as the text is needed for a
        # menu action.
        action.setText(config["text"])

        # Same exception is wanted here.
        action.triggered.connect(config["action"])

        menu_actions["name"] = action

    return action

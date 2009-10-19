# -*- coding: utf-8 -*-
'''
Loads and manages icons that are used by pynal.
Once icons are loaded they are saved in a dict to prevent
unnecessary lookups with the fdIconLoader.
'''
from PyQt4 import QtGui
import fdIconLoader

"""
Contains icons that have been loaded. The dict maps the
cache_name to the created QIcon. The cache_name is formed
by icon_name + "." + icon_size.
"""
loaded_icons = {}

def get(name, size=32):
    """
    Returns the icon of the specified name and size.

    Or None when no icon with the name could be found by the icon loader.
    """
    global loaded_icons
    icon_cache_name = name + "." + str(size)
    icon = loaded_icons.get(icon_cache_name, None)

    if icon is None:
        icon_path = fdIconLoader.find_icon(name, size)
        icon = QtGui.QIcon(icon_path)
        loaded_icons[icon_cache_name] = icon

    return icon
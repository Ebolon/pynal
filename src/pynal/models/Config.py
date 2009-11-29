# -*- coding: utf-8 -*-
'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
import os, ConfigParser

from PyQt4 import QtCore
from PyQt4 import QtGui


#===============================================================================
# Application information constants
#===============================================================================
# Name of the application.
appname = "pynal"

# Current version.
version = "0.1"

# Readable application name to display.
readable_appname = "Pynal"

# The KDE catalog specifier.
catalog = "catalog"

# The homepage of the app.
homepage = "http://github.com/dominiks/pynal"

# License for the code.
license = "BSD"

# The number of worker threads that can be active at the same time
# Wtf, using more than one thread for pdf rendering brings a nice crash.
threadpool_size = 1

# Space in pixels between the lower and upper border of two pages.
space_between_pages = 20

# List of files to open when the application has started.
open_files = []

#===============================================================================
# Page settings
#===============================================================================
# Resolution to use when rendering pdf pages to QImages.
pdf_base_dpi = 72.0 # This is the default for QtPoppler and is needed for size calculations.

# The minimum space between to pages (in pixels at zoom 1.0). This scales with the zoom level.
min_space_between_pages = 10

# Predefined page format
page_size_A4 = QtCore.QSizeF(595, 842)

# Color to use for the lines in checked bg pages.
checked_line_color = QtGui.QColor(123, 175, 246)

def parse_args(args):
    """ Parse the list of arguments and do something useful, like pass. """
    global open_files
    for pos in range(len(args)):
        arg = args[pos]
        if not arg.startswith("-") and arg.endswith(".pdf"):
            open_files.append(arg)

def add_default_values(config):
    """
    These are the default configuration values for the ConfigParser.
    """
    config.add_section("Main")
    config.set("Main", "window_width", "600")
    config.set("Main", "window_height", "600")
    config.set("Main", "window_maximized", "false")

    config.add_section("Rendering")
    config.set("Rendering", "use_opengl", "false")

    config.add_section("checked background")
    config.set("checked background", "size", "17")


# -*- coding: utf-8 -*-
'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

from PyKDE4.kdecore import KSharedConfig, KCmdLineOptions, ki18n

#===============================================================================
# Application information constants
#===============================================================================
# Name of the application.
appname = "pynal"

# Current version.
version = "0.1"

# Readable application name to display.
readable_appname = "Pynal"

# Description
description = "Journaling application bla bla, use on a tablet."
description_long = "Many words here. But actually not that many more than for the short \
                    description - ah there we go."

# Author information
author = "Dominik Schacht"
author_email = "domschacht@gmail.com"

# Platforms the program runs on
platforms = "Any"

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

# The zValue for the background of pages within the QGraphicsScene
background_z_value = -42

#===============================================================================
# Page settings
#===============================================================================
# Resolution to use when rendering pdf pages to QImages.
pdf_base_dpi = 72.0 # This is the default for QtPoppler and is needed for size calculations.

# The maximum amount of memory that can be used for background pixmaps in kb.
max_background_cache_size = 1024 * 64

# The minimum space between to pages (in pixels at zoom 1.0). This scales with the zoom level.
min_space_between_pages = 10

# Predefined page format (in pixel)
page_size_A4 = QtCore.QSizeF(595, 842)

page_size_default = page_size_A4

# Color to use for the lines in checked bg pages.
checked_line_color = QtGui.QColor(123, 175, 246)

# Limits for manual scaling
zoom_max = 3
zoom_min = 0.1

config = None

def init_config():
    global config
    config = KSharedConfig.openConfig("pynalrc")
    add_default_values(config)

def get_param_options():
    """
    Add the parameters that are to be recognized by pynal to a
    KCmdLineOptions object.

    Options:
      <files> -- A list of files that will be opened after start.
    """
    options = KCmdLineOptions()

    options.add("+[<files>]", ki18n("Files to open on startup."))

    return options

def get_group(name):
    """
    Return the requested KConfigGroup from the config.
    Convenience access to the KSharedConfig.
    """
    global config
    return config.group(name)

def add_default_values(config):
    """
    These are the default configuration values for the ConfigParser.

    Don't think this is necessary. Should find a better way.
    """
#    rendering = KConfigGroup(config, "rendering")
#    rendering.writeEntry("use_opengl", False)
#
#    backgrounds = KConfigGroup(config, "backgrounds")
#    backgrounds.writeEntry("checked_size", 17)
    pass

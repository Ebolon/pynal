# -*- coding: utf-8 -*-
'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
import os, ConfigParser

from PyQt4 import QtGui


#===============================================================================
# Application information constants
#===============================================================================
# Name of the application.
appname = "Pynal"

# Current version.
version = "0.1"

# The homepage of the app.
homepage = "http://github.com/dominiks/pynal"

# License for the code.
license = "BSD"

# Use opengl
use_opengl = True

# Initial width of the main window.
window_width = 600

# Initial height of the main window.
window_height = 600

# The number of worker threads that can be active at the same time
# Wtf, using more than one thread for pdf rendering brings a nice crash.
threadpool_size = 1

# Space in pixels between the lower and upper border of two pages.
space_between_pages = 20

# Resolution to use when rendering pdf pages to QImages.
pdf_base_dpi = 72 #This is the default for QtPoppler and is needed for size calculations.

# List of files to open when the application has started.
open_files = []

# User specific and dynamic settings are stored in this ConfigParser object
config = None

def parse_args(args):
    """ Parse the list of arguments and do something useful, like pass. """
    global open_files
    for pos in range(len(args)):
        arg = args[pos]
        if not arg.startswith("-") and arg.endswith(".pdf"):
            open_files.append(arg)

def load_config():
    """ Load the configuration file for the current user. """
    global config
    config = ConfigParser.SafeConfigParser()
    home = os.environ.get("HOME")
    conf = os.environ.get("XDG_CONFIG_HOME", "")
    path_configfile = os.path.join(home, conf, "pynal.conf")
    config.read(path_configfile)

def save_config():
    """ Save the config to the user's config file. """
    global config
    home = os.environ.get("HOME")
    conf = os.environ.get("XDG_CONFIG_HOME", "")
    path_configfile = os.path.join(home, conf, "pynal.conf")

    with open(path_configfile) as file:
        config.write(file)

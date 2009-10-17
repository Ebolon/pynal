# -*- coding: utf-8 -*-
'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
from PyQt4 import QtGui
# Name of the application.
appname = "Pynal"

# Current version.
version = "0.1"

# The homepage of the app.
homepage = "http://github.com/dominiks/pynal"

# License for the code.
license = "BSD"


# Initial width of the main window.
window_width = 600

# Initial height of the main window.
window_height = 600


# Resolution to use when rendering pdf pages to QImages.
pdf_render_dpi_x = QtGui.QX11Info.appDpiX() * 2
pdf_render_dpi_y = QtGui.QX11Info.appDpiY() * 2

def parse_args(args):
    """ Parse the list of arguments and do something useful, like pass. """
    pass

def load_config():
    """ Load the configuration file for the current user. """
    pass

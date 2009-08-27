# -*- coding: utf-8 -*-
'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
# Name of the application.
appname = "Pynal"

# Current version.
version = "0.1"

# The homepage of the app.
homepage = "http://github.com/dominiks/pynal"

# License for the code.
license = ""


# Initial width of the main window.
window_width = 600

# Initial height of the main window.
window_height = 600


# Resolution to use when rendering pdf pages to QImages.
pdf_render_dpi = 150

def parse_args(args):
    """ Parse the list of arguments and do something useful, like pass. """
    pass

def load_config():
    """ Load the configuration file for the current user. """
    pass

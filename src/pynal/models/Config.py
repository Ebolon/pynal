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

# The number of worker threads that can be active at the same time
# Wtf, using more than one thread for pdf rendering brings a nice crash.
threadpool_size = 1

# Space in pixels between the lower and upper border of two pages.
space_between_pages = 20

# Resolution to use when rendering pdf pages to QImages.
pdf_base_dpi = 72.0 # This is the default for QtPoppler and is needed for size calculations.

# List of files to open when the application has started.
open_files = []

# User specific and dynamic settings are stored in this ConfigParser object.
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
    global default_configs
    config = ConfigParser.SafeConfigParser()

    add_default_values(config)

    home = os.environ.get("HOME")
    conf = os.environ.get("XDG_CONFIG_HOME", "")
    path_configfile = os.path.join(home, conf, "pynal", "config")
    config.read(path_configfile)

def save_config():
    """ Save the config to the user's config file. """
    global config

    if not os.path.exists(get_config_path()):
        os.makedirs(get_config_path())

    with open(get_config_file(), "w") as file:
        config.write(file)

def get_config_path():
    """
    Resolve the path to the configuration directory.

    TODO: what if XDG_CONFIG_HOME is not set?
    """
    home = os.environ.get("HOME")
    conf = os.environ.get("XDG_CONFIG_HOME", "")
    return os.path.join(home, conf, "pynal")

def get_config_file():
    """ resolve the path to the configuration file. """
    return os.path.join(get_config_path(), "config")

def get(section, key):
    """ Return a configuration value as a string. """
    return config.get(section, key)

def get_int(section, key):
    """ Return a configuration value as an integer. """
    return config.getint(section, key)

def get_float(section, key):
    """ Return a configuration value as a float. """
    return config.getfloat(section, key)

def get_bool(section, key):
    """ Return a configuration value as a boolean. """
    return config.getboolean(section, key)

def set(section, key, value):
    """ Set a configuration value. """
    config.set(section, key, value)

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


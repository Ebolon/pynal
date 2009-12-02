# -*- coding: utf-8 -*-
'''
Entry point for the pynal appliaction.

Parses the startup parameters and creates a config object for the app.
'''
import sys

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication

from pynal.models import Config
from pynal.view.MainWindow import MainWindow

def load_config(args):
    """ Creates the configuration object that will be used in this instance. """
    return Config(args)

def start():
    Config.parse_args(sys.argv)

    appName = Config.appname
    catalog = Config.catalog
    programName = ki18n(Config.readable_appname)
    version = Config.version
    description = ki18n("A tablet annotation and journaling application.")
    license = KAboutData.License_BSD
    copyright = ki18n("(C) 2009 Dominik Schacht")
    text = ki18n("Whee, greetings.")
    homepage = Config.homepage
    bugemail = "dominik.schacht@gmail.com"

    aboutData = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homepage, bugemail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    Config.init_config() # Init after the KApplication has been created.

    mw = MainWindow()
    mw.show()

    result = app.exec_()

    return result

if __name__ == "__main__":
    sys.exit(start())

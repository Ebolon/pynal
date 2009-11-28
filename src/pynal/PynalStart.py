# -*- coding: utf-8 -*-
'''
Entry point for the pynal appliaction.

Parses the startup parameters and creates a config object for the app.
'''
import sys

from PyQt4 import QtGui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication

from pynal.models import Config
from pynal.view.MainWindow import MainWindow

def load_config(args):
    """ Creates the configuration object that will be used in this instance. """
    return Config(args)

def start():
    Config.parse_args(sys.argv)
    Config.load_config()

    appName = "KApplication"
    catalog = "catalog"
    programName = ki18n("Application 01")
    version = "1.0"
    description = ki18n("KApplication/KMAinWindow/KAboutData example")
    license = KAboutData.License_GPL
    copyright = ki18n("(C) 2009 Dominik Schacht")
    text = ki18n("derText")
    homepage = "github.org/dominiks"
    bugemail = "dominik.schacht@gmail.com"

    aboutData = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homepage, bugemail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()

    mw = MainWindow()
    mw.show()

    result = app.exec_()

    return result

if __name__ == "__main__":
    sys.exit(start())

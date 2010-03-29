# -*- coding: utf-8 -*-
'''
Slightly resembles an install script, but actually there is not much
to install.
'''
import os
import sys

from distutils.core import setup

sys.path.append("src")

from pynal.models import Config

pynal_data_files = [
        ("share/applications", ["resources/pynal.desktop"]),
        ("share/pynal", ["resources/pynalui.rc"]),
                    ]

setup(name=Config.appname.lower(),
      version=Config.version,
      description=Config.description,
      long_description=Config.description_long,
      author=Config.author,
      author_email=Config.author_email,
      platforms=Config.platforms,
      url=Config.homepage,
      license=Config.license,
      package_dir={"pynal": "src/pynal"},
      packages=["pynal", "pynal.models", "pynal.view", "pynal.control"],
      scripts=["pynal"],
      data_files=pynal_data_files)


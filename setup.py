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

setup(name=Config.appname.lower(), version=Config.version,
      url=Config.homepage, license=Config.license,
      package_dir={"pynal": "src/pynal"},
      packages=["pynal", "pynal.models", "pynal.view", "pynal.control"],
      scripts=["pynal"],)


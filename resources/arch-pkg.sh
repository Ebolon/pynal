#!/bin/sh
# Creates a package for the arch package system.
# When successful, file will be placed in dist/ .
cd ..
python setup.py sdist
cp resources/PKGBUILD dist/PKGBUILD
cd dist
makepkg -g >> PKGBUILD
makepkg

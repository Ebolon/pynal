=====
Pynal
=====
Journaling and PDF annotation application
-----------------------------------------

Introduction
============
Intended for use on tablets to make quick illustrations and add notes
and other annotations.

For installation instructions see ``docs/INSTALL.rst``.

The source is published under the 2-clause BSD license. For details 
see ``docs/LICENSE``.

Authors
=======
* Dominik Schacht <domschacht@gmail.com>
* Simon Pizonka <simzonka@gmail.com>
* Samuel Spiza <sam.spiza@gmail.com>

Contact
=======
For feedback or to report bugs go to http://github.com/dominiks/pynal

Maintaining author is Dominik Schacht <domschacht@gmail.com>

Notes
=====
When encountering errors related to QtPoppler when starting the application
it might help to reinstall/update the PyPoppler-qt4 bindings. For detailed
instructions see ``docs/INSTALL.rst``.

The pynalui.rc contains the xml configuration for the toolbars and menus.
When the application is installed the file will be moved automatically, if
that is not the case move it to::

    $HOME/.kde4/share/apps/pynal/pynalui.rc

This file is formatted with reStructuredText_ markup.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

Files
=====
Files that can be found in this file tree and their use:

=========================  ==========================================================================
 File                      Description
=========================  ==========================================================================
/MANIFEST                  Used by setup.py to determine which files to include in the distributions.
/README.rst                This file.
/setup.py                  The setup script. ``python setup.py --help`` for more info.
/resources/PKGBUILD        The configuration file for the arch packaging system.
/resources/arch-pkg.sh     Script to create an arch package.
/resources/pynal           A startup script that is used to start the application when installed.
/resources/pynal.desktop   Application descriptor for the installed program.
/resources/pynalui.rc      Default GUI configuration file.
=========================  ==========================================================================

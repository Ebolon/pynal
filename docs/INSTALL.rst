=====
Pynal
=====
Installation instructions
-------------------------

Preparations
============
Pynal uses *PyPoppler-qt4* to render PDF pages and is a necessary requirement.
*PyPoppler-qt4* is provided with Pynal in ``/pypoppler-qt4``. The version that
is provided is a snapshot from pyqt4-extrawidgets_. The source for pypoppler-qt4
can be found at the pardus-project_.

.. _pyqt4-extrawidgets: http://code.google.com/p/pyqt4-extrawidgets/
.. _pardus-project: http://svn.pardus.org.tr/uludag/trunk/pypoppler-qt4/

License information and authors can be found in ``/pypoppler-qt4/LICENSE`` and ``/pypoppler-qt4/AUTHORS``. 

Steps to install the bindings ::

    cd pypoppler-qt4
    python configure.py
    make
    make install

Installation process
====================
Pynal is distributed as python modules so there is no need
for a build process. To install the modules execute ::

    python setup.py install

Starting
========
Pynal can then be started by executing ``pynal`` in a terminal.

To start without installing (for development) change into the src/pynal directory and execute ::

    python PynalStart.py


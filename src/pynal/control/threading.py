# -*- coding: utf-8 -*-
'''
This is a sad try of using the QThreadPool which does not correctly work
in PyQt as there is no way of removing the python objects after the
runnables have completed.

So now there is a semaphore restricting the maximum number of running threads
and threads have to call the semaphores acquire and release functions.
'''
from PyQt4 import QtCore

import pynal.models.Config as Config

semaphore = QtCore.QSemaphore(Config.threadpool_size)

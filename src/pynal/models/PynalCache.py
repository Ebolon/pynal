# -*- coding: utf-8 -*-'''
import collections

from PyQt4 import QtCore, QtGui

class PynalCache(object):
    '''
    Limits the number of loaded page pixmaps.
    '''

    """ A pixmap that is a background of a page. """
    TYPE_BACKGROUND = 1

    """ A pixmap that is used as a thumbnail or placeholder. """
    TYPE_THUMBNAIL = 2

    """ The render of a complete page, with bg and children. """
    TYPE_COMPLETE = 3

    MAX_BACKGROUNDS = 2


    def __init__(self):
        '''
        Create a new cache.
        '''
        self.backgrounds = collections.deque(maxlen=5)

    def addBackground(self, page, pixmap):
        """
        Add a page to the background cache.
        """
        if page in self.backgrounds:
            self.backgrounds.remove(page)

        while len(self.backgrounds) >= PynalCache.MAX_BACKGROUNDS:
            page = self.backgrounds.pop()
            page.clear_bg_pixmap()

        self.backgrounds.appendleft(page)

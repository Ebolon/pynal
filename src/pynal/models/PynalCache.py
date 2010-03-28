# -*- coding: utf-8 -*-'''
import collections

from PyQt4 import QtCore, QtGui

class PynalCache(object):
    """
    Limits the number of loaded page pixmaps.

    Currently it works by counting the pages that have registered
    a background image here and removes the pixmaps of the last
    added page when the limit is reached.

    A better version of this could be based on the size in bytes
    of the pixmaps.
    """

    """ The maximum amount of loaded backgrounds. """
    MAX_BACKGROUNDS = 25

    def __init__(self):
        '''
        Create a new cache.
        '''
        self.backgrounds = collections.deque()

    def addBackground(self, page, pixmap):
        """
        Add a page to the background cache.

        Parameters:
          page   -- The page that the background belongs to.
          pixmap -- The pixmap of the background that is added.
                    Currently not used.
        """
        if page in self.backgrounds:
            self.backgrounds.remove(page)

        while len(self.backgrounds) >= PynalCache.MAX_BACKGROUNDS:
            remove_page = self.backgrounds.pop()
            remove_page.clear_bg_pixmap()

        self.backgrounds.appendleft(page)

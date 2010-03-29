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

    """ The maximum amount of memory that can be used for background pixmaps in kb. """
    MAX_BACKGROUND_SIZE = 1024 * 20

    def __init__(self):
        '''
        Create a new cache.
        '''
        self.bg_size = 0
        self.backgrounds = collections.deque()

    def addBackground(self, page, pixmap):
        """
        Add a page to the background cache.

        Parameters:
          page   -- The page that the background belongs to.
          pixmap -- The pixmap of the background that is added.
                    Currently not used.
        """
        self.bg_size += pixmap_size(pixmap)

        if page in self.backgrounds:
            self.backgrounds.remove(page)

        while self.bg_size >= PynalCache.MAX_BACKGROUND_SIZE:
            remove_page = self.backgrounds.pop()
            old_pixmap = remove_page.bg_graphics_item.pixmap()
            old_size = pixmap_size(old_pixmap)
            self.bg_size -= old_size
            remove_page.clear_bg_pixmap()

        self.backgrounds.appendleft(page)

def pixmap_size(pixmap):
    """ Calculates an estimate for the size in kb of a pixmap. """
    return pixmap.width() * pixmap.height() * pixmap.depth() / 8 / 1024

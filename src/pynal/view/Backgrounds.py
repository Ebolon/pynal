# -*- coding: utf-8 -*-
'''
This module contains the class definition and convenience methods
to create BackgroundImage objects that can be used as the bg_source
for a PynalDocument. These are similiar to the QtPoppler.Poppler.Page
but don't use a PDF as the backend.

Possible uses are images or patterns for graph or lined paper.
'''

def empty_background():
    """
    Create and configure a bg_source for a plain
    and empty page.
    """
    bg = BackgroundImage()
    return bg

class BackgroundImage():
    """
    Used as a bg_source by the DocumentPage to present a
    single image (or style). Functions resemble the API
    of QtPoppler.Poppler.Page so no typechecking is
    necessary when working with these objects.
    """

    def __init__(self):
        pass

    def pageSizeF(self):
        pass

    def renderToImage(self, dpix, dpiy):
        pass
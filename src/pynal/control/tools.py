'''
Contains the current tool and its configuration and the class definitions for different tools.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

class Tool():
    '''
    Base class of all tools.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cursor = QtCore.Qt.ArrowCursor

    def mouseDoubleClickEvent(self, event, document):
        """
        Process the event of a double click.
        TODO: The dclick might be useful to display a quick menu.
        """
        event.ignore()

    def mouseMoveEvent(self, event, document):
        """ Process the event of the mouse moving. """
        event.ignore()

    def mousePressEvent(self, event, document):
        """ Process the event of a pressed mouse key. """
        event.ignore()

    def mouseReleaseEvent(self, event, document):
        """ Process the event of a released mouse key. """
        event.ignore()

    def tabletEvent(self, event, document):
        """ Process the event of a tablet event. """
        event.ignore()

class ScrollTool(Tool):
    """
    The scroll tool. Not a full fledged tool as the pen or others as the
    functionality is provided by the QGraphicsView.
    """

    def __init__(self):
        Tool.__init__(self)

class SelectTool(Tool):
    """
    The selection tool. As small as the scroll tool as the logic
    is provided by the QGraphicsView.

    TODO: might want to merge with the scroll tool.
    """

    def __init__(self):
        Tool.__init__(self)

class PenTool(Tool):
    """
    Pen with some debug functionality. Not really usable as a free hand
    pen.
    """

    def __init__(self):
        Tool.__init__(self)
        self.deviceDown = False

    def mousePressEvent(self, event, document):
        self.devideDown = True
        point_coords = document.mapToScene(event.pos())
        page = document.page_at(point_coords)

        if page is None:
            return

        # Create the QGraphicsItem that should be added to the page.
        page_point = page.mapFromScene(point_coords)
        circle = QtGui.QGraphicsEllipseItem(page)
        circle.setRect(QtCore.QRectF(page_point.x() - 20, page_point.y() - 20, 40, 40))
        circle.setZValue(1)

        # Create and push the UndoCommand.
        document.undo_stack.push(GraphicsItemCommand(document, circle))

    def mouseReleaseEvent(self, event, document):
        self.deviceDown = False

    def mouseMoveEvent(self, event, document):
        if not self.deviceDown:
            return

class GraphicsItemCommand(QtGui.QUndoCommand):
    """
    Base class for all undo commands that add an item to the page.
    Allows easy undo/redo of adding the item to the scene and page.

    Attributes:
      document -- The document that provides the undo stack and the scene.
      item     -- The item that is added to the document.
      page     -- The page the item is on.
    """

    def __init__(self, document, graphicsItem):
        """
        Creates a new GraphicsItemCommand that can be pushed on an UndoStack.
        Undo and redo changes the parent item of the graphicsItem. The parent
        is read from the graphicsItem when the command is created therefore it
        should have the parent before the command is created.

        Parameters:
          document     -- The document that contains the undo stack.
          graphicsItem -- The QGraphicsItem that is added to the scene.
        """
        QtGui.QUndoCommand.__init__(self)
        self.document = document
        self.item = graphicsItem
        self.page = graphicsItem.parentItem()

    def undo(self):
        """ Remove the item from the scene. """
        self.document.scene().removeItem(self.item)

    def redo(self):
        """ Move the item into the scene with the page as a parent. """
        self.item.setParentItem(self.page)

current_tool = Tool()

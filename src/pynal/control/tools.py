'''
Contains the current tool and its configuration and the class definitions for different tools.
'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from math import hypot

import pynal.view.Item as Item

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
    
    def type(self):
        return "default"

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

class EraserTool(Tool):
    #TODO: improve functionality
    """
    The erase tool.
    """
    def __init__(self):
        Tool.__init__(self)
        self.Line = None
        self.deviceDown = False
        self.lastPoint = None
        self.tabletActive = False
        self.page = None
      
    def mousePressEvent(self, event, document):
        """
        Start drawing.
        """
        point_coords = document.mapToScene(event.pos())
        self.page = document.page_at(point_coords)
        if self.page is not None:
            self.deviceDown = True
            self.Line = Item.Line(document, point_coords)
            self.lastPoint = point_coords

<<<<<<< HEAD
    def mouseReleaseEvent(self, event, document):
        """
        Stop drawing.
        """
        self.Line = None
        self.deviceDown = False

    def mouseMoveEvent(self, event, document):
        if not self.deviceDown:
            # no stroke
            return
        point_coords = document.mapToScene(event.pos())
        pageNow = document.page_at(point_coords)
        if pageNow is None:
            # out of page
            self.Line = None
            return
        if not self.page == pageNow:
            # other page - begin new stroke
            self.mousePressEvent(event, document)
            return
        if self.Line is None:
            # back again in drawing action
            self.mousePressEvent(event, document)
        self.page = pageNow
        x, y = abs(point_coords.x() - self.lastPoint.x()), abs(point_coords.y() - self.lastPoint.y())
        if((x + y) * 0.8 > 3):
            self.Line.addPoint(point_coords)
            colliding = document.scene().collidingItems(self.Line)
            for item in colliding:
                if item.type() == 65555:
                    document.scene().removeItem(item)
            self.lastPoint = point_coords

    def type(self):
        return "EraseTool"
        
class PenTool(Tool):
    """
    The pen tool.
    """
    def __init__(self):
        Tool.__init__(self)
        self.Line = None
        self.deviceDown = False
        self.lastPoint = None
        self.tabletActive = False
        self.page = None
        self.LineStyle = QtCore.Qt.SolidLine
    
    def setLineStyle(self, style):
        self.LineStyle = style
        
=======
>>>>>>> dom/master
    def mousePressEvent(self, event, document):
        """
        Start drawing.
        """
        point_coords = document.mapToScene(event.pos())
<<<<<<< HEAD
        self.page = document.page_at(point_coords)
        if self.page is not None:
            self.deviceDown = True
            self.Line = Item.Line(document, point_coords)
            self.Line.setStyle(self.LineStyle)
            command = CommandAddLine(document, self.Line, "Line")
            document.undoStack.push(command)
            self.Line.setParentItem(self.page)
            self.Line.setZValue(1)
            self.lastPoint = point_coords
=======
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
>>>>>>> dom/master

    def mouseReleaseEvent(self, event, document):
        """
        Stop drawing.
        """
        if self.Line is not None:
            self.Line.finalize()
        self.Line = None
        self.deviceDown = False

    def mouseMoveEvent(self, event, document):
        if not self.deviceDown:
            # no stroke
            return
        point_coords = document.mapToScene(event.pos())
        pageNow = document.page_at(point_coords)
        if pageNow is None:
            # out of page
            self.Line = None
            return
        if not self.page == pageNow:
            # other page - begin new stroke
            self.mousePressEvent(event, document)
            return
        if self.Line is None:
            # back again in drawing action
            self.mousePressEvent(event, document)
        self.page = pageNow
        x, y = abs(point_coords.x() - self.lastPoint.x()), abs(point_coords.y() - self.lastPoint.y())
        if((x + y) * 0.8 > 3):
            self.Line.addPoint(point_coords)
            self.lastPoint = point_coords

    def type(self):
        return "PenTool"

class CommandAddLine(QtGui.QUndoCommand):
    """
    Undo Line Class
    """
    def __init__(self, document, Line, description):
        super(CommandAddLine, self).__init__(description)
        self.Line = Line
        self.document = document

    def redo(self):
        self.document.scene().addItem(self.Line)

    def undo(self):
        self.document.scene().removeItem(self.Line)

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
        Create a new GraphicsItemCommand that can be pushed on an UndoStack.
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

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QPainter
from editor.EditorScene import EditorScene
from core.Node import BaseNode, Wire, LiveWire, InputLabelUnit, OutputUnit
from utils.nodeutils import *

class EditorEngine(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def init(self):
        self.editorScene = EditorScene(self)
        self.setScene(self.editorScene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoom = 10
        self.zoomStep = 1
        self.zoomMin = 0
        self.zoomMax = 16
        self.isDraggingWireForwards = False
        self.isDraggingWireBackwards = False
        self.activeDraggingWire = None
        self.liveDraggingWire = None
        self.nodes = []
        self.currentlySelectedNode = None

    def getElementAtMouse(self, event):
        position = event.pos()
        element = self.itemAt(position)
        return element
    
    def addNode(self, event):
        self.nodes.append(BaseNode(self.editorScene, "First Node", inputs=["label", "label"], outputs=["scalar"]))

    def deleteNode(self, event):
        counter = 0
        for node in self.nodes:
            if node.id == self.currentlySelectedNode.id:
                node.removeSelf()
                del self.nodes[counter]
            counter += 1
        print(self.nodes)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.addNode(event)
        if event.key() == Qt.Key_X:
            self.deleteNode(event)
        if event.key() == Qt.Key_Delete:
            self.deleteNode(event)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())
        if self.liveDraggingWire:
            self.liveDraggingWire.render(position.x(), position.y())
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons(), event.modifiers())
        super().mousePressEvent(fakeEvent)
    
    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons(), event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        element = self.getElementAtMouse(event)
        if type(element) is OutputUnit:
            self.isDraggingWireForwards = True
            self.activeDraggingWire = Wire(self.editorScene, miniguid(), startSocket=element)
            self.liveDraggingWire = LiveWire(self.editorScene, id="LIVEWIREFORWARDS", startSocket=element)
            return
        elif type(element) is InputLabelUnit:
            self.isDraggingWireBackwards = True
            self.activeDraggingWire = Wire(self.editorScene, miniguid(), endSocket=element)

            if self.isDraggingWireBackwards == True:
                for wire in self.activeDraggingWire.endSocket.parent.connectedWires:
                    if wire.id != self.activeDraggingWire.id:
                        if wire.endSocket.id == self.activeDraggingWire.endSocket.id:
                            wire.removeSelf()
                            del wire

            self.liveDraggingWire = LiveWire(self.editorScene, id="LIVEWIREBACKWARDS", endSocket=element)
            return
        else:
            if element:
                if isinstance(element, BaseNode):
                    self.currentlySelectedNode = element
                elif isinstance(element.parentItem(), BaseNode):
                    self.currentlySelectedNode = element.parentItem()
                elif isinstance(element.parentItem().parent, BaseNode):
                    self.currentlySelectedNode = element.parentItem().parent
        super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self, event):
        element = self.getElementAtMouse(event)

        # regardless of where we release the left click, self.liveDraggingWire must be removed from the scene
        if self.liveDraggingWire:
            self.liveDraggingWire.removeSelf()
            self.liveDraggingWire = None

        if type(element) is OutputUnit:
            if self.isDraggingWireBackwards == True:
                for wire in self.activeDraggingWire.endSocket.parent.connectedWires:
                    if wire.startSocket:
                        if wire.endSocket.id == self.activeDraggingWire.endSocket.id:
                            wire.removeSelf()
                            del wire
                if self.activeDraggingWire.endSocket.parent.id != element.parent.id:
                    self.isDraggingWireBackwards = False
                    self.activeDraggingWire.setStartSocket(element)
                self.activeDraggingWire = None
                return
        if type(element) is InputLabelUnit:
            if self.isDraggingWireForwards == True:
                for wire in element.parent.connectedWires:
                    if wire.endSocket:
                        if wire.endSocket.id == element.id:
                            wire.removeSelf()
                            del wire
                if self.activeDraggingWire.startSocket.parent.id != element.parent.id:
                    self.isDraggingWireForwards = False
                    self.activeDraggingWire.setEndSocket(element)
                self.activeDraggingWire = None
                return
        else:
            if self.activeDraggingWire:
                if self.isDraggingWireBackwards == True:
                    # check for failed wires which will have no startSocket set
                    for wire in self.activeDraggingWire.endSocket.parent.connectedWires:
                        if not wire.startSocket:
                            wire.removeSelf()
                            del wire
                    self.isDraggingWireBackwards = False
                if self.isDraggingWireForwards == True:
                    self.activeDraggingWire.removeSelf()
                    self.isDraggingWireForwards = False
                wire = self.activeDraggingWire
                self.activeDraggingWire = None
                del wire
        super().mouseReleaseEvent(event)
    
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
    
    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = self.zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomMin:
            self.zoom = self.zoomMin
            clamped = True

        if self.zoom > self.zoomMax:
            self.zoom = self.zoomMax
            clamped = True

        if not clamped:
            self.scale(zoomFactor, zoomFactor)
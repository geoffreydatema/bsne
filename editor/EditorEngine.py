from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QPainter
from editor.EditorScene import EditorScene
from core.Node import Wire, InputLabelUnit, OutputUnit

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
        self.isDraggingWire = False
        self.activeDraggingWire = None
        self.mousePosition = []

    def mouseMoveEvent(self, event):
        if self.isDraggingWire == True:
            position = self.mapToScene(event.pos())
            self.mousePosition = [position.x(), position.y()]
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

    def getItemAtMouse(self, event):
        position = event.pos()
        element = self.itemAt(position)
        return element

    def leftMouseButtonPress(self, event):
        element = self.getItemAtMouse(event)
        if type(element) is OutputUnit:
            self.isDraggingWire = True
            self.activeDraggingWire = Wire(self.editorScene, startSocket=element)
            return
        if type(element) is InputLabelUnit:
            # implement draging wire from input backwards to an output
            return
        super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self, event):
        element = self.getItemAtMouse(event)
        if type(element) is OutputUnit:
            return
        if type(element) is InputLabelUnit:
            self.draggingEdge = False
            self.activeDraggingWire.setEndSocket(element)
            return
        else:
            self.activeDraggingWire = None
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
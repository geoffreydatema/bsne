from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent
from editor.EditorScene import EditorScene

class EditorEngine(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def init(self):
        self.editorScene = EditorScene()
        self.setScene(self.editorScene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoom = 10
        self.zoomStep = 1
        self.zoomMin = 0
        self.zoomMax = 16

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
        return super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)
    
    def rightMouseButtonPress(self, event):
        return super().mousePressEvent(event)
    
    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)
    
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
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QColor, QBrush, QPainterPath, QFont, QCursor
from PyQt5.QtCore import Qt, QRectF, QPointF
from utils.nodeutils import *

class Wire(QGraphicsPathItem):
    def __init__(self, scene, id=None, startSocket=None, endSocket=None, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.id = id
        self.startSocket = startSocket
        self.endSocket = endSocket
        self.wireColour = QColor("#777777")
        self.wireColourSelected = QColor("#ffffff")
        self.wirePen = QPen(self.wireColour)
        self.wirePenSelected = QPen(self.wireColourSelected)
        self.wirePen.setWidthF(2.0)
        self.wirePenSelected.setWidthF(2.0)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.startPosition = []
        self.endPosition = []
        self.setStartPosition()
        self.setEndPosition()

        self.scene.addItem(self)
        
        if self.startSocket:
            self.startSocket.parent.connectedWires.append(self)
        if self.endSocket:
            self.endSocket.parent.connectedWires.append(self)
        
    def setStartPosition(self):
        if self.startSocket:
            self.startPosition = self.startSocket.getPosition()
    
    def setEndPosition(self):
        if self.endSocket:
            self.endPosition = self.endSocket.getPosition()

    def setStartSocket(self, element):
        self.startSocket = element
        self.setStartPosition()
        self.startSocket.parent.connectedWires.append(self)

    def setEndSocket(self, element):
        self.endSocket = element
        self.setEndPosition()
        self.endSocket.parent.connectedWires.append(self)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        if self.endSocket:
            self.updatePath()
            painter.setPen(self.wirePen if not self.isSelected() else self.wirePenSelected)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.path())

    def updatePath(self):
        if self.startPosition and self.endPosition:
            path = QPainterPath(QPointF(self.startPosition[0], self.startPosition[1]))
            path.lineTo(self.endPosition[0], self.endPosition[1])
            self.setPath(path)

    def removeSelf(self):
        print(f"deleting id {self.id}")
        if self.startSocket:
            index = 0
            for wire in self.startSocket.parent.connectedWires:
                if wire.id == self.id:
                    del self.startSocket.parent.connectedWires[index]
                index += 1
        if self.endSocket:
            if not self.id == "LIVEWIREFORWARDS" and not self.id == "LIVEWIREBACKWARDS":
                index = 0
                for wire in self.endSocket.parent.connectedWires:
                    if wire.id == self.id:
                        del self.endSocket.parent.connectedWires[index]
                    index += 1
        self.scene.removeItem(self)

class LiveWire(Wire):
    def __init__(self, scene, id=None, startSocket=None, parent=None):

        super().__init__(scene, id, startSocket, parent)

        # the live dragging wire has a lighter colour to help with user feedback
        self.wireColour = QColor("#999999")
        self.wirePen = QPen(self.wireColour)
        self.wirePen.setWidthF(2.0)

        # we need to allow the wire to render, so we give the sockets a True value depending on the direction of the wire
        if self.id == "LIVEWIREFORWARDS":
            self.endSocket = True

    def setEndPosition(self):
        if self.endSocket:
            return [self.endPosition[0], self.endPosition[1]]
        
    def render(self, x, y):
        self.endPosition = [x, y]
        if self.id == "LIVEWIREFORWARDS":
            self.setEndPosition()

class OutputUnit(QGraphicsItem):
    def __init__(self, id=None, index=0, label="Output", parent=None):
        super().__init__(parent)

        self.parent = parent
        self.id = id
        self.index = index
        self.socketSize = 8
        self.x = parent.x
        self.y = parent.y
        self.width = parent.width
        self.height = parent.unitSize
        self.padding = 8
        self.unitBrush = QBrush(QColor("#333333"))
        self.socketBrush = QBrush(QColor("#13FF00"))
        self.socketOutlinePen = QPen(QColor("#111111"))
        self.label = QGraphicsTextItem(parent=self)
        self.labelText = label
        self.labelColour = QColor("#FFFFFF")
        self.labelFont = QFont()

    def boundingRect(self):
        return QRectF(self.width - self.socketSize // 2, int((self.height * self.index) + self.height), self.socketSize, self.height).normalized()
    
    def paintSocket(self, painter):
        painter.setPen(self.socketOutlinePen)
        painter.setBrush(self.socketBrush)
        painter.drawEllipse(int(self.width - (self.socketSize // 2)), int((self.height * self.index) + (self.height * 1.5) - (self.socketSize // 2)), self.socketSize, self.socketSize)
        
    def paintLabel(self):
        self.label.setPlainText(self.labelText)
        self.label.setDefaultTextColor(self.labelColour)
        self.label.setPos(self.width - self.label.boundingRect().width() - self.padding, int((self.height * self.index) + self.height))
        self.labelFont.setPixelSize(14)
        self.label.setFont(self.labelFont)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintSocket(painter)
        self.paintLabel()

    def getPosition(self):
        return [self.x + self.width, self.y + int((self.height * self.index) + (self.height * 1.5))]

class InputLabelUnit(QGraphicsItem):
    def __init__(self, id=None, index=0, label="Undefined Label", parent=None):
        super().__init__(parent)

        self.parent = parent
        self.id = id
        self.index = index
        self.socketSize = 8
        self.x = parent.x
        self.y = parent.y
        self.width = parent.width
        self.height = parent.unitSize
        self.padding = 8
        self.unitBrush = QBrush(QColor("#333333"))
        self.socketBrush = QBrush(QColor("#ffaa00"))
        self.socketOutlinePen = QPen(QColor("#111111"))
        self.label = QGraphicsTextItem(parent=self)
        self.labelText = label
        self.labelColour = QColor("#FFFFFF")
        self.labelFont = QFont()

    def boundingRect(self):
        return QRectF(self.socketSize // 2, int((self.height * self.index) + self.height), -self.socketSize, self.height).normalized()
    
    def paintSocket(self, painter):
        painter.setPen(self.socketOutlinePen)
        painter.setBrush(self.socketBrush)
        painter.drawEllipse(-self.socketSize // 2, int((self.height * self.index) + (self.height * 1.5) - (self.socketSize // 2)), self.socketSize, self.socketSize)
        
    def paintLabel(self):
        self.label.setPlainText(self.labelText)
        self.label.setDefaultTextColor(self.labelColour)
        self.label.setPos(self.padding, int((self.height * self.index) + self.height))
        # self.label.setTextWidth(self.width - 2 * self.padding) # probably dont need this
        self.labelFont.setPixelSize(14)
        self.label.setFont(self.labelFont)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintSocket(painter)
        self.paintLabel()

    def getPosition(self):
        return [self.x, self.y + int((self.height * self.index) + (self.height * 1.5))]

#   Input Scalar Unit class

#   Input Vector Unit class

#   Input Text Unit class

class BaseNode(QGraphicsItem):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[], parent=None):
        super().__init__(parent)
        self.scene = scene
        self.id = miniguid()
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.x = 0
        self.y = 0
        self.radius = 8
        self.width = 200
        self.unitSize = 24
        self.unitStack = []
        self.initUnits()
        self.connectedWires = []
        self.unitCount = len(self.unitStack)
        self.height = (self.unitSize * 1.5) + (self.unitSize * self.unitCount)
        self.padding = 8
        self.titleColor = QColor("#dddddd")
        self.titleBrush = QBrush(QColor("#444444"))
        self.backgroundBrush = QBrush(QColor("#222222"))
        self.titleElement = QGraphicsTextItem(self)
        self.outlinePenUnselected = QPen(QColor("#111111"))
        self.outlinePenSelected = QPen(QColor("#cccccc"))
        
        self.init()
    
    def initUnits(self):
        unitIndexCounter = 0

        for output in self.outputs:
            self.unitStack.append(OutputUnit(miniguid(), unitIndexCounter, f"Output {unitIndexCounter}", parent=self))
            unitIndexCounter += 1
        
        for input in self.inputs:
            self.unitStack.append(InputLabelUnit(miniguid(), unitIndexCounter, f"Value {unitIndexCounter}", parent=self))
            unitIndexCounter += 1

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()

    def paintTitle(self, painter):
        titlePath = QPainterPath()
        titlePath.setFillRule(Qt.WindingFill)
        titlePath.addRoundedRect(0, 0, self.width, self.unitSize, self.radius, self.radius)
        titlePath.addRect(0, self.unitSize - self.radius, self.radius, self.radius)
        titlePath.addRect(self.width - self.radius, self.unitSize - self.radius, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.titleBrush)
        painter.drawPath(titlePath.simplified())

    def paintBottom(self, painter):
        bottomPath = QPainterPath()
        bottomPath.setFillRule(Qt.WindingFill)
        bottomPath.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawPath(bottomPath.simplified())

    def paintOutline(self, painter):
        outlinePath = QPainterPath()
        outlinePath.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(self.outlinePenUnselected if not self.isSelected() else self.outlinePenSelected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outlinePath.simplified())

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintBottom(painter)
        self.paintTitle(painter)
        self.paintOutline(painter)

    def init(self):
        self.titleElement.setPlainText(self.title)
        self.titleElement.setDefaultTextColor(self.titleColor)
        self.titleElement.setPos(self.padding, 0)
        # self.titleElement.setTextWidth(self.width - 2 * self.padding) # probably dont need this
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # self.scene.addNode(self)
        self.scene.addItem(self)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        for unit in self.unitStack:
            unit.x = self.x
            unit.y = self.y
        self.setPos(self.x, self.y)
    
    def getPosition(self):
        return(self.x, self.y)

    def updateConnectedWires(self):
        self.setPosition(self.pos().x(), self.pos().y())
        for wire in self.connectedWires:
            wire.setStartPosition()
            wire.setEndPosition()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.updateConnectedWires()

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PyQt5.QtCore import Qt, QRectF, QPointF

class Wire(QGraphicsPathItem):
    def __init__(self, scene, startSocket, endSocket, parent=None):
        super().__init__(parent)
        self.scene = scene
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
        self.startPosition = [0, 0]
        self.endPosition = [200, 100]

        self.scene.addItem(self)

    def setStartPosition(self, x, y):
        self.startPosition = [x, y]
    
    def setEndPosition(self, x, y):
        self.endPosition = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        painter.setPen(self.wirePen if not self.isSelected() else self.wirePenSelected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        path = QPainterPath(QPointF(self.startPosition[0], self.startPosition[1]))
        path.lineTo(self.endPosition[0], self.endPosition[1])
        self.setPath(path)

class OutputUnit(QGraphicsItem):
    def __init__(self, index=0, parent=None):
        super().__init__(parent)

        self.index = index
        self.socketSize = 8
        self.width = parent.width
        self.height = parent.unitSize
        self.unitBrush = QBrush(QColor("#333333"))
        self.socketBrush = QBrush(QColor("#13FF00"))
        self.socketOutlinePen = QPen(QColor("#111111"))

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()
    
    def paintSocket(self, painter):
        painter.setPen(self.socketOutlinePen)
        painter.setBrush(self.socketBrush)
        painter.drawEllipse(int(self.width - (self.socketSize // 2)), int((self.height * self.index) + (self.height * 1.5) - (self.socketSize // 2)), self.socketSize, self.socketSize)
        
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintSocket(painter)

class InputLabelUnit(QGraphicsItem):
    def __init__(self, index=0, label="Undefined Label", parent=None):
        super().__init__(parent)

        self.index = index
        self.socketSize = 8
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
        return QRectF(0, 0, self.width, self.height).normalized()
    
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

#   Input Scalar Unit class

#   Input Vector Unit class

#   Input Text Unit class

class BaseNode(QGraphicsItem):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[], parent=None):
        super().__init__(parent)
        self.scene = scene
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.tx = 0
        self.ty = 0
        self.radius = 8
        self.width = 200
        self.unitSize = 24

        self.unitStack = []
        self.unitStack.append(OutputUnit(0, parent=self))
        self.unitStack.append(InputLabelUnit(1, "Value 1", parent=self))

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

        self.scene.addNode(self)
        self.scene.addItem(self)

    def setPosition(self, x, y):
        self.tx = x
        self.ty = y
        self.setPos(self.tx, self.ty)
    
    def getPosition(self):
        return(self.tx, self.ty)

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QColor, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF

# Wire class

# Socket class? Or do we just have the Unit class display the socket?

# Unit classes (all Unit classes can have their socket turned on or off)

class OutputUnit(QGraphicsItem):
    def __init__(self, width, unitSize, node=None, parent=None):
        super().__init__(parent)

        self.socketSize = 8
        self.width = width
        self.height = unitSize
        self.unitBrush = QBrush(QColor("#333333"))
        self.socketBrush = QBrush(QColor("#ffaa00"))
        self.socketOutlinePen = QPen(QColor("#111111"))

        print(self.width, self.height)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()
    
    # def paintUnit(self, painter):
    #     unitPath = QPainterPath()
    #     unitPath.setFillRule(Qt.WindingFill)
    #     unitPath.addRect(1, self.height, self.width, self.height)
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(self.unitBrush)
    #     painter.drawPath(unitPath.simplified())
    
    def paintSocket(self, painter):
        painter.setPen(self.socketOutlinePen)
        painter.setBrush(self.socketBrush)
        painter.drawEllipse(int(self.width - (self.socketSize // 2)), int((self.height * 1.5) - (self.socketSize // 2)), self.socketSize, self.socketSize)
        
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintSocket(painter)

#   Input Label Unit class

#   Input Scalar Unit class

#   Input Vector Unit class

#   Input Text Unit class

class BaseNode(QGraphicsItem):
    def __init__(self, scene, title="New Node", inputs=[], outputs=[], parent=None):
        super().__init__(parent)
        self.scene = scene
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.tx = 0
        self.ty = 0
        self.radius = 8
        self.unitSize = 24
        self.unitCount = 1
        self.width = 200
        self.height = (self.unitSize * 1.5) + (self.unitSize * self.unitCount)
        self.padding = 8
        self.titleColor = QColor("#dddddd")
        self.titleBrush = QBrush(QColor("#444444"))
        self.backgroundBrush = QBrush(QColor("#222222"))
        self.titleElement = QGraphicsTextItem(self)
        self.outlinePenUnselected = QPen(QColor("#111111"))
        self.outlinePenSelected = QPen(QColor("#cccccc"))
        self.unitStack = []

        testOutput = OutputUnit(self.width, self.unitSize, parent=self)
        self.unitStack.append(testOutput)

        print(self.unitStack[0].pos().x())

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
        self.titleElement.setTextWidth(self.width - 2 * self.padding)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.scene.addNode(self)
        self.scene.addItem(self)
        # self.scene.addItem(self.unitStack[0])

    def setPosition(self, x, y):
        self.tx = x
        self.ty = y
        self.setPos(self.tx, self.ty)
    
    def getPosition(self):
        return(self.tx, self.ty)

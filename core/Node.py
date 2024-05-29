from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QColor, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF

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
        self.unitBrush = QBrush(QColor("#333333"))
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
        # bottomPath.addRect(0, unitStackOffset, self.radius, self.radius)
        # bottomPath.addRect(self.width - self.radius, unitStackOffset, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawPath(bottomPath.simplified())

    def paintOutline(self, painter):
        outlinePath = QPainterPath()
        outlinePath.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(self.outlinePenUnselected if not self.isSelected() else self.outlinePenSelected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outlinePath.simplified())

    def paintUnit(self, painter):
        unitPath = QPainterPath()
        unitPath.setFillRule(Qt.WindingFill)
        unitPath.addRect(0, self.unitSize, self.width, self.unitSize)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.unitBrush)
        painter.drawPath(unitPath.simplified())

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.paintBottom(painter)
        self.paintTitle(painter)
        self.paintUnit(painter)
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

    def setPosition(self, x, y):
        self.tx = x
        self.ty = y
        self.setPos(self.tx, self.ty)
    
    def getPosition(self):
        return(self.tx, self.ty)
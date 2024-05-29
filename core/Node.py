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
        self.width = 200
        self.height = 300
        self.radius = 8
        self.titleHeight = 24
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

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        titlePath = QPainterPath()
        titlePath.setFillRule(Qt.WindingFill)
        titlePath.addRoundedRect(0, 0, self.width, self.titleHeight, self.radius, self.radius)
        titlePath.addRect(0, self.titleHeight - self.radius, self.radius, self.radius)
        titlePath.addRect(self.width - self.radius, self.titleHeight - self.radius, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.titleBrush)
        painter.drawPath(titlePath.simplified())

        # node background
        contentPath = QPainterPath()
        contentPath.setFillRule(Qt.WindingFill)
        contentPath.addRoundedRect(0, self.titleHeight, self.width, self.height - self.titleHeight, self.radius, self.radius)
        contentPath.addRect(0, self.titleHeight, self.radius, self.radius)
        contentPath.addRect(self.width - self.radius, self.titleHeight, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawPath(contentPath.simplified())

        # outline
        outlinePath = QPainterPath()
        outlinePath.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(self.outlinePenUnselected if not self.isSelected() else self.outlinePenSelected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outlinePath.simplified())
        
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
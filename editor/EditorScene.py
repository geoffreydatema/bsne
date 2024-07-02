import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QLine

class EditorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init()

    def init(self):
        # self.nodes = []
        self.sceneWidth = 8192
        self.sceneHeight = 8192
        self.setSceneRect(-self.sceneWidth // 2, -self.sceneHeight // 2, self.sceneWidth, self.sceneHeight)

        self.gridSize = 16
        self.lightGrey = QColor("#333333")
        self.darkGrey = QColor("#222222")
        
        self.penDark = QPen(self.darkGrey)
        self.penDark.setWidth(1)

        self.setBackgroundBrush(self.lightGrey)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        leftBound = int(math.floor(rect.left()))
        rightBound = int(math.ceil(rect.right()))
        topBound = int(math.floor(rect.top()))
        bottomBound = int(math.ceil(rect.bottom()))
    
        firstLeftLine = leftBound - (leftBound % self.gridSize)
        firstTopLine = topBound - (topBound % self.gridSize)

        gridLines = []
        for x in range(firstLeftLine, rightBound, self.gridSize):
            gridLines.append(QLine(x, topBound, x, bottomBound))

        for y in range(firstTopLine, bottomBound, self.gridSize):
            gridLines.append(QLine(leftBound, y, rightBound, y))

        painter.setPen(self.penDark)
        painter.drawLines(*gridLines)

    # def addNode(self, node):
    #     self.nodes.append(node)
        
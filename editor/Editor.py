from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QFile
from editor.EditorEngine import EditorEngine
from core.Node import BaseNode, Wire
from utils.nodeutils import *

class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf=8"))
    
    def init(self):
        self.loadStylesheet("data/EditorStylesheet.qss")
        self.setWindowTitle("BSNE Editor")
        self.setGeometry(0, 0, 1280, 720)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.editorEngine = EditorEngine()
        self.layout.addWidget(self.editorEngine)

        # test nodes and wires
        firstNode = BaseNode(self.editorEngine.editorScene, "First Node", inputs=["label"], outputs=["scalar"])
        firstNode.setPosition(-300, 0)
        secondNode = BaseNode(self.editorEngine.editorScene, "Second Node", inputs=["label", "label", "label"], outputs=["scalar"])
        secondNode.setPosition(0, 0)
        thirdNode = BaseNode(self.editorEngine.editorScene, "Third Node", inputs=["label", "label"], outputs=["scalar"])
        thirdNode.setPosition(-300, 200)
        fourthNode = BaseNode(self.editorEngine.editorScene, "Fourth Node", inputs=["label", "label", "label", "label"], outputs=["scalar", "scalar"])
        fourthNode.setPosition(-50, 300)

        # firstWire = Wire(self.editorEngine.editorScene, miniguid(), firstNode.unitStack[0], secondNode.unitStack[1])

        self.show()

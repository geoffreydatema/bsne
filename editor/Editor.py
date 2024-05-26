from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QFile

class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf=8"))
    
    def init(self):
        self.loadStylesheet("data/EditorStylesheet.qss")
        self.setWindowTitle("BSNE Editor")
        self.setGeometry(0, 0, 1280, 720)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # add QGraphicsScene

        # add QGraphicsView

        self.show()

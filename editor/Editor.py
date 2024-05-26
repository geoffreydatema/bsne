from PyQt5.QtWidgets import QWidget

class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def init(self):
        self.show()
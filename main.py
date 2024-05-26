import sys
from PyQt5.QtWidgets import QApplication
from editor.Editor import Editor

def main():
    app = QApplication(sys.argv + ["-platform", "windows:darkmode=1"])
    editor = Editor()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
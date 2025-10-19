import sys, os
from ui import NoteMood
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    path = sys.argv[1] if len(sys.argv) > 1 else None
    window = NoteMood(path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

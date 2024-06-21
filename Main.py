import sys
from PyQt6.QtWidgets import QApplication
from Window1 import Window1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1 = Window1()
    window1.show()
    sys.exit(app.exec())
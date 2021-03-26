import sys
from contextlib import contextmanager
from copy import copy

from PyQt5.QtWidgets import QApplication

from ui.windows import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Image processing")

    window = MainWindow()
    window.show()

    app.exec()

from contextlib import contextmanager
from copy import copy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from app.processing import imaging, thresholding, filtering
from . import ui


class MainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.actionChoose.triggered.connect(self.loadImage)
        self.actionRefresh.triggered.connect(self.refreshImage)

        self.pushButtonBinarize.pressed.connect(self.thresholdImage)
        self.pushButtonFilter.pressed.connect(self.filterImage)

        for e in thresholding.Threshold:
            self.comboBoxBinarization.addItem(e.value[0])

        for e in filtering.Filter:
            s = e.value[0]
            self.comboBoxFiltering.addItem(e.value[0])

        self.setAttribute(Qt.WA_AlwaysShowToolTips)

        self.main_image = None
        self.modified_image = None

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        current_file, _ = QFileDialog().getOpenFileName(self, "Choose an image", ".", options=options)

        if current_file:
            self.main_image = imaging.OpenCVImageWrapper(current_file)
            self.refreshImage()

    def refreshImage(self):
        self.modified_image = copy(self.main_image)
        self.drawCurrent()

    def drawCurrent(self):
        if self.modified_image is not None:
            pixmap = QPixmap.fromImage(self.modified_image.get_image())

            w, h = self.graphicsView.width() - 5, self.graphicsView.height() - 5
            scene = QGraphicsScene(self)
            scene.addPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))

            self.graphicsView.setScene(scene)

    def resizeEvent(self, event) -> None:
        self.drawCurrent()

    @contextmanager
    def _safe(self, exc_type, message):
        try:
            yield None
        except exc_type:
            QMessageBox.warning(self, "Warning", message)

    def filterImage(self):
        with self._safe(Exception, "Cannot filter image"):
            t = filtering.Filter.from_value(self.comboBoxFiltering.currentText())

            self.modified_image.filtering(ttype=t)
            self.drawCurrent()

    def thresholdImage(self):
        with self._safe(Exception, "Cannot threshold image"):
            t = thresholding.Threshold[self.comboBoxBinarization.currentText().upper()]
            block = self.horizontalSlider.value() * 2 + 1

            self.modified_image.thresholding(ttype=t, block=block)
            self.drawCurrent()

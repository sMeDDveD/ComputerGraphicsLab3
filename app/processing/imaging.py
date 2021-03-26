import functools

import cv2
import numpy as np
from PyQt5.QtGui import QImage

from . import filtering
from . import thresholding


def modifies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.modified = True
        return func(self, *args, **kwargs)

    return wrapper


class OpenCVImageWrapper:
    def __init__(self, image: np.ndarray):

        if isinstance(image, str):
            self.cv_image = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
        else:
            self.cv_image = image
        self.modified = True

        self.q_image = self.get_image()

    def __copy__(self):
        return OpenCVImageWrapper(self.cv_image.copy())

    def get_image(self) -> QImage:

        if self.modified:
            rgb_image = self.cv_image
            if self.cv_image.ndim < 3:
                rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_GRAY2RGB)

            height, width, channel = rgb_image.shape
            bytes_count = 3 * width
            self.q_image = QImage(rgb_image.data, width, height, bytes_count, QImage.Format_RGB888)

        self.modified = False
        return self.q_image

    @modifies
    def thresholding(self, ttype: thresholding.Threshold, block=13) -> None:
        self.cv_image = thresholding.threshold(self.cv_image, block_size=block, ttype=ttype)

    @modifies
    def filtering(self, ttype: filtering.Filter) -> None:
        self.cv_image = filtering.filter_(self.cv_image, ttype=ttype)

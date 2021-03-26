import enum

import cv2
import numpy as np
import pythreshold.local_th as local


class Threshold(enum.Enum):
    ADAPTIVE = "Adaptive",
    BERNSEN = "Bernsen",
    NIBLACK = "Niblack",


BLACK = 255
WHITE = 0


def mask(image: np.ndarray, thresh: np.ndarray) -> np.ndarray:
    hold = BLACK * (image > thresh)

    return hold.astype(np.uint8)


def threshold(image: np.ndarray, block_size: int, ttype: Threshold) -> np.ndarray:
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    if ttype == Threshold.ADAPTIVE:
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 5)
    elif ttype == Threshold.NIBLACK:
        return mask(gray, local.niblack_threshold(gray, block_size))
    elif ttype == Threshold.BERNSEN:
        return mask(gray, local.bernsen_threshold(gray, block_size))

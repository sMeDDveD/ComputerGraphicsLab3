import enum

import cv2
import numpy as np

LAPLASSIAN = np.array(
    [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1],
    ]
)

LOG = np.array(
    [
        [0, 0, -1, 0, 0],
        [0, -1, -2, -1, 0],
        [-1, -2, 16, -2, -1],
        [0, -1, -2, -1, 0],
        [0, 0, -1, 0, 0]
    ]
)


class Filter(enum.Enum):
    LOG = "Laplassian of Gauss",
    LAPLASSIAN = "Laplassian",

    @classmethod
    def from_value(cls, s: str) -> "Filter":
        for e in Filter:
            if e.value[0] == s:
                return e
        raise IndexError("Invalid value")


def filter_(image: np.ndarray, ttype: Filter) -> np.ndarray:
    if ttype == Filter.LOG:
        f = LOG
    else:
        f = LAPLASSIAN

    return cv2.filter2D(image, -1, f)

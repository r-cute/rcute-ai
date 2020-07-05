"""
rcute_ai 是对一些图像/语音识别 Python 库的简单封装，使用简单，用来辅助 R-Cute 机器人（如 |Cozmars| ）进行图像/语音识别等一些高级功能

.. |Cozmars| raw:: html

   <a href="https://rcute-cozmars.readthedocs.io" target='blank'>Cozmars</a>

"""


from .face_recognizer import FaceRecognizer
from .object_recognizer import ObjectRecognizer
from .qrcode_recognizer import QRCodeRecognizer
from .hotword_recognizer_snowboy import HotwordRecognizer
from .speech_recognizer import SpeechRecognizer

from .version import __version__

from . import util
if not util.BUILDING_RTD:
    import cv2

def imshow(win, img, wait=1):
    """显示图像

    .. code:: python

        rcute_ai.imshow('win_name', img)

    等同于：

    .. code:: python

        cv2.imshow('win_name', img)
        cv2.waitKey(1)


    :param win: 图像窗口的名字
    :type win: str
    :param img: 要显示的图像
    :type img: numpy.ndarray
    :param wait: `cv2.waitKey()`的参数，默认是 `1`
    :type wait: int
    """
    cv2.imshow(win, img)
    cv2.waitKey(wait)

def imclose(win=None):
    '''关闭图像窗口

    :param win: 要关闭的图像窗口的名字，默认是 `None`，表示关闭所有图形窗口
    :type win: str
    '''
    cv2.destroyWindow(win) if win else cv2.destroyAllWindows()


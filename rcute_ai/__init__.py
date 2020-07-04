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
"""
rcute-ai consists of simple wrapper classes over some python libs for image/audio detection/recognition etc to facilitate R-Cute robots.

.. note::

    On Windows, before you :data:`pip install rcute-ai`, make sure you're using Python *64 bit* interpreter of version 3.7 or 3.8, to show info of your interpreter, run

    .. code::

        import sys
        print(sys.version)
        print(len("{0:b}".format(sys.maxsize))+1, 'bit')

    You also need to manually download and install dlib module pre-built for Windows, `dlib-19.21.0-cp37-cp37m-win_amd64.whl <https://cdn.jsdelivr.net/gh/vivekmathema/Dlib19.2.1_windows/dlib-19.21.0-cp37-cp37m-win_amd64.whl>`_ or `dlib-19.19.0-cp38-cp38-win_amd64.whl <https://cdn.jsdelivr.net/gh/pratyusa98/face-recognition_dlib_library/face-recognition_dlib_library/dlib-19.19.0-cp38-cp38-win_amd64.whl>`_ according to your Python version

"""


from .face_recognizer import FaceRecognizer
from .object_recognizer import ObjectRecognizer
from .qrcode_recognizer import QRCodeRecognizer
from .wake_word_detector_vosk import WakeWordDetector
from .stt_vosk import STT
import platform
if platform.system()=='Linux':
    from .tts_espeak import TTS
else:
    from .tts_pyttsx3 import TTS

from .version import __version__

from .util import imshow, imclose
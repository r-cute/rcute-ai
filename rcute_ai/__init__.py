"""
rcute-ai consists of simple wrapper classes over some python libs for image/audio detection/recognition etc to facilitate R-Cute robots.

.. note::

    On Windows, You need Python *64 bit* interpreter, to find out the bit-ness of your interpreter, run

    .. code::

        import sys
        print(len("{0:b}".format(sys.maxsize))+1)

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
"""
rcute-ai consists of simple wrapper classes over some python libs for image/audio detection/recognition etc to facilitate R-Cute robots.

You need Python *64bit* interpreter, because speech recognition functions does not run on Python 32bit interperter. To find out:

.. code::

    import sys
    print(len("{0:b}".format(sys.maxsize))+1)

"""


from .face_recognizer import FaceRecognizer
from .object_recognizer import ObjectRecognizer
from .qrcode_recognizer import QRCodeRecognizer
from .wake_word_detector_vosk import WakeWordDetector
from .speech_recognizer import SpeechRecognizer
from .tts import TTS

from .version import __version__

from .util import imshow, imclose
"""
rcute-ai simply wrappers some python libs for image/audio detection/recognition etc to provide consistent API.

"""


from .face_detection import FaceDetector
from .object_detection import ObjectDetector
from .qrcode_detection import QRCodeDetector
from .aruco import ArUcoDetector
from .wake_word_detection_vosk import WakeWordDetector
from .stt_vosk import STT
from .hand_detection import HandDetector, HandLandmark
from .pose_detection import PoseDetector, PoseLandmark
from .ocr_tesseract import OCR

import platform
if platform.system()=='Linux':
    from .tts_espeak import TTS
else:
    from .tts_pyttsx3 import TTS

from .version import __version__

from .util import imshow, imclose, set_data_path
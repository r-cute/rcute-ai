from . import util
import json
from vosk import Model, KaldiRecognizer

class WakeWordDetector:
    """唤醒词检测器，对 `vosk-api <https://github.com/alphacep/vosk-api>`_ 的简单封装，默认的唤醒词是 `'阿Q'` 和 `'R-Cute'`。

    如果要自定义唤醒词，请参考 https://github.com/alphacep/vosk-api/blob/master/python/example/test_words.py
    """

    def __init__(self, sr=16000, lang='en', grammar='[ "a b c d e f g h i j k l m n o p q r s t u v w x y z key cute", "[unk]" ]'):
        model = Model(util.data_file("vosk/"+ lang))
        self._det = KaldiRecognizer(model, sr, grammar)

    def _detected(self, text):
        if text == 'r q':
            return '阿Q'
        elif text == 'r cute':
            return 'R-Cute'

    def detect(self, source, timeout=None):
        """开始检测

        :param source: 声音来源
        :param timeout: 超时，即检测的最长时间（秒），默认为 `None` ，表示不设置超时，知道检测到唤醒词才返回
        :type timeout: float, optional
        :return: 检测到的唤醒词模型对应的唤醒词，若超时没检测到唤醒词则返回 `None`
        :rtype: str
        """
        self._cancel = False
        if timeout:
            count = 0.0
        self._det.FinalResult() # clear buffer
        while True:
            segment = source.read()
            if self._det.AcceptWaveform(segment.raw_data):
                p= self._detected(json.loads(self._det.Result())['text'])
            else:
                p= self._detected(json.loads(self._det.PartialResult())['partial'])
            if p:
                return p
            if self._cancel:
                raise RuntimeError('Hotword detection cancelled by another thread')
            elif timeout:
                count += segment.duration_seconds
                if count > timeout:
                    return# self._detected(self._det.FinalResult()['text'])

    def cancel(self):
        """停止检测"""
        self._cancel = True


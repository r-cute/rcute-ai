from . import util
import json
if not util.BUILDING_RTD:
    from vosk import Model, KaldiRecognizer

class WakeWordDetector:
    """唤醒词检测器，对 `vosk-api <https://github.com/alphacep/vosk-api>`_ 的简单封装，默认的唤醒词是 `'阿Q'` 和 `'R-cute`。

    如果要自定义唤醒词，请参考 https://github.com/alphacep/vosk-api/blob/master/python/example/test_words.py
    """

    def __init__(self, sr=16000, model_file=None, grammar=None):
        model = Model(model_file or util.resource("sphinx/vosk-model-en-us-daanzu-20200328-lgraph"))
        self._det = KaldiRecognizer(model, sr, grammar or '[ "a b c d e f g h i j k l m n o p q r s t u v w x y z key cute", "[unk]" ]')

    def _process_result(self, text):
        if text == 'r q':
            return '阿Q'
        elif text == 'r cute':
            return 'R-Cute'

    def detect(self, source, timeout=None):
        """开始识别

        :param source: 声音来源
        :param timeout: 超时，即识别的最长时间（秒），默认为 `None` ，表示不设置超时，知道识别到唤醒词才返回
        :type timeout: float, optional
        :return: 识别到的唤醒词模型对应的唤醒词，若超时没识别到唤醒词则返回 `None`
        :rtype: str
        """
        self._cancel = False
        if timeout:
            count = 0.0
        self._rec.FinalResult() # clear buffer
        while True:
            segment = source.read()
            if self._rec.AcceptWaveform(segment.raw_data):
                p= self._process_result(json.loads(self._rec.Result())['text'])
            else:
                p= self._process_result(json.loads(self._rec.PartialResult())['partial'])
            if p:
                return p
            if self._cancel:
                raise RuntimeError('Hotword detection cancelled by another thread')
            elif timeout:
                count += segment.duration_seconds
                if count > timeout:
                    return# self._process_result(self._rec.FinalResult()['text'])

    def cancel(self):
        """停止识别"""
        self._cancel = True


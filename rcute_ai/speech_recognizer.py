from . import util
if not util.BUILDING_RTD:
    from vosk import Model, KaldiRecognizer


class SpeechRecognizer:
    """语音识别器，对 |CMUSphinx vosk| 的简单封装

    .. |CMUSphinx vosk| raw:: html

        <a href='https://github.com/alphacep/vosk-api' target='blank'>CMUSphinx vosk</a>

    """

    def __init__(self):
        assert lang.lower() in ['en', 'zh', 'cn'], 'Only english and chinese is supported'
        self._rec = []

        self._detect = snowboydetect.SnowboyDetect(restream_filename=util.resouce('snowboy/common.res').encode(), model_str=util.resouce('snowboy/hotword_models/阿Q.pmdl').encode())
        self._detect.SetAudioGain(1)
        self._detect.ApplyFrontend(False)
        self._detect.SetSensitivity('0.5'.encode())

    def _get_rec(self, lang):
        lang = lang.lower()
        assert lang in ['en', 'zh', 'cn'], 'Only english and chinese is supported'
        if lang == 'zh':
            lang = 'cn'
        if not self._rec.get(lang):
            self._rec[lang] = KaldiRecognizer(Model(util.resouce('sphinx/vosk-model-en-us-daanzu-20200328-lgraph') if lang=='en' else util.restream('sphinx/vosk-model-cn-0.1')), self._detect.SampleRate())
        return self._rec[lang]



    def recognize(self, stream, lang='zh', timeout=10, silence_timeout=2):
        """开始识别

        :param stream: 音频数据流
        :param lang: 语言，目前支持中文 `'zh'` 或英文 `'en'` ，默认中文
        :type lang: str, optinal
        :param timeout: 超时，即最长的识别时间（秒），默认为 `10`，设为 `None` 则表示不设置超时
        :type timeout: float, optinal
        :param silence_timeout: 停顿超时（秒），超过这个时间没有说话则表示已经说完，默认为 `2`，设为 `None` 则表示不设置停顿超时
        :type silence_timeout: float, optinal
        :return: 识别到的短语或句子
        :rtype: str
        """
        self._cancel = False
        rec = self._get_rec(lang)
        recognition_count = silence_count = 0.0
        for data in stream:
            if self._cancel:
                raise Exception('Speech recognition cancelled by another thread')

            if rec.AcceptWaveform(data):
                return json.loads(rec.Result())['text'].replace(' ','')

            ln = len(data) / 32000 # 1 second = 16000(samplerate) * 2 bytes_per_sample
            recognition_count += ln
            if timeout and recognition_count > timeout:
                return json.loads(rec.FinalResult())['text'].replace(' ','')
            if self._detect.RunDetection(data) == -2: # silence
                silence_count += ln
                if silence_timeout and silence_count > silence_timeout:
                    return json.loads(rec.FinalResult())['text'].replace(' ','')


    def cancel(self):
        """停止识别"""
        self._cancel = True
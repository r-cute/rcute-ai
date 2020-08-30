from . import util
if not util.BUILDING_RTD:
    import json
    from vosk import Model, KaldiRecognizer
    from pydub import AudioSegment
    # import snowboydetect


class SpeechRecognizer:
    """语音识别器，对 |CMUSphinx vosk| 的简单封装

    .. |CMUSphinx vosk| raw:: html

        <a href='https://github.com/alphacep/vosk-api' target='blank'>CMUSphinx vosk</a>

    :param lang: 语言，目前支持中文 `'zh'` 或英文 `'en'` ，默认中文
    :type lang: str, optinal
    """

    def __init__(self, lang='zh'):
        lang = lang.lower()
        self._lang = lang
        assert lang in ['en', 'zh', 'cn'], 'Currently only english and chinese are supported'
        self._rec = KaldiRecognizer(Model(util.resource('sphinx/vosk-model-en-us-daanzu-20200328-lgraph') if lang=='en' else util.resource('sphinx/vosk-model-cn-0.1')), 16000)
        # self._detect = snowboydetect.SnowboyDetect(resource_filename=util.resource('snowboy/common.res').encode(),model_str=util.resource('snowboy/hotword_models/阿Q.pmdl').encode())
        # self._detect.SetAudioGain(2)
        # self._detect.ApplyFrontend(False)
        # self._detect.SetSensitivity('0.5'.encode())


    def recognize(self, source, timeout=10, silence_timeout=2, silence_rms_threshold=500):
        """开始识别

        :param source: 声音来源
        :param timeout: 超时，即最长的识别时间（秒），默认为 `10`，设为 `None` 则表示不设置超时
        :type timeout: float, optinal
        :param silence_timeout: 停顿超时（秒），超过这个时间没有说话则表示已经说完，默认为 `2`，设为 `None` 则表示不设置停顿超时
        :type silence_timeout: float, optinal
        :param silence_rms_threshold: 停顿音量的阈值，当音量小于这个阈值则认为没有说话，默认为 `500`。见 |pydub.AudioSegment(…).rms|
        :type silence_rms_threshold: int, optinal
        :return: 识别到的短语或句子
        :rtype: str

        .. |pydub.AudioSegment(…).rms| raw:: html

            <a href='https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentrms' target='blank'>pydub.AudioSegment(…).rms</a>

        """
        self._cancel = False
        recognition_count = silence_count = 0.0
        while True:
            data = source.raw_read()
            if self._cancel:
                raise Exception('Speech recognition cancelled by another thread')

            if self._rec.AcceptWaveform(data):
                text = self._rec.Result()
                break

            # ln = len(data) / 32000 # 1 second = 16000(samplerate) * 2 bytes_per_sample
            recognition_count += source.frame_duration
            if timeout and recognition_count > timeout:
                text = self._rec.FinalResult()
                break
            # voice activity detection:
            # if self._detect.RunDetection(data) == -2: # silence
            if silence_timeout:
                if AudioSegment(data=data, sample_width=source.sample_width, frame_rate=source.sample_rate, channels=source.channels).rms < silence_rms_threshold:
                    silence_count += source.frame_duration
                    if silence_count > silence_timeout:
                        text = self._rec.FinalResult()
                        break
                else:
                    silence_count = 0

        text = json.loads(text)['text']
        if not self._lang == 'en':
            text = text.replace(' ','')
        return text


    def cancel(self):
        """停止识别"""
        self._cancel = True


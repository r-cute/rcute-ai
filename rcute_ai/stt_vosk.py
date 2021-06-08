from . import util
from os import listdir, path
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

class STT:
    """语音识别类，对 |CMUSphinx vosk| 的简单封装

    .. |CMUSphinx vosk| raw:: html

        <a href='https://github.com/alphacep/vosk-api' target='blank'>CMUSphinx vosk</a>

    :param lang: 语言缩写，默认为英文 `'en'`。这个参数和 `rcute-ai 依赖的资源文件 <../installation.html#data-file>`_ 的语音识别 vosk 文件夹里的文件名对应
    :type lang: str, optinal
    """

    def __init__(self, lang='en'):
        self._lang = lang
        self._rec = KaldiRecognizer(self.load(util.vosk_map[lang]), 16000)

    @property
    def lang(self):
        """语言"""
        return self._lang

    @lang.setter
    def lang(self, lang):
        if self._lang != lang:
            self._lang = lang
            self._rec = KaldiRecognizer(self.load(util.vosk_map[lang]), 16000)

    @classmethod
    def get_lang_list(cl):
        """列出支持的所有语言

        如何支持添加你需要的语言？参考 `下载 rcute-ai 依赖的资源文件 -> 语音识别 <../installation.html#data-file>`_"""
        return list(util.vosk_map)

    def load(self, lang_file=None):
        """load language models in advance"""
        if isinstance(lang_file, list):
            for l in lang_file:
                self.load(l)
        else:
            model = util.cache.get(f'vosk.{lang_file}', Model(util.data_file(f'vosk/{lang_file}')))
            util.cache[f'vosk.{lang_file}'] = model
            return model

    def stt(self, source, timeout=None, silence_timeout=2, silence_threshold=-35):
        """speech to text

        :param source: 声音来源
        :param timeout: 超时，即最长的识别时间（秒），默认为 `None` 则表示不设置超时
        :type timeout: float, optinal
        :param silence_timeout: 停顿超时（秒），开始说话后超过这个时间的停顿表示已经说完，默认为2秒， `None` 则表示不设置停顿超时
        :type silence_timeout: float, optinal
        :param silence_threshold: 停顿音量的阈值，当音量小于这个阈值则认为没有说话，默认为 `-35` (dBFS)。见 |pydub.AudioSegment(…).dBFS|
        :type silence_rms_threshold: int, optinal
        :return: 识别到的短语或句子
        :rtype: str

        .. |pydub.AudioSegment(…).dBFS| raw:: html

            <a href='https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentdbfs' target='blank'>pydub.AudioSegment(…).dBFS</a>

        """
        self._cancel = False
        recognition_count = silence_count = 0.0
        started = False
        while True:
            segment = source.read()
            if self._cancel:
                raise Exception('Speech recognition cancelled by another thread')

            if self._rec.AcceptWaveform(segment.raw_data):
                text = self._rec.FinalResult()
                break

            if not started and json.loads(self._rec.PartialResult())['partial']:
                started = True

            seg_duration = segment.duration_seconds
            recognition_count += seg_duration
            if timeout and recognition_count > timeout:
                text = self._rec.FinalResult()
                break
            # voice activity detection:
            if silence_timeout and started:
                if segment.dBFS < silence_threshold:
                    silence_count += seg_duration
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


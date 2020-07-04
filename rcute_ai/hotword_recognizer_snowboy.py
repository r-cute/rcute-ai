from . import util

if not util.BUILDING_RTD:
    import sys
    sys.path.append(util.resource('snowboy'))
    import snowboydetect

logger = util.logger

class HotwordRecognizer:
    """热词（唤醒词）识别器，对 |snowboy| 的简单封装

    .. |snowboy| raw:: html

        <a href='https://github.com/Kitt-AI/snowboy' target='blank'>snowboy</a>

    :param hotword_model: 热词模型的文件路径或路径列表，默认为 `None`
    :type hotword_model: str / list
    :param hotword: 热词或热词列表，默认为 `None` ，数量与顺序应该与热词模型对应，当某个热词模型被识别到时， :func:`recognize` 会返回对应的热词

        如果不设置热词，识别到的热词为热词模型文件的文件名

        如果热词模型和热词都不设置，则默认的热词为“阿Q”或“R Cute”
    :type hotword: str / list
    :param sensitivity: 灵明度或灵明度列表，0~1，数量与顺序应该与热词模型对应，默认为 `0.5`
    :type sensitivity: float / list, optional
    :param audio_gain: 声音增益，0~2，默认为 `1`
    :type audio_gain: float, optinal
    """


    def __init__(self, *,
                        hotword_model=None,
                        hotword=None,
                        sensitivity=.5,
                        audio_gain=1):

        if not hotword_model:
            hotword_model = [util.resource(f'snowboy/hotword_models/{a}') for a in ['阿Q.pmdl']]
        if not isinstance(hotword_model, list):
            hotword_model = [hotword_model]
        if isinstance(sensitivity, list):
            assert len(hotword_model) == len(sensitivity), 'Number of hotword_model does not match number of sensitivity'
        else:
            sensitivity = [sensitivity]* len(hotword_model)
        if hotword is not None:
            if not isinstance(hotword, list):
                hotword = [hotword]
            assert len(hotword) == len(hotword_model), 'Number of hotword_model does not match number of hotword'
        self._hotwords = [w.split('/')[-1].split('.')[0] for w in hotword_model] if hotword is None else hotword
        self._detect = snowboydetect.SnowboyDetect(restream_filename=util.resouce('snowboy/common.res').encode(), model_str=",".join(hotword_model).encode())
        self._detect.SetAudioGain(audio_gain)
        self._detect.ApplyFrontend(False)
        self._detect.SetSensitivity(','.join([str(s) for s in sensitivity]).encode())

    def recognize(self, stream, timeout=None):
        """开始识别

        :param stream: 音频数据流
        :param timeout: 超时，即识别的最长时间（秒），默认为 `None` ，表示不设置超时，知道识别到热词才返回
        :type timeout: float, optional
        :return: 识别到的热词模型对应的热词，若超时没识别到热词则返回 `None`
        :rtype: str
        """
        self._cancel = False
        if timeout:
            count = 0.0
        for data in stream:
            if self._cancel:
                raise Exception('Hotword detection cancelled by another thread')
            status = self._detect.RunDetection(data)
            if status == -1:
                logger.warning("Error initializing streams or reading audio data")
            elif status > 0:
                return self.hotwords[status-1]
            elif timeout:
                count += len(data) / 32000
                if count > timeout:
                    return


    def cancel(self):
        """停止识别"""
        self._cancel = True

    @property
    def hotword_list(self):
        """自带的热词列表，只读"""
        return util.hotword_list_snowboy()

    @property
    def hotword_model_list(self):
        """自带的热词模型文件的列表，只读"""
        return util.hotword_model_list_snowboy()



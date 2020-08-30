from . import util
if not util.BUILDING_RTD:
    from pocketsphinx import Pocketsphinx, get_model_path
    import os

class HotwordRecognizer:
    """热词（唤醒词）识别器，对 |pocketsphinx| 的简单封装，默认的热词是 `'阿Q'` 和 `'R-cute`。

    如果要自定义热词，请参考 https://blog.51cto.com/feature09/2300352

    .. |pocketsphinx| raw:: html

        <a href='https://github.com/bambocher/pocketsphinx-python' target='blank'>pocketsphinx</a>

    .. |config| raw:: html

        <a href='https://github.com/bambocher/pocketsphinx-python#default-config' target='blank'>pocketsphinx Default config</a>

    :param hotword: 热词或热词列表，默认为 `['阿Q', 'R-cute']`
    :type hotword: str / list, optional
    :param hmm: 参考 |config|
    :type hmm: str, optional
    :param lm: 参考 |config|
    :type lm: str, optional
    :param dic: 参考 |config|
    :type dic: str, optional
    """

    def __init__(self, **kwargs):
        # signal.signal(signal.SIGINT, self.stop)
        self._no_search = False
        self._full_utt = False
        hotword = kwargs.pop('hotword', ['阿Q', 'R-cute'])
        self._hotwords = hotword if isinstance(hotword, list) else [hotword]

        model_path = get_model_path()
        opt = {
            'verbose': False,
            'hmm': os.path.join(model_path, 'en-us'),
            'lm': util.resource('sphinx/rcute.lm'),
            'dic': util.resource('sphinx/rcute.dic'),
            }
        opt.update(kwargs)
        self._rec = Pocketsphinx(**opt)

    def recognize(self, stream, timeout=None):
        """开始识别

        :param source: 声音来源
        :param timeout: 超时，即识别的最长时间（秒），默认为 `None` ，表示不设置超时，知道识别到热词才返回
        :type timeout: float, optional
        :return: 识别到的热词模型对应的热词，若超时没识别到热词则返回 `None`
        :rtype: str
        """
        self._cancel = False
        if timeout:
            count = 0.0
        in_speech = False
        with self._rec.start_utterance():
            while True:
                data = stream.raw_read()
                self._rec.process_raw(data, self._no_search, self._full_utt)
                if in_speech != self._rec.get_in_speech():
                    in_speech = not in_speech
                    if not in_speech and self._rec.hyp():
                        with self._rec.end_utterance():
                            hyp = self._rec.hypothesis()
                            if hyp in self._hotwords:
                                return hyp
                if self._cancel:
                    raise RuntimeError('Hotword detection cancelled by another thread')
                elif timeout:
                    count += source.frame_duration #len(data) / 32000
                    if count > timeout:
                        return

    def cancel(self):
        """停止识别"""
        self._cancel = True


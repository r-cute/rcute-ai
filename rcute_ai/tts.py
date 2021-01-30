import re
from espeakng import ESpeakNG

class TTS:
    def __init__(self):
        self.default_options= {}
        """ voice/volume/pitch/speed etc. See `py-espeak-ng <https://github.com/gooofy/py-espeak-ng>`_
        """

    @property
    def ng(self):
        if not hasattr(self, '_esng'):
            self._esng = ESpeakNG()
        return self._esng

    def _set(self, txt, options):
        if 'lang' in options:
            options['voice'] = options.pop('lang')
        if 'voice' not in options:
            options['voice'] = lang_detect(txt)
        op = self.default_options.copy()
        op.update(options)
        for k, v in op.items():
            setattr(self.ng, k, v)

    def say(self, txt, **options):
        """text to speach

        :param txt: text to be said
        :type txt: str
        :param options: if not set, :data:`default_options` is used.
            * voice/lang: if not set, English is the default unless Chinese characters are detected in :data:`txt`
            * volume
            * pitch
            * speed
            * word_gap

            See `py-espeak-ng <https://github.com/gooofy/py-espeak-ng>`_
        :type options: optional
        """
        self._set(txt, options)
        self.ng.say(txt)

    def wav(self, txt, **options):
        """return tts wav

        :param txt: text to be said
        :type txt: str
        :param options: if not set, :data:`default_options` is used.
            * voice/lang: if not set, English is the default unless Chinese characters are detected in :data:`txt`
            * volume
            * pitch
            * speed
            * word_gap

            See `py-espeak-ng <https://github.com/gooofy/py-espeak-ng>`_
        :type options: optional
        :return: wav data
        :rtype: bytes
        """
        file = options.pop('file')
        self._set(txt, options)
        return self.ng.synth_wav(txt)
        # return self.ng.synth_wav(txt, file=file)

def lang_detect(txt):
    return 'zh' if re.findall(r'[\u4e00-\u9fff]+', txt) else 'en'
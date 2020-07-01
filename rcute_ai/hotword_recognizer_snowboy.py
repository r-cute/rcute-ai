from . import util

import sys
sys.path.append(util.resource('snowboy'))
import snowboydetect

import logging
logger = logging.getLogger(__name__)

class HotwordRecognizer:

    @classmethod
    def hotword_list(cl):
        return util.hotword_list_snowboy()

    @classmethod
    def hotword_model_list(cl):
        return util.hotword_model_list_snowboy()

    def __init__(self, hotword_model=[util.resource(f'snowboy/hotword_models/{a}') for a in ['阿Q.pmdl']],
                        *,
                        hotword=None,
                        sensitivity=.5,
                        audio_gain=1):

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

    def recognize(self, stream):
        self._cancel = False
        for data in stream:
            if self._cancel:
                raise Exception('Hotword detection cancelled by another thread')
            status = self._detect.RunDetection(data)
            if status == -1:
                logger.warning("Error initializing streams or reading audio data")
            elif status > 0:
                return self.hotwords[status-1]

    def cancel(self):
        self._cancel = True


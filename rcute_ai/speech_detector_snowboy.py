import json
from vosk import Model, KaldiRecognizer
from . import util

import sys
sys.path.append(util.restream('snowboy'))
import snowboydetect

logger = logging.getLogger(__name__)

class SpeechDetector:

    @classmethod
    def hotword_list(cl):
        return util.hotword_list_snowboy()

    @classmethod
    def hotword_model_list(cl):
        return util.hotword_model_list_snowboy()

    def __init__(self,
                    hotword_model=[util.restream(f'snowboy/hotword_models/{a}') for a in ['阿Q.pmdl']],
                    sensitivity=.5,
                    lang='zh',
                    audio_gain=1,
                    silence_timeout=2,
                    recognition_timeout=10):

        if not isinstance(hotword_model, list):
            hotword_model = [hotword_model]
        if isinstance(sensitivity, list):
            assert len(hotword_model) == len(sensitivity), 'Number of hotword does not match number of sensitivity'
        else:
            sensitivity = [sensitivity]* len(hotword_model)

        self._detect = snowboydetect.SnowboyDetect(restream_filename=util.resouce('snowboy/common.res').encode(), model_str=",".join(hotword_models).encode())
        self._detect.SetAudioGain(audio_gain)
        self._detect.ApplyFrontend(False)
        self._detect.SetSensitivity(','.join([str(s) for s in sensitivity]).encode())

        assert lang.lower() in ['en', 'zh', 'cn'], 'Only english and chinese is supported'
        self._rec = KaldiRecognizer(Model(util.resouce('sphinx/vosk-model-en-us-daanzu-20200328-lgraph') if lang=='en' else util.restream('sphinx/vosk-model-cn-0.1')), self._detect.SampleRate())

        self._hotwords = [w.split('/')[-1].split('.')[0] for w in hotword_model]
        self._recognition_timeout = int(recognition_timeout/self.required_buffer_size)
        self._silence_timeout = int(silence_timeout/self.required_buffer_size)

    @property
    def required_samplerate(self):
        return 16000

    @property
    def required_bit_depth(self):
        return 16

    @property
    def required_channels(self):
        return 1

    @property
    def required_buffer_size(self):
        return self.required_samplerate * self.required_bit_depth//8 * self.required_channels // 10 # 0.1 sec

    def stop(self):
        self._stop = True

    def detect(self, stream, *, hotword_callback=None, speech_callback=None):
        self._stop = False
        recognizing = False
        recognition_count = silence_count = 0
        for data in stream:
            if self._stop:
                return
            status = self._detect.RunDetection(data)
            if status == -1:
                logger.warning("Error initializing streams or reading audio data")
            if recognizing:
                if self._rec.AcceptWaveform(data):
                    speech_callback(json.loads(self._rec.Result())['text'].replace(' ',''))
                    recognizing = False
                else:
                    recognition_count += 1
                    if status == -2: # silence detected
                        silence_count += 1
                    else:
                        silence_count = 0
                    if recognition_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                        speech_callback(json.loads(self._rec.FinalResult())['text'].replace(' ',''))
                        recognizing = False

            elif status > 0:
                hotword_callback and hotword_callback(self._hotwords[status])
                if speech_callback:
                    recognition_count = silence_count = 0
                    recognizing = True


    def detect_once(self, stream, *, hotword_callback=None, speech_callback=None):
        self._stop = False
        recognizing = False
        recognition_count = silence_count = 0
        for data in stream:
            if self._stop:
                return
            status = self._detect.RunDetection(data)
            if status == -1:
                logger.warning("Error initializing streams or reading audio data")
            if recognizing:
                if self._rec.AcceptWaveform(data):
                    speech_callback(json.loads(self._rec.Result())['text'])
                    return
                else:
                    recognition_count += 1
                    if status == -2: # silence detected
                        silence_count += 1
                    else:
                        silence_count = 0
                    if recognition_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                        speech_callback(json.loads(self._rec.FinalResult())['text'])
                        return
            elif status > 0:
                hotword_callback and hotword_callback(self._hotwords[status])
                if speech_callback:
                    recognizing = True
                else:
                    return



import collections
import json
from vosk import Model, KaldiRecognizer
from . import util

logger = logging.getLogger(__name__)

class SpeechDetector:

    @classmethod
    def wake_word_list(cl):
        return util.wake_word_list()

    def __init__(self, source, *, wake_word_callback=None, speech_callback=None,
                    wake_word_model=[util.resource_path(a) for a in ['阿Q.pmdl']],
                    sensitivity=[.5],
                    lang='en',
                    audio_gain=1,
                    silence_timeout=2,
                    recognition_timeout=10):


        assert speech_callback or wake_word_callback, 'Neither wake_word_callback nor speech_callback is provided'
        if not isinstance(wake_word_model, list):
            wake_word_model = [wake_word_model]
        if isinstance(sensitivity, list):
            assert len(wake_word_model) == len(sensitivity), 'Number of wake_word does not match number of sensitivity'
        else:
            sensitivity = [sensitivity]* len(wake_word_model)
        self._detect = snowboydetect.SnowboyDetect(resource_filename=util.resouce_path('common.res').encode(), model_str=",".join(wake_word_model).encode())
        self._detect.SetAudioGain(audio_gain)
        self._detect.ApplyFrontend(False)
        self._detect.SetSensitivity(','.join([str(s) for s in sensitivity]).encode())
        if speech_callback:
            assert lang.lower in ['en', 'zh', 'cn'], 'Only english and chinese is supported'
            self._rec = KaldiRecognizer(Model(util.EN_LANG_MODEL if lang=='en' else util.CN_LANG_MODEL), self._detect.SampleRate())
        self._speech_callback = speech_callback
        self._wake_word_callback = wake_word_callback
        self._wake_words = [w.split('/')[-1][:-5] for w in wake_word_model]
        self._source = source
        self._recognition_timeout = int(recognition_timeout/source.frame_time)
        self._silence_timeout = int(silence_timeout/source.frame_time)

    def stop(self):
        self._stop = True

    def run(self):
        self._stop = False
        self._source.samplerate = self._detect.SampleRate()
        with self._source:
            recognizing = False
            recognize_count = silence_count = 0
            for data in self._source.raw_output_stream:
                if self._stop:
                    return
                status = self._detect.RunDetection(data)
                if status == -1:
                    logger.warning("Error initializing streams or reading audio data")
                if recognizing:
                    if self._rec.AcceptWaveform(data):
                        self._wake_word_callback(json.loads(self._rec.Result())['text'])
                        recognizing = False
                    else:
                        recognize_count += 1
                        if status == -2: # silence detected
                            silence_count += 1
                        else:
                            silence_count = 0
                        if recognize_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                            self._wake_word_callback(json.loads(self._rec.FinalResult())['text'])
                            recognizing = False
                elif status > 0:
                    self._wake_word_callback and self._wake_word_callback(self._wake_words[status])
                    if self._speech_callback:
                        recognize_count = silence_count = 0
                        recognizing = True


    def run_once(self):
        self._stop = False
        self._source.samplerate = self._detect.SampleRate()
        with self._source:
            recognizing = False
            recognize_count = silence_count = 0
            for data in self._source.raw_output_stream:
                if self._stop:
                    return
                status = self._detect.RunDetection(data)
                if status == -1:
                    logger.warning("Error initializing streams or reading audio data")
                if recognizing:
                    if self._rec.AcceptWaveform(data):
                        self._wake_word_callback(json.loads(self._rec.Result())['text'])
                        return
                    else:
                        recognize_count += 1
                        if status == -2: # silence detected
                            silence_count += 1
                        else:
                            silence_count = 0
                        if recognize_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                            self._wake_word_callback(json.loads(self._rec.FinalResult())['text'])
                            return
                elif status > 0:
                    self._wake_word_callback and self._wake_word_callback(self._wake_words[status])
                    if self._speech_callback:
                        recognizing = True
                    else:
                        return



# not tested

import struct
from pydub import AudioSegment
import pvporcupine
from vosk import Model, KaldiRecognizer
from . import util

logger = logging.getLogger(__name__)

class SpeechDetector:

    @classmethod
    def wake_word_list(cl):
        return util.wake_word_list_picovoice()

    def __init__(self, source, *, wake_word_callback=None, speech_callback=None,
                    wake_word_model=[util.resource_path(a) for a in ['r_cute.linux_2020-07-28_v1.8.0.ppn']],
                    sensitivity=[.5],
                    lang='en',
                    silence_timeout=2,
                    recognition_timeout=10,
                    silence_rms_threshold=500):


        assert speech_callback or wake_word_callback, 'Neither wake_word_callback nor speech_callback is provided'
        if not isinstance(wake_word_model, list):
            wake_word_model = [wake_word_model]
        if isinstance(sensitivity, list):
            assert len(wake_word_model) == len(sensitivity), 'Number of wake_word does not match number of sensitivity'
        else:
            sensitivity = [sensitivity]* len(wake_word_model)
        self._detect = pvporcupine.Porcupine(
                    library_path=pvporcupine.LIBRARY_PATH,
                    model_file_path=pvporcupine.MODEL_FILE_PATH,
                    keyword_file_paths=wake_word_model,
                    sensitivities=sensitivity)
        if speech_callback:
            assert lang.lower() in ['en', 'zh', 'cn'], 'Only english and chinese is supported'
            self._rec = KaldiRecognizer(Model(util.EN_LANG_MODEL if lang=='en' else util.CN_LANG_MODEL), self._detect.SampleRate())
        self._speech_callback = speech_callback
        self._wake_word_callback = wake_word_callback
        self._wake_words = [w.split('/')[-1].split('.')[0] for w in wake_word_model]
        self._source = source
        self._silence_rms_threshold = silence_rms_threshold
        self._recognition_timeout = int(recognition_timeout/source.frame_time)
        self._silence_timeout = int(silence_timeout/source.frame_time)

    def stop(self):
        self._stop = True

    def __del__(self):
        if hasattr(self, '_detect'):
            self._detect.delete()

    def run(self):
        self._stop = False
        self._source.samplerate = self._detect.sample_rate
        wanted_length = self._detect.frame_length
        with self._source:
            for data in self._source.raw_output_stream:
                data = old_data + data
                while len(data) >= wanted_length:
                    if self._stop:
                        return

                    status = self._detect.process(struct.unpack_from("h" * wanted_length, data[:wanted_length]))

                    if status==True or isinstance(status, int) and status>=0:
                        data = b''
                        self._wake_word_callback and self._wake_word_callback(self._wake_words[0 if status==True else status])
                        if self._speech_callback:

                            recognition_count = silence_count = 0
                            for d in self._source.raw_output_stream:
                                if self._stop:
                                    return

                                if self._rec.AcceptWaveform(d):
                                    self._wake_word_callback(json.loads(self._rec.Result())['text'])
                                    break
                                else:
                                    recognition_count += 1
                                    # hard coded
                                    if AudioSegment(data=d, sample_width=2, frame_rate=16000, channels=1).rms < self._silence_rms_threshold:
                                        silence_count += 1
                                    else:
                                        silence_count = 0
                                    if recognition_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                                        self._wake_word_callback(json.loads(self._rec.FinalResult())['text'])
                                        break
                    else:
                        data = data[wanted_length:]
                else:
                    old_data = data


    def run_once(self):
        self._stop = False
        self._source.samplerate = self._detect.sample_rate
        wanted_length = self._detect.frame_length
        with self._source:
            for data in self._source.raw_output_stream:
                data = old_data + data
                while len(data) >= wanted_length:
                    if self._stop:
                        return

                    status = self._detect.process(struct.unpack_from("h" * wanted_length, data[:wanted_length]))

                    if status == True or isinstance(status, int) and status >= 0:
                        data = b''
                        self._wake_word_callback and self._wake_word_callback(self._wake_words[0 if status==True else status])
                        if self._speech_callback:

                            recognition_count = silence_count = 0
                            for d in self._source.raw_output_stream:
                                if self._stop:
                                    return

                                if self._rec.AcceptWaveform(d):
                                    self._wake_word_callback(json.loads(self._rec.Result())['text'])
                                    break
                                else:
                                    recognition_count += 1
                                    # hard coded
                                    if AudioSegment(data=d, sample_width=2, frame_rate=16000, channels=1).rms < self._silence_rms_threshold:
                                        silence_count += 1
                                    else:
                                        silence_count = 0
                                    if recognition_count >= self._recognition_timeout or silence_count >= self._silence_timeout:
                                        self._wake_word_callback(json.loads(self._rec.FinalResult())['text'])
                                        break
                        return

                    else:
                        data = data[wanted_length:]
                else:
                    old_data = data



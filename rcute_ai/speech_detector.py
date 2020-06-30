from vosk import Model, KaldiRecognizer
from . import util

class SpeechRecognizer:

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

    def cancel(self):
        self._cancel = True

    def recognize(self, stream, lang='zh', timeout=10, silence_timeout=2):
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
            if recognition_count > timeout:
                return json.loads(rec.FinalResult())['text'].replace(' ','')
            if self._detect.RunDetection(data) == -2: # silence
                silence_count += ln
                if silence_count > silence_timeout:
                    return json.loads(rec.FinalResult())['text'].replace(' ','')



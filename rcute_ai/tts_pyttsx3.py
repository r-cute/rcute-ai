if not util.BUILDING_RTD:
    import pyttsx3

class TTS:
    """see tts_espeak.TTS"""
    def __init__(self):
        self.default_settings= {}
        self._ng = pyttsx3.Engine()

    def _set_properties(self, options):
        op = self.default_settings.copy()
        op.update(options)
        for k,v in op.items():
            self._ng.setProperty(k, v)

    def say(self, txt, **options):
        self._set_properties(options)
        self._ng.say(txt)
        self._ng.runAndWait()

    def tts_wav(self, txt, file=None, **options):
        self._set_properties(options)
        if file:
            self._ng.save_to_file(txt, file)
            return self._ng.runAndWait()
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            self._ng.save_to_file(txt, f.name)
            self._ng.runAndWait()
            f.seek(0)
            return f.read()

    @property
    def voices(self):
        return self._ng.getProperty('voices')
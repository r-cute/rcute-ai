from . import util
import pyttsx3

class TTS:
    """text to speech class used on Win and Mac

    same api as `tts_espeak.TTS <TTS.html#rcute_ai.tts_espeak.TTS>`_ but behaves slightly different

    """
    def __init__(self):
        self.default_settings= {}
        """see `pyttsx3 docs for available property settings <https://pyttsx3.readthedocs.io/en/latest/engine.html#pyttsx3.engine.Engine.setProperty>`_
        """
        self._ng = pyttsx3.Engine()

    def _set_properties(self, options):
        op = self.default_settings.copy()
        op.update(options)
        for k,v in op.items():
            self._ng.setProperty(k, v)

    def say(self, txt, **options):
        """ """
        self._ng.isBusy() and self._ng.stop()
        self._set_properties(options)
        self._ng.say(txt)
        self._ng.runAndWait()

    def tts_wav(self, txt, file=None, **options):
        """ """
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
        """ """
        return self._ng.getProperty('voices')
# modified from github.com/gooofy/py-espeak-ng
import re
import subprocess
import tempfile
from . import util
from pyttsx3.voice import Voice

def lang_detect(txt):
    return 'zh' if re.findall(r'[\u4e00-\u9fff]+', txt) else 'en'

class TTS:
    """text to speech on Linux"""

    def __init__(self):
        self.default_settings= {'b': 1}
        """ voice/volume/pitch/speed etc. See `espeak <http://espeak.sourceforge.net/commands.html>`_ command options section"""
        self._cmd_param_map= {'voice':'v', 'lang':'v',
                                'volume': 'a',
                                'capitals': 'k',
                                'line_length': 'l',
                                'pitch': 'p',
                                'speed': 's',
                                'word_gap': 'g'}

    def _normalize_cmd_param(self, txt, options):
        op = {self._cmd_param_map.get(k,k):str(v) for k,v in self.default_settings.items()}
        op.update({self._cmd_param_map.get(k,k):str(v) for k,v in options.items()})
        if not op.get('v'):
            op['v'] = lang_detect(txt)
        gd = op.pop('gender', None)
        if gd:
            op['v'] = op['v'].split('+')[0] + '+'+ gd.lower()+ ('1' if len(gd)==1 else '')
        return {('-'if len(k)==1 else '--')+k:v for k,v in op.items()}

    def _exe(self, cmd, sync=False):
        # logging.debug ('espeak cmd: '+ ' '.join(cmd))
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        res = iter(p.stdout.readline, b'')
        if not sync:
            p.stdout.close()
            if p.stderr:
                p.stderr.close()
            if p.stdin:
                p.stdin.close()
            return res

        res2 = []
        for line in res:
            res2.append(line)

        p.stdout.close()
        if p.stderr:
            p.stderr.close()
        if p.stdin:
            p.stdin.close()
        p.wait()

        return res2

    def say(self, txt, **options):
        """speak text

        :param txt: text to be said
        :type txt: str
        :param options: if not set, :data:`default_settings` is used.

            * voice/lang: if not set, English is the default unless Chinese characters are detected in :data:`txt`
            * volume
            * pitch
            * speed
            * word_gap

            See `espeak <http://espeak.sourceforge.net/commands.html>`_ command options section
        :type options: optional
        """
        op = self._normalize_cmd_param(txt, options)
        cmd = ['espeak', txt.encode('utf8')]
        cmd.extend(sum(op.items(),()))
        return self._exe(cmd, sync=False)

    def tts_wav(self, txt, file=None, **options):
        """return tts wav or save it to file

        :param txt: text to be said
        :type txt: str
        :param file: path for tts wav data to be saved at, default to None
        :type txt: str, optional
        :param options: if not set, :data:`default_settings` is used.

            * voice/lang: if not set, English is the default unless Chinese characters are detected in :data:`txt`
            * volume
            * pitch
            * speed
            * word_gap

            See `espeak <http://espeak.sourceforge.net/commands.html>`_ command options section
        :type options: optional
        :return: wav data if :data:`file` is not specified
        :rtype: bytes or None
        """
        # if fmt == 'xs':
        #     txt = '[[' + txt + ']]'
        # elif fmt != 'txt':
        #     raise Exception ('unknown format: %s' % fmt)

        with (open(file, 'w') if file else tempfile.NamedTemporaryFile()) as f:
            op = self._normalize_cmd_param(txt, options)
            cmd = ['espeak', txt.encode('utf8'), '-w', f.name]
            cmd.extend(sum(op.items(),()))
            self._exe(cmd, sync=True)
            if file:
                return
            f.seek(0)
            return f.read()

    @property
    def voices(self):
        """return installed voices
        """
        res = self._exe('espeak --voices'.split(), sync=True)
        voices = []
        gd ={'M':'male', 'F':'female'}
        for i,v in enumerate(res[1:]):
            parts = v.decode('utf8').split()

            if len(parts)<5:
                continue

            age_parts = parts[2].split('/')

            voice = Voice(id=i,
                        # 'pty'        : parts[0],
                        languages  = [parts[1]],
                        age        = None if len(age_parts)==1 else age_parts[-2],
                        gender     = gd.get(age_parts[-1], age_parts[-1]),
                        name = parts[3],
                        # 'file'       : parts[4],
                    )

            # logging.debug ('espeakng: voices: parts= %s %s -> %s' % (len(parts), repr(parts), repr(voice)))
            voices.append(voice)

        return voices

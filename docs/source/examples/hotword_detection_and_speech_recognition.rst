语音识别
========================

热词检测和语音识别
-------------------

这个程序进行热词检测和语音识别

热词，即唤醒词，类似于 iPhnone 的“Hi, Siri”或者小米的“小爱同学”。一般的语音识别应用中先要进行热词检测，只有检测到热词之后在进行语音识别。

运行以下程序，对着 Cozmars 背上的麦克风说：“阿Q”，在听到“嘟”的一声提示音后，接着说出你的命令：“前进”/“后退”/“左传”/“右转”，或者说“结束程序”

.. literalinclude:: ../../../examples/speech_recognition.py



.. seealso::

   * `rcute_ai.HotwordRecognizer <../api/HotwordRecognizer.html>`_    
   * `rcute_ai.SpeechRecognizer <../api/SpeechRecognizer.html>`_

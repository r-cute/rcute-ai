语音识别
========================

:class:`rcute_ai.HotwordRecognizer` 和 :class:`rcute_ai.SpeechRecognizer` 两个类分别用来进行热词识别和语音识别，它们的使用方法十分类似

热词，也叫唤醒词，类似于 iPhone 的 “Hi, Siri” 或者小米的 “小爱同学”。一般的语音识别应用中先要进行热词识别，只有听到热词之后，才会对紧接着一段时间内的声音进行语音识别，这样能提高识别的准确性。

热词识别
----------------

:class:`rcute_ai.HotwordRecognizer` 是用来作热词识别的类，若没有特别指定，默认的热词是 “阿Q” 或 “R Cute”

它的 :meth:`recognize` 方法接受一个声音来源作为参数，当识别到热词时，返回识别到的热词字符串；还可以指定一个 :data:`timeout` 参数，如果在 :data:`timeout` 时间（秒）内没有识别到热词，则返回 `None`

运行下面的程序，对则 Cozmars 背上的麦克风说 “阿Q” 或 “R Cute”，看能不能被识别到：

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个热词识别器，默认热词是 “阿Q” 或 “R Cute”
    hotword_rec = ai.HotwordRecognizer()

    # 把 IP 换成你的 Cozmars IP 地址，连接机器人
    with Robot('192.168.1.102') as robot:

        # 把麦克风音量较小，所以我们把音量调到 100%
        robot.microphone.volumn = 100

        # 打开麦克风
        with robot.microphone.get_buffer() as mic_buf:

            while True:

                # 通过 Cozmars 的麦克风进行热词识别，设置 10 秒的超时
                text = hotword_rec.recognize(mic_buf, timeout=10)

                # 如果识别到热词，就发出“嘟”的一声提示音符，并把热词打印出来
                if text:
                    robot.buzzer.set_tone('C4', .2)
                    print('识别到热词：', text)

                # 如果 10 秒内没有识别到热词，就退出程序
                else:
                    break



热词检测 + 语音识别
-------------------------------
:class:`rcute_ai.SpeechRecognizer` 是用来作语音识别的类，默认的语言是中文

它也有一个 :meth:`recognize` 方法从指定的声音来源中识别语音，并返回识别到字符串

接下来我们拓展以上的程序，在热词检测之后进行语音识别。运行程序，对着 Cozmars 背上的麦克风说：“阿Q”，在听到“嘟”的一声提示音后，接着说出你的命令：“前进”/“后退”/“左传”/“右转”，或者说“结束程序”

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个热词识别器，默认热词是 “阿Q” 或 “R Cute”
    hotword_rec = ai.HotwordRecognizer()

    # 新建一个语音识别器，默认语言是中文
    speech_rec = ai.SpeechRecognizer()

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot('192.168.1.102') as robot:

        with robot.microphone.get_buffer() as mic_buf:

            while True:

                # 先进行热词检测，不设置超时，直到识别到热词该函数才返回
                hotword_rec.recognize(mic_buf)
                # 识别到热词后发出“嘟”的一声提示音符
                robot.buzzer.set_tone('C4', .2)

                # 开始语音识别并返回识别到的文字
                text = speech_rec.recognize(mic_buf)
                print(text)

                if text == '前进':
                    robot.forward(3)
                elif text == '后退':
                    robot.backward(3)
                elif text == '左转':
                    robot.turn_left(3)
                elif text == '右转':
                    robot.turn_right(3)
                elif text == '结束程序':
                    break



.. seealso::

   `rcute_ai.HotwordRecognizer <../api/HotwordRecognizer.html>`_ ， `rcute_ai.SpeechRecognizer <../api/SpeechRecognizer.html>`_

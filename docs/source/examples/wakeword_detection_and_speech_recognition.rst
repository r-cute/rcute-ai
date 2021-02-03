语音识别
========================

:class:`rcute_ai.WakeWordDetector` 和 :class:`rcute_ai.STT` 两个类分别用来进行唤醒词检测和语音识别，它们的使用方法十分类似

唤醒词，类似于 iPhone 的 “Hi, Siri” 或者小米的 “小爱同学”。一般的语音识别应用中先要进行唤醒词检测，只有听到唤醒词之后，才会对紧接着一段时间内的声音进行语音识别，这样能提高识别的准确性。

唤醒词检测
----------------

:class:`rcute_ai.WakeWordDetector` 是用来作唤醒词检测的类，若没有特别指定，默认的唤醒词是 “阿Q” 或 “R-Cute”

它的 :meth:`detect` 方法接受一个声音来源作为参数，当识别到唤醒词时，返回识别到的唤醒词字符串；还可以指定一个 :data:`timeout` 参数，如果在 :data:`timeout` 时间（秒）内没有识别到唤醒词，则返回 `None`

运行下面的程序，对则 Cozmars 背上的麦克风说 “阿Q” 或 “R-Cute”，看能不能被识别到：

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个唤醒词检测器，默认唤醒词是 “阿Q” 或 “R-Cute”
    wwd = ai.WakeWordDetector()

    # 把 IP 换成你的 Cozmars IP 地址，连接机器人
    with Robot('192.168.1.102') as robot:

        # 把麦克风音量较小，所以我们把音量调到 100%
        robot.microphone.volumn = 100

        # 打开麦克风
        with robot.microphone.get_buffer() as mic_buf:

            while True:

                # 通过 Cozmars 的麦克风进行唤醒词检测，设置 10 秒的超时
                text = wwd.detect(mic_buf, timeout=10)

                # 如果识别到唤醒词，就发出“嘟”的一声提示音符，并把唤醒词打印出来
                if text:
                    robot.speaker.beep([600])
                    print('识别到唤醒词：', text)

                # 如果 10 秒内没有识别到唤醒词，就退出程序
                else:
                    break



唤醒词检测 + 语音识别
-------------------------------
:class:`rcute_ai.STT` 是用来作语音识别的类，它的 :meth:`stt` 方法将语音转化为文本

接下来我们拓展上面的程序，在唤醒词检测之后进行语音识别。运行程序，对着 Cozmars 背上的麦克风说：“阿Q”，在听到“嘟”的一声提示音后，接着说出你的命令：“前进”/“后退”/“左传”/“右转”，或者说“结束程序”

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个唤醒词检测器，默认唤醒词是 “阿Q” 或 “R-Cute”
    wwd = ai.WakeWordDetector()

    # 新建一个语音识别器，并设置语言为中文（默认是英语）
    sr = ai.STT(lang='zh')

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot('192.168.1.102') as robot:

        with robot.microphone.get_buffer() as mic_buf:

            while True:

                # 先进行唤醒词检测，不设置超时，直到识别到唤醒词该函数才返回
                wwd.detect(mic_buf)
                # 识别到唤醒词后发出“嘟”的一声提示音符
                robot.speaker.beep([600])

                # 开始语音识别并返回识别到的文字
                text = sr.stt(mic_buf)
                print(text)

                if text == '前进':
                    robot.forward(3)
                elif text == '后退':
                    robot.backward(3)
                elif text == '左转':
                    robot.turn_left(3)
                elif text == '右转':
                    robot.turn_right(3)
                elif text == '结束':
                    break



.. seealso::

   `rcute_ai.WakeWordDetector <../api/WakeWordDetector.html>`_ ， `rcute_ai.STT <../api/STT.html>`_

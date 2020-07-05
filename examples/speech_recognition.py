import rcute_ai as ai
from rcute_cozmars import Robot

# 新建一个热词识别器
hotword_rec = ai.HotwordRecognizer()

# 新建一个语音识别器，默认语言是中文
speech_rec = ai.SpeechRecognizer()

# 把 IP 换成你的 Cozmars IP 地址
with Robot('192.168.1.102') as robot:

    # 把麦克风音量较小，所以我们把音量调到 100%
    robot.microphone.volumn = 100

    with robot.microphone as mic:

        while True:

            # 先进行热词检测，默认热词是 “阿Q” 或 “R Cute”, 直到识别到热词该函数才返回
            hotword_rec.recognize(mic.raw_output_stream)
            # 发出“嘟”的一声提示音符
            robot.buzzer.set_tone('C4', .2)


            # 识别语音并返回识别到的文字
            text = speech_rec.recognize(mic.raw_output_stream)
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
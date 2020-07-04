from rcute_ai import SpeechRecognizer, HotwordRecognizer
from rcute_cozmars import Robot

# 新建一个热词识别器
hotword_rec = HotwordRecognizer()

# 新建一个语音识别器
speech_rec = SpeechRecognizer()

# 把 IP 换成你的 Cozmars IP 地址
with Robot('192.168.1.102') as robot:
    with robot.microphone as mic:

        while True:

            # 默认唤醒词是 “阿Q” 或 “R Cute”, 直到识别到唤醒词该函数才返回
            hotword_rec.recognize(mic.raw_output_stream)

            # 识别语音并返回识别到的文字，默认语言是中文
            text = speech_rec.recognize(mic.raw_output_stream)

            if text == '前进':
                robot.forward(2)
            elif text == '后退':
                robot.backward(2)
            elif text == '结束程序':
                break
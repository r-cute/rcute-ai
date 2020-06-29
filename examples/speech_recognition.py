'''
语音识别实验，对着Cozmars的麦克风说: 阿Q，前进
'''
from rcute_ai import SpeechDetector
from rcute_cozmars import Robot

# 新建一个语音识别器
# 默认唤醒词是 “阿Q” 或 “R Cute”，检测到唤醒词后就开始识别语音，默认是中文
# 更多的参数设置可以参考文档：https://rcute-ai.readthedocs.io/zh/latest/
detector = SpeechDetector()

# 一个简单的回调函数，
# 当识别到'前进'或'后退'命令时，就让机器人前进或后退2秒
# 当识别到'程序结束'时停止语音识别
def process_command(text):
    if text == '前进':
        robot.forward(2)
    elif text == '后退':
        robot.backward(2)
    elif text == '程序结束':
        detector.stop()


with Robot(ip='192.168.1.102') as robot:
    with robot.microphone:

        # 开始语音识别，直到`detector.stop()`被调用才结束
        # Cozmars 的麦克风数据流作为语音识别器的输入
        detector.detect(robot.microphone.raw_output_stream, speech_callback=process_command)

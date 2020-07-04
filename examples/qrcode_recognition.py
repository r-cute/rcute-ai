from rcute_ai import QRCodeRecognizer
from rcute_cozmars import Robot
import cv2

# 新建一个二维码识别器
rec = QRCodeRecognizer()

# 把 IP 换成你的 Cozmars IP 地址
with Robot('192.168.1.102') as robot:

    with robot.camera:
        for image in robot.camera.output_stream:

            # 识别图像中的二维码位置和信息
            edges, text = rec.recognize(image)

            # 将识别到的二维码的信息画到图中
            rec.draw_labels(image, edges, text)

            cv2.imshow('QR code recognition', image)

            # 按下键盘上任何按键退出
            if cv2.waitKey(1) > 0:
                break

cv2.destroyAllWindows()
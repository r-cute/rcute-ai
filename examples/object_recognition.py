import rcute_ai as ai
from rcute_cozmars import Robot
import cv2

# 新建一个物体识别器
rec = ai.ObjectRecognizer()

# 把 IP 换成你的 Cozmars IP 地址
with Robot('192.168.1.102') as robot:

    # 如果物体识别比较消耗 CPU, 我们可以降低摄像头帧率:
    robot.camera.framerate = 1

    with robot.camera:
        for image in robot.camera.output_stream:

            # 识别图像中的物体位置和物体名称
            locations, names = rec.recognize(image)

            # 将识别到的物体的信息画到图中
            rec.draw_labels(image, locations, names)

            ai.imshow(image)

            if robot.button.pressed:
                break

ai.imclose()
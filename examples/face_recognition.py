import rcute_ai as ai
from rcute_cozmars import Robot
import cv2

# 新建一个人脸识别器
rec = ai.FaceRecognizer()

# 把 IP 换成你的 Cozmars IP 地址
with Robot('192.168.1.102') as robot:
    with robot.camera:

        for image in robot.camera.output_stream:

            ai.imshow(image)

            # 对着镜头，按下 Cozmars 的按钮拍张照片
            if robot.button.pressed:
                # 让人脸识别器记住你（“主人”）的样子
                rec.memorize('主人', image)
                break


        # 开始人脸识别
        for image in robot.camera.output_stream:

            # 识别图像中的人脸位置和人名
            locations, names = rec.recognize(image)

            # 把识别到的人脸信息（位置和名字）画到图上
            rec.draw_labels(image, locations, names)

            ai.imshow(image)

            # 长按 Cozmars 的按钮推出程序
            if robot.button.held:
                break

ai.imclose()

from rcute_ai import FaceRecognizer
from rcute_cozmars import Robot

# 新建一个人脸识别器
rec = FaceRecognizer()

# 让人脸器记住两人的样子
rec.memorize('李雷', './lilei.jpg')
rec.memorize('韩梅梅', './hanmeimei.jpg')

with Robot(ip='192.168.1.102') as robot:
    with robot.camera:
        for image in robot.camera.output_stream:

            # # 识别图像中的人脸位置和人名
            locations, names = rec.recognize(image)

            # 将识别到的人脸信息（位置和名字）画到图上
            rec.draw_labels(image, locations, names)

            cv2.imshow('face recognition', image)

            # 按下任何按键就退出
            if cv2.waitKey(1) > 0:
                break

cv2.destroyAllWindows()

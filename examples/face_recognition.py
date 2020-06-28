from rcute_ai import FaceDetector
from rcute_cozmars import Robot

# 新建一个人脸识别器
detector = FaceDetector()

# 让人脸器记住两人的样子
detector.memorize('李雷', './lilei.jpg')
detector.memorize('韩梅梅', './hanmeimei.jpg')

with Robot(ip='192.168.1.102') as robot:
    with robot.camera:
        for image in robot.camera.output_stream:

            # 开始识别
            detector.detect(image)
            # 将识别到的人脸信息（位置和名字）画到图上
            detector.draw_face_info(image, locations=True, names=True, landmarks=False)

            cv2.imshow('face recognition', image)

            # 按下任何按键就退出
            if cv2.waitKey(1) > 0:
                break

cv2.destroyAllWindows()

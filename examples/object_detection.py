from rcute_ai import ObjectDetector
from rcute_cozmars import Robot

# 新建一个物体识别器
detector = ObjectDetector()

with Robot(ip='192.168.1.102') as robot:

    # 如果物体识别比较消耗CPU, 我们也可以降低帧率
    # robot.camera.framerate = 3
    with robot.camera:
        for image in robot.camera.output_stream:

            obj_info = detector.detect(image)

            # 将识别到的物体的信息画到图中
            detector.draw(image, obj_info)

            cv2.imshow('object detection', image)

            # press any key to stop
            if cv2.waitKey(1) > 0:
                break

cv2.destroyAllWindows()


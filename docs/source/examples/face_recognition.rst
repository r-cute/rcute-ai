人脸检测和识别
======================

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个人脸识别器
    face = ai.FaceDetector()

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot() as robot:
        with robot.camera.get_buffer() as cam_buf:

            for image in cam_buf:
                ai.imshow(image)

                # 对着镜头，按下 Cozmars 的按钮拍张照片
                if robot.button.pressed:
                    # 让人脸识别器记住你（“主人”）的样子
                    face.memorize('主人', image)
                    break


            for image in cam_buf:

                # 识别图像中的人脸位置和人名
                locations, names = face.detect(image)

                # 把识别到的人脸信息（位置和名字）画到图上
                face.annotate(image, locations, names)

                ai.imshow(image)

                # 长按 Cozmars 的按钮推出程序
                if robot.button.held:
                    break

    ai.imclose()


.. seealso::

   `rcute_ai.FaceDetector <../api/FaceDetector.html>`_
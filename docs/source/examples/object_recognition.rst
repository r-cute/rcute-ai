物品识别
==========

:class:`rcute_ai.ObjectDetector` 类可以用来识别图像中的物品，使用十分简单。:meth:`detect` 方法用来识别图像，返回图像中识别到的物品的位置和名称，:meth:`annotate` 方法可以将识别到的物品在图像中标注出来

.. note::

    :class:`rcute_ai.ObjectDetector` 并不能识别所有的物品。它是 yolov3 的简单封装，使用 coco 数据集训练的模型，能够识别这 |80种物品|

    .. |80种物品| raw:: html

       <a href='https://github.com/pjreddie/darknet/blob/master/data/coco.names' target='blank'>80种物品</a>

下面利用 Cozmars 机器人的摄像头，来演示物品识别：

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个物体识别器
    det = ai.ObjectDetector()

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot() as robot:

        # 打开摄像头
        with robot.camera.get_buffer() as cam_buf:

            for image in cam_buf:

                # 识别图像中的物体位置和物体名称
                locations, names = det.detect(image)

                # 将识别到的物体的信息画到图中
                det.annotate(image, locations, names)

                # 显示图像
                ai.imshow(image)

                # 按下按钮就结束程序
                if robot.button.pressed:
                    break

    # 关闭图像
    ai.imclose()



.. seealso::

   `rcute_ai.ObjectDetector <../api/ObjectDetector.html>`_



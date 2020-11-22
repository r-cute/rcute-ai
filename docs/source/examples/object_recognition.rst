物品识别
==========

:class:`rcute_ai.ObjectRecognizer` 类可以用来识别图像中的物品，使用十分简单。:meth:`recognize` 方法用来识别图像，返回图像中识别到的物品的位置和名称，:meth:`draw_labels` 方法可以将识别到的物品在图像中标注出来

.. note::

    :class:`rcute_ai.ObjectRecognizer` 并不能识别所有的物品。它是 yolov3 的简单封装，使用 coco 数据集训练的模型，能够识别这 |80种物品|

    .. |80种物品| raw:: html

       <a href='https://github.com/pjreddie/darknet/blob/master/data/coco.names' target='blank'>80种物品</a>

下面利用 Cozmars 机器人的摄像头，来演示物品识别：

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个物体识别器
    rec = ai.ObjectRecognizer()

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot('192.168.1.102') as robot:

        # 如果物体识别比较消耗 CPU, 我们可以降低摄像头帧率:
        robot.camera.frame_rate = 1

        # 打开摄像头
        with robot.camera.get_buffer() as cam_buf:

            for image in cam_buf:

                # 识别图像中的物体位置和物体名称
                locations, names = rec.recognize(image)

                # 将识别到的物体的信息画到图中
                rec.draw_labels(image, locations, names)

                # 显示图像
                ai.imshow(image)

                # 按下按钮就结束程序
                if robot.button.pressed:
                    break

    # 关闭图像
    ai.imclose()



.. seealso::

   `rcute_ai.ObjectRecognizer <../api/ObjectRecognizer.html>`_



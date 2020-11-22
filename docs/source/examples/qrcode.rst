二维码
======================

.. code:: python

    import rcute_ai as ai
    from rcute_cozmars import Robot

    # 新建一个二维码识别器
    rec = ai.QRCodeRecognizer()

    # 把 IP 换成你的 Cozmars IP 地址 或 序列号
    with Robot('192.168.1.102') as robot:

        with robot.camera.get_buffer() as cam_buf:
            for image in cam_buf:

                # 识别图像中的二维码位置和信息
                points, text = rec.recognize(image)

                # 将识别到的二维码的信息画到图中
                rec.draw_labels(image, points, text)

                ai.imshow(image)

                if robot.button.pressed:
                    break

    ai.imclose()

.. seealso::

   `rcute_ai.QRCodeRecognizer <../api/QRCodeRecognizer.html>`_
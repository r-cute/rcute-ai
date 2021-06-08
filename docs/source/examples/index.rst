快速上手
==========

.. note::

    值得说明的是，图像的 “检测”（detection）和 “识别”（recognition) 严格来说是不同的两个概念。“检测” 是判断图像中是否包含某物品，而“识别”是要区分物品的种类。

    比如，“人脸检测”只要判断图像中是否包含人脸（如果有的话指出人脸的位置），而“人脸识别”是判断这个人是谁。

    但实际应用中 “检测” 和 “识别” 两个概念有时没有严格的区分，有时还有 “追踪”（tracking）的功能。

    为了提供简单一致的 API，rcute_ai 在命名时也没有严格区分 “检测” 和 “识别”，许多类名都叫 :data:`xxxDetector`，并且都有一个 :meth:`detect` 方法，但实际上常常既有检测也有识别的功能。

.. toctree::
   :maxdepth: 2


   face_recognition
   qrcode
   object_recognition
   wakeword_detection_and_speech_recognition

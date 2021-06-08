安装 rcute-ai
================

Windows
++++++++++

* 对于 Windows 用户，首先确保你用的是 Python *3.7 或 3.8 版本的 64位* 解释器，如果你已经安装了 Python，运行以下代码查看是否符合要求：

        .. code::

            import sys
            print(sys.version)
            print(len("{0:b}".format(sys.maxsize))+1, 'bit')

    如果是 32位，或者你还未安装 Python，请到 `Python 官网 <https://python.org>`_ 下载 `Python 64位 3.7 版本 <https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe>`_，安装时记得勾选 “添加 Python 到 PATH”。

* 安装 dlib 模块

    如果是 Python 3.7 版本，下载 `dlib-19.21.0-cp37-cp37m-win_amd64.whl <https://cdn.jsdelivr.net/gh/vivekmathema/Dlib19.2.1_windows/dlib-19.21.0-cp37-cp37m-win_amd64.whl>`_

    如果是 Python 3.8 版本，下载 `dlib-19.19.0-cp38-cp38-win_amd64.whl <https://cdn.jsdelivr.net/gh/pratyusa98/face-recognition_dlib_library/face-recognition_dlib_library/dlib-19.19.0-cp38-cp38-win_amd64.whl>`_

    然后在所下载的文件夹路径下，运行：

    .. code::

        python -m pip install dlib-xxx # 用刚下载的文件名取代这里的 dlib-xxx

* 最后安装 rcute-ai 及其依赖资源文件，方法和下面 `Mac OS X <#mac-os-x>`_ 一样：

Mac OS X
++++++++++++

* 安装 rcute-ai，在命令窗口里输入：

    .. code::

        python -m pip install rcute-ai

    或者，从国内的镜像服务器下载安装，速度会快很多：

    .. code::

        python -m pip install rcute-ai -i https://pypi.tuna.tsinghua.edu.cn/simple

.. _data-file:

* （可选）下载 rcute-ai 依赖的资源文件

    新建一个文件夹用于存放这些资源文件，新建环境变量 “RCUTE_AI_DATA_PATH” ，把这个文件夹的路径作为该环境变量的值。这样当 rcute-ai 模块需要相应资源文件时就会到这个文件夹里寻找。

    * 语音识别

        在上述的文件夹里，新建一个名为 “vosk” 的文件夹。

        从 https://alphacephei.com/vosk/models 下载用于语音识别的模型文件，解压到 vosk 文件夹里，并将解压出来的文件夹命名为对应语言的缩写。该缩写和 语音识别类 `rcute_ai.STT <api/STT.html>`_ 的语言参数对应

        比如，下载中文模型 `vosk-model-cn-0.1.zip <https://alphacephei.com/vosk/models/vosk-model-cn-0.1.zip>`_ 和 英文模型 `vosk-model-en-us-daanzu-20200905-lgraph <https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905-lgraph.zip>`_ ，解压到 vosk 文件夹里，分别得到 “vosk-model-cn-0.1” 和 “vosk-model-en-us-daanzu-20200905-lgraph” 两个文件夹。

        然后在 vosk 文件夹里新建一个名为 map.json 的文件，里面写明不同语言对应的语言模型：

        .. code:: json

            {
            "zh": "vosk-model-cn-0.1",
            "cn": "vosk-model-cn-0.1",
            "en": "vosk-model-en-us-daanzu-20200905-lgraph"
            }

        英文模型是语音唤醒必须的，其他语言为可选。

    * 物体识别

        在上述环境变量 “RCUTE_AI_DATA_PATH” 对应的文件夹里，新建另一个名为 “yolo” 的文件夹，在 “yolo” 文件夹里再新建一个 “coco” 文件夹。

        下载 `coco.names <https://codechina.csdn.net/mirrors/pjreddie/darknet/-/raw/master/data/coco.names?inline=false>`_， `yolov3.cfg <https://codechina.csdn.net/mirrors/pjreddie/darknet/-/raw/master/cfg/yolov3.cfg?inline=false>`_， `yolov3.weights <https://pjreddie.com/media/files/yolov3.weights>`_ 三个文件到 coco 文件夹里

..
    在文件保存路径下，运行命令：

    .. code::

        python -m pip install xxx # 用刚下载的文件名取代这里的 xxx

对于 Windows 或 Mac 用户来说，到这里就结束了

Linux
++++++++++

* 首先，参考上面 `Mac OS X <#mac-os-x>`_ 的步骤安装 rcute-ai 及其依赖资源模块。你可能需要把命令行中的 :data:`python` 换成 :data:`python3`

* 然后，Linux 用户需要另外安装以下程序：

    .. code::

        sudo apt install espeak ffmpeg libespeak1 tesseract-ocr

* （可选）简体中文文字识别：

    .. code::

        sudo apt install tesseract-ocr-chi-sim

* （可选）中文语音合成：

    .. code::

        git clone https://codechina.csdn.net/mirrors/caixxiong/espeak-data.git
        sudo mv /usr/lib/x86_64-linux-gnu/espeak-data /usr/lib/x86_64-linux-gnu/espeak-data.dak
        sudo unzip espeak-data/espeak-data.zip -d /usr/lib/x86_64-linux-gnu/
        cd /usr/lib/x86_64-linux-gnu/espeak-data
        sudo espeak --compile=zh
        sudo espeak --compile=zhy

    以上命令添加 espeak 的普通话和粤语的语音合成

..
    从 `espeak <http://espeak.sourceforge.net/>`_ 官网下载
    `espeak-1.48.04-source.zip <http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/espeak-1.48.04-source.zip>`_ 和 `zh_listx.zip <http://espeak.sourceforge.net/data/zh_listx.zip>`_ 文件，分别解压后，将 zh_listx 和 espeak-1.48.04-source/dictsource 里的文件都复制到 /usr/lib/x86_64-linux-gnu/ 文件夹，然后在该文件夹里执行命令 :data:`espeak --compile=zh`

    和普通话一样，粤语和俄语也需要另行安装，见 http://espeak.sourceforge.net/data/


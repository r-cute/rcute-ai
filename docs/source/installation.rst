安装 rcute-ai
================

在命令窗口里输入：

    .. code::

        python3 -m pip install rcute-ai

    或者，从国内的镜像服务器下载安装，速度会快很多：

    .. code::

        python3 -m pip install rcute-ai -i https://pypi.tuna.tsinghua.edu.cn/simple

对于 Windows 或 Linux 的用户，有几点需要注意：

Windows
++++++++++

* 对于 Windows 用户，首先确保你用的是 Python *3.7 或 3.8 版本的 64位* 解释器，如果你已经安装了 Python，运行以下代码查看是否符合要求：

        .. code::

            import sys
            print(sys.version)
            print(len("{0:b}".format(sys.maxsize))+1, 'bit')

    如果是 32位，或者你还未安装 Python，请到 `Python 官网 <https://python.org>`_ 下载 `Python 64位 3.7 版本 <https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe>`_，安装时记得勾选“添加 Python 到 PATH”。

* 安装 dlib 模块

    如果是 Python 3.7 版本，下载 `dlib-19.21.0-cp37-cp37m-win_amd64.whl <https://cdn.jsdelivr.net/gh/vivekmathema/Dlib19.2.1_windows/dlib-19.21.0-cp37-cp37m-win_amd64.whl>`_

    如果是 Python 3.8 版本，下载 `dlib-19.19.0-cp38-cp38-win_amd64.whl <https://cdn.jsdelivr.net/gh/pratyusa98/face-recognition_dlib_library/face-recognition_dlib_library/dlib-19.19.0-cp38-cp38-win_amd64.whl>`_

    然后在所下载的文件夹路径下，运行：

    .. code::

        python -m pip install dlib-... # 用刚下载的文件名取代这里的 dlib-...

* 以上两步都完成后再安装 rcute-ai：

    .. code::

        python -m pip install rcute-ai -i https://pypi.tuna.tsinghua.edu.cn/simple




Linux
++++++++++

* Linux 用户需要另外安装以下程序：

    .. code::

        sudo apt install espeak ffmpeg libespeak1

* （可选）中文语音合成：

    .. code::

        git clone https://codechina.csdn.net/mirrors/caixxiong/espeak-data.git
        sudo mv /usr/lib/x86_64-linux-gnu/espeak-data /usr/lib/x86_64-linux-gnu/espeak-data.dak
        sudo unzip espeak-data/espeak-data.zip -d /usr/lib/x86_64-linux-gnu/
        cd /usr/lib/x86_64-linux-gnu/
        sudo espeak --compile=zh
        sudo espeak --compile=zhy

    以上命令添加 espeak 的普通话和粤语的语音合成

..
    从 `espeak <http://espeak.sourceforge.net/>`_ 官网下载
    `espeak-1.48.04-source.zip <http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/espeak-1.48.04-source.zip>`_ 和 `zh_listx.zip <http://espeak.sourceforge.net/data/zh_listx.zip>`_ 文件，分别解压后，将 zh_listx 和 espeak-1.48.04-source/dictsource 里的文件都复制到 /usr/lib/x86_64-linux-gnu/ 文件夹，然后在该文件夹里执行命令 :data:`espeak --compile=zh`

    和普通话一样，粤语和俄语也需要另行安装，见 http://espeak.sourceforge.net/data/


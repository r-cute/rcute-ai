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

如果你用的是 Windows 系统，你需要使用 Python *64位* 解释器，因为 rcute-ai 的语音识别功能无法在 Windows 的 Python 32位解释器上运行，请到 `Python 官网 <https://python.org>`_ 下载安装 Python 64位

如何查看 Python 解释器是否为 64位：

    .. code::

        import sys
        print(len("{0:b}".format(sys.maxsize))+1)


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


安装
======

rcute-ai 的语音识别功能需要使用 Python *64位* 解释器，如果您使用的是 Python 32位版，请到 `Python 官网 <https://python.org>`_ 下载安装 Python 64位

如何查看 Python 解释器是否为 64位：

.. code::

    import sys
    print(len("{0:b}".format(sys.maxsize))+1)


Windows
++++++++++

1. 下载安装 `espeak-ng-x64.msi <https://github.com/espeak-ng/espeak-ng/releases>`_ ，然后

2. 安装 rcute-ai，在命令窗口或 PowerShell 里输入：

    .. code::

        python3 -m pip install rcute-ai

    或者，从国内的镜像服务器下载安装，速度会快很多：

    .. code::

        python3 -m pip install rcute-ai -i https://pypi.tuna.tsinghua.edu.cn/simple

Mac OS X
+++++++++++

.. code::

    brew install espeak
    python3 -m pip install rcute-ai

Linux
++++++++++

.. code::

    sudo apt install espeak-ng
    python3 -m pip install rcute-ai


install
==============

Windows
--------------

* Make sure you use Python 3.7 or 3.8 version 64 bit interpreter. To find out:

    ```
    import sys
    print(sys.version>`_
    print(len("{0:b}".format(sys.maxsize>`_>`_+1, 'bit'>`_
    ```

    if not, install `Python3.7 64-bit <https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe>`_ , and add it to PATH

* Install dlib module

    for Python 3.7, download `dlib-19.21.0-cp37-cp37m-win_amd64.whl <https://github.com/vivekmathema/Dlib19.2.1_windows/raw/master/dlib-19.21.0-cp37-cp37m-win_amd64.whl>`_

    for Python 3.8, download `dlib-19.19.0-cp38-cp38-win_amd64.whl <https://github.com/pratyusa98/face-recognition_dlib_library/raw/main/face-recognition_dlib_library/dlib-19.19.0-cp38-cp38-win_amd64.whl>`_

    install it `python -m pip install xxx.whl`

* Then, install rcute-ai and required data resources, same as described in "Mac OS X" section below

Mac OS X
-----------

* install rcute-ai

    `python3 -m pip install rcute-ai`

* (Optional) download data resources.

    Create a folder for the resources, and set evironment variable "RCUTE_AI_DATA" to the path to this folder.

    * Speech recognition

        Create another folder called "vosk" inside the folder that "RCUTE_AI_DATA" points to.

        Download model files from https://alphacephei.com/vosk/models, and unzip to the "vosk" folder, rename unzipped folder as language name that will later be use by `rcute_ai.TTS <https://rcute-ai.readthedocs.io/zh_CN/latest/api/STT.html>`_ class.

        For example, download English model `vosk-model-en-us-daanzu-20200905-lgraph <https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905-lgraph.zip>`_ , unzip to "vosk" folder, rename "vosk-model-en-us-daanzu-20200905-lgraph" folder to "en".

    * Object recognition

        Create another folder called "yolo" inside the folder that "RCUTE_AI_DATA" points to. Inside "yolo", create another folder called "coco"

        Download `coco.names <https://codechina.csdn.net/mirrors/pjreddie/darknet/-/raw/master/data/coco.names?inline=false>`_ , `yolov3.cfg <https://codechina.csdn.net/mirrors/pjreddie/darknet/-/raw/master/cfg/yolov3.cfg?inline=false>`_ and `yolov3.weights <https://pjreddie.com/media/files/yolov3.weights>`_ to "coco" folder

    That's it for Windows and Mac users.

Linux
------------

* First, install rcute-ai and required data resources, same as described in "Mac OS X" section above

* `sudo apt install espeak ffmpeg libespeak1`

* (Optional) install Chinese (Mandarine/Cantonese) TTS

    ```
    git clone https://codechina.csdn.net/mirrors/caixxiong/espeak-data.git
    sudo mv /usr/lib/x86_64-linux-gnu/espeak-data /usr/lib/x86_64-linux-gnu/espeak-data.dak
    sudo unzip espeak-data/espeak-data.zip -d /usr/lib/x86_64-linux-gnu/
    cd /usr/lib/x86_64-linux-gnu/
    sudo espeak --compile=zh
    sudo espeak --compile=zhy
    ```


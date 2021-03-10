# rpi-object-tracking

1. [About](#about)
1. [OS Requirements](#os-requirements)
1. [Python Requirements](#python-requirements)
1. [Usage](#usage)
1. [Issues](#issues)
1. [Reference Links](#reference-links)

## About
This project is inspired in [this](https://github.com/leigh-johnson/rpi-deep-pantilt) one but in this case it makes use of the [Pi's Camera web stream recipe](http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming) to stream video from the Pi's Camera over HTTP. I've tweaked it for my own purposes. \
I'm evaluating solutions for object detection as [CVLib](https://www.cvlib.net/) and [ImageAI](https://imageai.readthedocs.io/en/latest/).
Also, I'm evaluating capturing images with PiCamera or OpenCV.

## OS Requirements
* Install the following libraries:
  * libhdf5-dev
  * libhdf5-103
  * libatlas-base-dev
  * libjasper-dev
  * libilmbase-dev
  * libopenexr-dev
  * libgstreamer1.0-dev
  * libavcodec-dev
  * libavformat-dev
  * libswscale-dev

  If you're using Raspbian or derivatives you can do by running:
  ```bash
  apt-get install libhdf5-dev libhdf5-103 libatlas-base-dev libjasper-dev libilmbase-dev libopenexr-dev libgstreamer1.0-dev libavcodec-dev libavformat-dev libswscale-dev
  ```

## Python Requirements
Install the _requirements.txt_ file:
```bash
pip install -r src/requirements.txr
```
If you have resource issues when installing tensorflow try running:
```bash
mkdir pip_tmp
TMPDIR=pip_tmp pip install tensorflow --no-cache-dir
rm -rf pip_tmp
```

## Usage
```bash
python picamera_stream.py
```
Then check the live video at [http://127.0.0.1:8000](http://127.0.0.1:8000). \
Or you can set the IP/Port where the app will be listening to by using environment varables (or you can edit them inside the code as well).
```bash
STREAM_IP=192.168.0.151 STREAM_PORT=8080 python picamera_stream.py
```
Then check the live video at [http://192.168.0.151:8080](http://192.168.0.151:8080).

## Issues
* Pip process is killed when installing tensorflow. This is likely you're running log on resources, try running:
  ```bash
  mkdir pip_tmp
  TMPDIR=pip_tmp pip install tensorflow --no-cache-dir
  rm -rf pip_tmp
  ```
* `HadoopFileSystem load error: libhdfs.so: cannot open shared object file: No such file or directory` \
You can safely ignore this error if you're not using HadoopFS, otherwise you will need to upgrade Tensorflow to 2.x.

## Reference Links
* [Original project article](https://towardsdatascience.com/real-time-object-tracking-with-tensorflow-raspberry-pi-and-pan-tilt-hat-2aeaef47e134)
* [Original project repo](https://github.com/leigh-johnson/rpi-deep-pantilt)
* [Pi's Camera web stream recipe](https://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming)
* [Pi's Camera API reference](https://picamera.readthedocs.io/en/release-1.13/api_camera.html)
* [Streaming with Flask article](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page)
* [Streaming with Flask repo](https://github.com/miguelgrinberg/flask-video-streaming)
* [Install OpenCV](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) (alternative way)
* [Install Tensorflow](https://www.tensorflow.org/install/pip) (alternative way)
* [CVlib Repo](https://github.com/arunponnusamy/cvlib)

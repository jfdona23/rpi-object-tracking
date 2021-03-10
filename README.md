# rpi-object-tracking

1. [About](#about)
1. [OS Requirements](#os-requirements)
1. [Python Requirements](#python-requirements)
1. [Usage](#usage)
1. [Issues](#issues)
1. [Reference Links](#reference-links)

## About
This project is inspired in [this](https://github.com/leigh-johnson/rpi-deep-pantilt) one but I'm writting it from scratch for learning purposes.

## OS Requirements
* Install the following libraries to ensure tensorflow works properly:
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

  If you're using Raspbian or derivatives you can do it by running:
  ```bash
  apt-get install libhdf5-dev libhdf5-103 libatlas-base-dev libjasper-dev libilmbase-dev libopenexr-dev libgstreamer1.0-dev libavcodec-dev libavformat-dev libswscale-dev
  ```

## Python Requirements
Install the _requirements.txt_ file:
```bash
pip install -r src/requirements.txr
```

## Usage
Several options can be configured using environment variables before the command:
|   Variable  |                 Description                 |  Default  |
|:-----------:|:-------------------------------------------:|:---------:|
| LISTEN_HOST | Webserver IP address                        | "0.0.0.0" |
| LISTEN_PORT | Webserver Port number                       |   "8080"  |
| MODE        | Camera backend: picamera or opencv (*)      |  picamera |
| RES_WIDTH   | Resolution - width                          |    640    |
| RES_HEIGHT  | Resolution - height                         |    480    |
| FRAMERATE   | Framerate (currently is not implemented)    |     24    |
| DETECT      | Enable (1) or disable (0) objects detection |     1     |
Example:
```bash
LISTEN_HOST=127.0.0.1 MODE=opencv RES_WIDTH=1280 RES_HEIGHT=800 DETECT=0 python3 src/camera_stream.py
```
Then check the live video at [http://127.0.0.1:8080/video_feed](http://127.0.0.1:8080/video_feed). \
_(*) OpenCV showed to perform faster than PiCamera_

## Issues
* Pip process is killed when installing tensorflow. This is likely you're running log on resources, try running:
  ```bash
  mkdir pip_tmp
  TMPDIR=pip_tmp pip install tensorflow --no-cache-dir
  rm -rf pip_tmp
  ```
* `HadoopFileSystem load error: libhdfs.so: cannot open shared object file: No such file or directory` \
You can safely ignore this error if you're not using HadoopFS, otherwise you will need to upgrade Tensorflow to 2.x.
* When enabling object detection, the image lag is just horrible. Well, this is part of my next step where I'll try using Threads and buffers to improve latency, but at the moment every single frame is sent to the object detection method, parsed and then sent back to finally be encoded as a .jpg image. Such a journey for a single frame, hum?

## Reference Links
* [Leigh Johnson article](https://towardsdatascience.com/real-time-object-tracking-with-tensorflow-raspberry-pi-and-pan-tilt-hat-2aeaef47e134)
* [Leigh Johnson project repo](https://github.com/leigh-johnson/rpi-deep-pantilt)
* [Pi's Camera web stream recipe](https://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming)
* [Pi's Camera API reference](https://picamera.readthedocs.io/en/release-1.13/api_camera.html)
* [Streaming with Flask article](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page)
* [Streaming with Flask repo](https://github.com/miguelgrinberg/flask-video-streaming)
* [Install OpenCV](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) (alternative way)
* [Install Tensorflow](https://www.tensorflow.org/install/pip) (alternative way)
* [CVlib Repo](https://github.com/arunponnusamy/cvlib)

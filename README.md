# rpi-object-tracking

1. [About](#about)
1. [Usage](#usage)

## About
This project makes use of the [Pi's Camera web stream recipe](http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming) to stream video from the Pi's Camera over HTTP. I've tweaked it for my own purposes. \
I'm evaluating solutions for object detection as [CVLib](https://www.cvlib.net/) and [ImageAI](https://imageai.readthedocs.io/en/latest/).

## Usage
```bash
pip install -r src/requirements.txr
python picamera_stream.py
```
Then check the live video at [http://127.0.0.1:8000](http://127.0.0.1:8000). \
Or you can set the IP/Port where the app will be listening to by using environment varables (or you can edit them inside the code as well).
```bash
pip install -r src/requirements.txr
STREAM_IP=192.168.0.151 STREAM_PORT=8080 python picamera_stream.py
```
Then check the live video at [http://192.168.0.151:8080](http://192.168.0.151:8080).

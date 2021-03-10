"""
Video Stream over HTTP
"""
import os

from flask import Flask, render_template, Response

from camera_capture import CameraCapture


# ----------------------------------------------------------------------------------------------- #
# Variables and config
# ----------------------------------------------------------------------------------------------- #
LISTEN_HOST = os.environ.get("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = os.environ.get("LISTEN_PORT", "8080")

app = Flask(__name__)


# ----------------------------------------------------------------------------------------------- #
# Main Program
# ----------------------------------------------------------------------------------------------- #
# @app.route('/')
# def index():
#     return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(
        gen(CameraCapture()),
        mimetype='multipart/x-mixed-replace; boundary=frame',
    )


# ----------------------------------------------------------------------------------------------- #
# Main Loop
# ----------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    app.run(host=LISTEN_HOST, port=LISTEN_PORT, debug=True)
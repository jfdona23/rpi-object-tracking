"""
Web streaming example
Source code from the official PiCamera package
http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming
"""

import io
import logging
import os
import socketserver

from http import server
from threading import Condition

import picamera

from pages import index_page

# ----------------------------------------------------------------------------------------------- #
# Constants and Config
# ----------------------------------------------------------------------------------------------- #
STREAM_IP = os.environ.get("STREAM_IP", "")
STREAM_PORT = int(os.environ.get("STREAM_PORT", 8000))


# Pi's Camera settings
camera_resolution = "640x480"
camera_framerate = 24
camera_rotation = 180
camera_exposure_mode = "auto"
camera_sensor_mode = 0
camera_awb_mode = "auto"
camera_drc_strength = "high"
output = None # StreamingOutput class object shared by the main loop and the HTTP handler


# ----------------------------------------------------------------------------------------------- #
# Main Programm
# ----------------------------------------------------------------------------------------------- #
class StreamingOutput(object):
    """StreamingOutput"""

    def __init__(self):
        """Init"""

        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        """Write bytes into the stream
        
        Args:
            - buf (buffer): Buffer where write to

        Returns:
            - int: Number of bytes written
        """

        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    """StreamingHandler"""

    def do_GET(self):
        """do_GET"""

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = index_page.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                global output
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    """StreamingServer"""

    allow_reuse_address = True
    daemon_threads = True


def start():
    """Start"""

    with picamera.PiCamera() as camera:
        # Pi's Camera settings
        camera.resolution = camera_resolution
        camera.framerate = camera_framerate
        camera.rotation = camera_rotation
        camera.exposure_mode = camera_exposure_mode
        camera.sensor_mode = camera_sensor_mode
        camera.awb_mode = camera_awb_mode
        camera.drc_strength = camera_drc_strength

        global output
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            address = (STREAM_IP, STREAM_PORT)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()

# ----------------------------------------------------------------------------------------------- #
# Main Loop
# ----------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    start()

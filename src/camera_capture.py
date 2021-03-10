"""
Capture video from camera
"""
import os

from time import sleep

import cv2
import numpy as np

from picamera import PiCamera


# ----------------------------------------------------------------------------------------------- #
# Variables and config
# ----------------------------------------------------------------------------------------------- #
MODE = os.environ.get("MODE", "picamera")
RES_WIDTH = int(os.environ.get("RES_WIDTH", 640))
RES_HEIGHT = int(os.environ.get("RES_HEIGHT", 480))
FRAMERATE = int(os.environ.get("FRAMERATE", 24))
DETECT = bool(int(os.environ.get("DETECT", 1)))

if DETECT:
    from object_detection import detect_common_objects

# Camera settings
camera_resolution_width = RES_WIDTH
camera_resolution_height = RES_HEIGHT
camera_resolution = (camera_resolution_width, camera_resolution_height)
camera_framerate = FRAMERATE
camera_rotation = 180
camera_exposure_mode = "auto"
camera_sensor_mode = 0
camera_awb_mode = "auto"
camera_drc_strength = "high"


# ----------------------------------------------------------------------------------------------- #
# Main Program
# ----------------------------------------------------------------------------------------------- #
class CameraCapture:
    """Camera Capture"""

    frame = None

    def __init__(self, mode=MODE):
        """Init the programm using picamera or opencv backend"""

        self.mode = mode
        self.is_picamera = False
        self.is_opencv = False
        if self.mode.lower() == "picamera":
            self.is_picamera = True
            self.camera = PiCamera()
            self.camera.resolution = camera_resolution
            self.camera.framerate = camera_framerate
            self.camera.rotation = camera_rotation
            self.camera.exposure_mode = camera_exposure_mode
            self.camera.sensor_mode = camera_sensor_mode
            self.camera.awb_mode = camera_awb_mode
            self.camera.drc_strength = camera_drc_strength
            sleep(2)
        elif self.mode.lower() == "opencv":
            self.is_opencv = True
            self.camera = cv2.VideoCapture(0)
            sleep(2)
            if not self.camera.isOpened():
                raise IOError("Could not open Camera")
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_resolution_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_resolution_height)
        else:
            raise ValueError("Camera mode unknown. Please select either picamera or opencv")
 
    def close_camera(self):
        """Close the camera"""

        if self.is_picamera:
            self.camera.close()

        if self.is_opencv:
            self.camera.release()

    def get_frame(self):
        """Get a frame
        
        Returns:
            - (array): A numpy array containing a image frame
        """

        if self.is_picamera:
            CameraCapture.frame = np.empty(
                (camera_resolution_height * camera_resolution_width * 3,),
                dtype=np.uint8
            )
            self.camera.capture(CameraCapture.frame , "bgr")
            CameraCapture.frame = CameraCapture.frame.reshape((camera_resolution_height, camera_resolution_width, 3))

        if self.is_opencv:
            if self.camera.isOpened():
                _, CameraCapture.frame = self.camera.read()
                CameraCapture.frame = cv2.rotate(CameraCapture.frame, cv2.ROTATE_180)
        
        image = detect_common_objects(CameraCapture.frame) if DETECT else CameraCapture.frame
        return cv2.imencode('.jpg', image)[1].tobytes()

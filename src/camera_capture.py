"""
Capture video from camera
"""
import cv2
import numpy as np

from time import sleep

from picamera import PiCamera

# from object_detection import detect_common_objects


MODE = os.environ.get("MODE", "picamera")

# Camera settings
camera_resolution_width = 320
camera_resolution_height = 320
camera_resolution = (camera_resolution_width, camera_resolution_height)
camera_framerate = 8
camera_rotation = 180
camera_exposure_mode = "auto"
camera_sensor_mode = 0
camera_awb_mode = "auto"
camera_drc_strength = "high"

class CameraCapture:
    """Camera Capture"""

    def __init__(self, mode=MODE):
        """Init the programm using picamera or opencv backend"""

        self.mode = mode
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
            self.camera.set(CAP_PROP_FRAME_WIDTH, camera_resolution_width)
            self.camera.set(CAP_PROP_FRAME_HEIGHT, camera_resolution_height)
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
            image_array = np.empty(
                (camera_resolution_height * camera_resolution_width * 3,),
                dtype=np.uint8
            )
            self.camera.capture(image_array, "bgr")
            image_array = image_array.reshape((camera_resolution_height, camera_resolution_width, 3))
            # Toggle the comments to enable/disable object detection
            # image = detect_common_objects(image_array)
            image = image_array
            return cv2.imencode('.jpg', image)[1].tobytes()

        if self.is_opencv:
            if self.camera.isOpened():
                _, frame = self.camera.read()
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
                # Toggle the comments to enable/disable object detection
                # image = detect_common_objects(rotated_frame)
                image = rotated_frame
                return cv2.imencode('.jpg', image)[1].tobytes()

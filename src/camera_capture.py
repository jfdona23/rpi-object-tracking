"""
Capture video from camera
"""
import cv2

from object_detection import detect_common_objects


class CameraCapture:
    """Camera Capture"""

    def __init__(self):
        """Init"""

        self.camera = = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise IOError("Could not open Camera")

    def close_camera(self):
        """Close the camera"""

        self.camera.release()

    def get_frame(self):
        """Get a frame
        
        Returns:
            - (array): A numpy array containing a image frame
        """
        
        if self.camera.isOpened():
            _, frame = camera.read()
            # image = detect_common_objects(frame)
            return frame
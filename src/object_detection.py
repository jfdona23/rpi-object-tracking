"""
Objects Detection
"""
import cvlib as cv

from cvlib.object_detection import draw_bbox
from cvlib.utils import cv2

def detect_common_objects(image):
    """Detects common objects

    Args:
        - img (array): Image to parse in a Numpy array form

    Returns:
        - image: A parsed image with the identified objects
    """

    bbox, label, conf = cv.detect_common_objects(image, confidence=0.25, model="yolov4-tiny")
    output_image = draw_bbox(image, bbox, label, conf)

    return output_image

def image_encode(image):
    """Image to Numpy Array"""

    return cv2.imencode(image, 1)

def image_decode(image):
    """Numpy Array to Image"""

    return cv2.imdecode(image, 1)
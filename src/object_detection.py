"""
Object Detection
"""
import cvlib as cv

from cvlib.object_detection import draw_bbox


def detect_common_objects(image):
    """Detects common objects"""

    bbox, label, conf = cv.detect_common_objects(image, confidence=0.25, model="yolov4-tiny")
    output_image = draw_bbox(image, bbox, label, conf)

    return output_image

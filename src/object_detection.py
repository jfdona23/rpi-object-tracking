"""
Objects Detection
"""
import cvlib as cv
from cvlib.object_detection import draw_bbox

def detect_common_objects(img):
    """Detects common objects

    Args:
        - img (image): Image to parse

    Returns:
        - image: A parsed image with the identified objects
    """

    bbox, label, conf = cv.detect_common_objects(img)
    output_image = draw_bbox(img, bbox, label, conf)

    return output_image

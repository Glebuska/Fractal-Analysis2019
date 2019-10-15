import cv2

import converter_types


def convert(image, type):
    if type == converter_types.GrayScale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif type == converter_types.RGB_Red:
        image = image[:, :, 2]
    elif type == converter_types.RGB_Green:
        image = image[:, :, 1]
    elif type == converter_types.RGB_Blue:
        image = image[:, :, 0]
    elif type == converter_types.HSV_Hue:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = hsv_image[:, :, 0]
    else:
        raise Exception("Incorrect converter type")

    return image

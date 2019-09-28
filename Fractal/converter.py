import cv2

from converter_types import ConverterType


def convertPixel(image, type):

    if type == ConverterType.GrayScale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif type == ConverterType.RGB_Red:
        image[:, :, 0] = image[:, :, 1] = 0
    elif type == ConverterType.RGB_Green:
        image[:, :, 0] = image[:, :, 2] = 0
    elif type == ConverterType.RGB_Blue:
        image[:, :, 1] = image[:, :, 2] = 0
    elif type == ConverterType.HSV_Hue:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = hsv_image[:, :, 0]
    else:
        raise Exception("Incorrect converter type")

    return image

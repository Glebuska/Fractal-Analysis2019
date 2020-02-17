import cv2
import numpy as np

from converter_types import ConverterType

print(ConverterType.GrayScaleCV.value)

def convert(image, type):
    if type == ConverterType.GrayScaleCV.value:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif type == ConverterType.RGB_Red.value:
        image = image[:, :, 2]
    elif type == ConverterType.RGB_Green.value:
        image = image[:, :, 1]
    elif type == ConverterType.RGB_Blue.value:
        image = image[:, :, 0]
    elif type == ConverterType.HSV_Hue.value:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = hsv_image[:, :, 0]
    elif type == ConverterType.GrayScaleMid.value:
        image = (np.int32(image[:, :, 0]) + image[:, :, 1] + image[:, :, 2]) // 3
    else:
        raise Exception("Incorrect converter type")

    return image

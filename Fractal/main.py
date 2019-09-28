import cv2
import os
from converter import convertPixel
from converter_types import ConverterType

inputDirectory = "C:\Pictures"
inputFile = "roses.jpg"
outputDirectory = "C:\Pictures"
outputFile = "converted_image.png"


def main():
    try:
        input_type = int((input("Enter converter type: ")))
    except ValueError:
        print("Not a number")
        return

    path = os.path.join(inputDirectory, inputFile)
    converter = ConverterType(input_type)
    img = cv2.imread(path, -1)

    converted_image = convertPixel(path, converter)

    cv2.imshow('result', converted_image)
    cv2.waitKey(0)
    cv2.imwrite(os.path.join(outputDirectory, outputFile), converted_image)
    cv2.destroyAllWindows()


main()

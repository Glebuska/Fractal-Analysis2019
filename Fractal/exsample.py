import cv2
import os
from converter_types import ConverterType
from converter import convertPixel
from LayersBuilder import LayersBuilder

inputDirectory = "C:\Pictures"
inputFile = "roses.jpg"
path = os.path.join(inputDirectory, inputFile)
img = cv2.imread(path, 1)
print(img[1, 1])
img = convertPixel(img, ConverterType.GrayScale)
print(img[1, 1])

layersBuilder = LayersBuilder()
someInterval = layersBuilder.getSingularityBounds(img, 1)
print()






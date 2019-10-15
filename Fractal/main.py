import cv2
import os
import time

import converter_types
from layers_builder import LayersBuilder

import converter


def main():
    inputDirectory = "C:\Pictures"
    inputFile = "paris.jpg"
    path = os.path.join(inputDirectory, inputFile)
    img = cv2.imread(path, 1)
    image = converter.convert(img, converter_types.GrayScale)
    layersBuilder = LayersBuilder(image)
    start_time = time.time()
    someInterval = layersBuilder.getSingularityBounds()
    print("--- %s seconds ---" % (time.time() - start_time))


main()

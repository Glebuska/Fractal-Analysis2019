import cv2
import os
import time
import numpy as np

import converter_types
from layers_builder import LayersBuilder
from spectrum_builder import SpectrumBuilder

import converter


def main():
    inputDirectory = "C:\Pictures"
    inputFile = "2.jpg"
    path = os.path.join(inputDirectory, inputFile)
    img = cv2.imread(path, 1)
    convert_image = converter.convert(img, converter_types.GrayScale)

    layersBuilder = LayersBuilder(convert_image)

    singularityBounds = layersBuilder.get_singularity_bounds()

    layers = layersBuilder.split_by_layers(singularityBounds, 0.2)

    spectrum_builder = SpectrumBuilder(img)

    spectrum = spectrum_builder.calculate_spectrum(layers, singularityBounds, 0.2)

    print(spectrum)


main()

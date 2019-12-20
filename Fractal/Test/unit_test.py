import os
import unittest
import cv2
import math

import converter
import converter_types
from layers_builder import LayersBuilder


class MyTestCase(unittest.TestCase):
    inputDirectory = "C:\Pictures"
    inputFile = "2.jpg"
    path = os.path.join(inputDirectory, inputFile)
    img = cv2.imread(path, 1)

    converted_image = converter.convert(img, converter_types.GrayScaleMid)

    layersBuilder = LayersBuilder(converted_image)
    layersBuilder.calculate_density()
    Densities = layersBuilder.Densities

    def test_intensity_converter(self):
        self.assertTrue(self.converted_image[0, 0] == 27)
        self.assertTrue(self.converted_image[209, 0] == 97)
        self.assertTrue(self.converted_image[209, 207] == 189)
        self.assertTrue(self.converted_image[0, 207] == 187)

    def test_calculate_density(self):
        self.assertTrue(math.isclose(self.Densities[0, 0], 1.913537, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[209, 0], 2.018651, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[0, 207], 1.301924, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[209, 207], 1.572659, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[134, 146], 1.787388, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[108, 140], 1.504346, rel_tol=1e-5))

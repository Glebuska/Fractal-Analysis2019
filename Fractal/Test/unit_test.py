import os
import unittest
import cv2
import math

import numpy as np

import converter
import converter_types
from layers_builder import LayersBuilder


class MyTestCase(unittest.TestCase):
    inputDirectory = "C:\Pictures"
    inputFile = "2.jpg"
    path = os.path.join(inputDirectory, inputFile)
    img = cv2.imread(path, 1)

    converted_image = converter.convert(img, converter_types.ConverterType.GrayScaleMid.value)
    windows = np.array([2, 3, 4, 5, 7])

    layers_builder = LayersBuilder(converted_image, windows)
    Densities = layers_builder.calculate_density()
    singularity_bounds = layers_builder.get_singularity_bounds(Densities)

    def test_intensity_converter(self):
        self.assertTrue(self.converted_image[0, 0] == 27)
        self.assertTrue(self.converted_image[209, 0] == 97)
        self.assertTrue(self.converted_image[209, 207] == 189)
        self.assertTrue(self.converted_image[0, 207] == 187)

    def test_calculate_density(self):
        # window = np.array([2, 3, 4, 5, 7])
        # densities with max window size
        # x = np.log(2 * window + 1); y = np.log(intensity + 1)
        self.assertTrue(math.isclose(self.Densities[0, 0], 1.955013, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[195, 0], 3.06910, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[195, 193], 2.47862, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[0, 193], 2.26545, rel_tol=1e-5))

        self.assertTrue(math.isclose(self.Densities[134, 146], 1.65610, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.Densities[108, 140], 2.01141, rel_tol=1e-5))

    def test_max_min_density(self):
        self.assertTrue(math.isclose(self.singularity_bounds.begin, 0.76878, rel_tol=1e-5))
        self.assertTrue(math.isclose(self.singularity_bounds.end, 3.93179, rel_tol=1e-5))

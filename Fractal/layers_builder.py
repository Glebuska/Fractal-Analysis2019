import numpy as np
from scipy import ndimage

from least_squares import apply_method
from layers import Layer
from structures import *


class LayersBuilder:

    def __init__(self, img, windows):
        self.image = img
        self.windows = windows
        self.max_window_size = windows[-1]
        self.height = img.shape[0] - self.max_window_size * 2
        self.width = img.shape[1] - self.max_window_size * 2

    # <summary>
    # Определение границ сингулярности изображения
    # </summary>
    # <returns>Интервал сингулярностей изображения</returns>

    @staticmethod
    def get_singularity_bounds(density_values):

        return Interval(np.amin(density_values), np.amax(density_values))

    # /// <summary>
    # /// Определение множеств уровня исходного изображения
    # /// </summary>
    # /// <param name="singularity_bounds">Интервал сингулярности</param>
    # /// <param name="singularity_step">Шаг сингулярности</param>
    # /// <param name="density_values">Матрица плотности</param>
    # /// <returns>Список слоёв, каждый из которых - список точек</returns>

    def split_by_layers(self, singularity_bounds, singularity_step, density_values):
        layers = list()
        sin = singularity_bounds.begin
        while sin <= singularity_bounds.end:
            layerSingularity = Interval(sin, sin + singularity_step)

            points = list()

            for i in range(0, self.height):
                for j in range(0, self.width):
                    if sin <= density_values[i, j] < sin + singularity_step:
                        points.append(Point(i, j))

            layers.append(Layer(points, layerSingularity))

            sin += singularity_step
        return layers

    def calculate_density(self):
        densities = np.array([[None] * self.width] * self.height)
        base_height, base_width = self.image.shape
        intensities = np.zeros((len(self.windows), base_height, base_width), np.float)

        for i, win_size in enumerate(self.windows):
            kernel_size = win_size * 2 + 1
            kernel = np.ones((kernel_size, kernel_size))
            intensities[i] = np.log(ndimage.convolve(self.image, kernel, mode='constant') + 1)

        x = np.log(2 * self.windows + 1)

        for i in range(self.max_window_size, self.height + self.max_window_size):
            for j in range(self.max_window_size, self.width + self.max_window_size):
                point = Point(i, j)
                y = intensities[:, i, j]
                density = apply_method(list(zip(x, y)))
                densities[point.x - self.max_window_size, point.y - self.max_window_size] = density

        return densities

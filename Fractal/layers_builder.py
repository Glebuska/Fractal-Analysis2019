import numpy as np

from least_squares import apply_method
from layers import Layer
from structures import *


class LayersBuilder:

    max_window_size = 7

    def __init__(self, img):
        self.image = img
        self.height = img.shape[0] - self.max_window_size * 2
        self.width = img.shape[1] - self.max_window_size * 2

    # <summary>
    # Определение границ сингулярности изображения
    # </summary>
    # <returns>Интервал сингулярностей изображения</returns>

    @staticmethod
    def get_singularity_bounds(densityValues):
        return Interval(np.amin(densityValues), np.amax(densityValues))

    # /// <summary>
    # /// Определение множеств уровня исходного изображения
    # /// </summary>
    # /// <param name="singularityBounds">Интервал сингулярности</param>
    # /// <param name="singularityStep">Шаг сингулярности</param>
    # /// <returns>Список слоёв, каждый из которых - список точек</returns>

    # Interval singularityBounds, double singularityStep
    def split_by_layers(self, singularityBounds, singularityStep, densityValues):
        layers = list()
        sin = singularityBounds.begin
        while sin <= singularityBounds.end:
            layerSingularity = Interval(sin, sin + singularityStep)

            points = list()

            for i in range(0, self.height):
                for j in range(0, self.width):
                    if sin <= densityValues[i, j] < sin + singularityStep:
                        points.append(Point(i, j))

            layers.append(Layer(points, layerSingularity))

            sin += singularityStep
        return layers

    # /// <summary>
    # /// Вычисление функции плотности для всех точек изображения
    # /// </summary>
    # /// <returns>Матрица плотности</returns>

    def calculate_density(self):
        width = self.width
        height = self.height
        densities = np.array([[None] * width] * height)
        for i in range(self.max_window_size, height + self.max_window_size):
            for j in range(self.max_window_size, self.width + self.max_window_size):
                point = Point(i, j)
                density = self.__calculate_density_in_point(point)
                densities[point.x - self.max_window_size, point.y - self.max_window_size] = density

        return densities

    # /// <summary>
    # /// Вычисление функции плотности в окрестности данной точки
    # /// </summary>
    # /// <param name="point">Координаты точки</param>
    # /// <returns>Значение функции плотности в окрестности данной точки</returns>

    def __calculate_density_in_point(self, point):
        window = np.array([2, 3, 4, 5, 7])
        intensity = np.array(self.__calculate_intensity(point, window))
        x = np.log(2 * window + 1)
        y = np.log(intensity + 1)
        return apply_method(list(zip(x, y)))

    # /// <summary>
    # /// Вычисление суммарной интенсивности пикселей в прямоугольнике
    # /// </summary>
    # /// <param name="point">Цетральная точка области</param>
    # /// <param name="windowSize">Размер окна</param>
    # /// <returns>Cуммарная интенсивность пикселей в области</returns>

    def __calculate_intensity(self, point, windowSizes):
        intensities = list()
        img = self.image
        for window in windowSizes:
            intensity = np.sum(img[(point.x - window):(point.x + window + 1), (point.y - window):(point.y + window + 1)])
            intensities.append(intensity)
        return intensities

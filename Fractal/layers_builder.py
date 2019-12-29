import math

import numpy as np

from least_squares import apply_method
from layers import Layer
from structures import *


class LayersBuilder:

    def __init__(self, img):
        self.image = img
        self.height = img.shape[0]
        self.width = img.shape[1]

    # Двумерный массив плотности
    Densities = np.array([])

    # <summary>
    # Определение границ сингулярности изображения
    # </summary>
    # <returns>Интервал сингулярностей изображения</returns>

    def get_singularity_bounds(self):
        # заполняем матрицу плотности
        self.calculate_density()

        densityValues = self.Densities
        return Interval(np.amin(densityValues), np.amax(densityValues))

    # /// <summary>
    # /// Определение множеств уровня исходного изображения
    # /// </summary>
    # /// <param name="singularityBounds">Интервал сингулярности</param>
    # /// <param name="singularityStep">Шаг сингулярности</param>
    # /// <returns>Список слоёв, каждый из которых - список точек</returns>

    # Interval singularityBounds, double singularityStep
    def split_by_layers(self, singularityBounds, singularityStep):
        layers = list()
        sin = singularityBounds.begin
        while sin <= singularityBounds.end:
            layerSingularity = Interval(sin, sin + singularityStep)

            points = list()

            for i in range(0, self.height):
                for j in range(0, self.width):
                    if sin <= self.Densities[i, j] < sin + singularityStep:
                        points.append(Point(i, j))

            layers.append(Layer(points, layerSingularity))

            sin += singularityStep
        return layers

    # /// <summary>
    # /// Вычисление функции плотности для всех точек изображения
    # /// </summary>

    def calculate_density(self):
        self.Densities = np.array([[None] * self.width] * self.height)
        for i in range(0, self.height):
            for j in range(0, self.width):
                point = Point(i, j)
                density = self.__calculate_density_in_point(point)
                self.Densities[i, j] = density

    # /// <summary>
    # /// Вычисление функции плотности в окрестности данной точки
    # /// </summary>
    # /// <param name="point">Координаты точки</param>
    # /// <returns>Значение функции плотности в окрестности данной точки</returns>

    def __calculate_density_in_point(self, point):
        points = list()
        window = [2, 3, 4, 5, 7]  # максимальный размер окна?
        intensity = self.__calculate_intensity(point, window)

        for i in range(0, len(window)):
            x = math.log(window[i])
            y = math.log(intensity[i] + 1)
            cord = (x, y)
            points.append(cord)
        return apply_method(points)

    # /// <summary>
    # /// Вычисление суммарной интенсивности пикселей в прямоугольнике
    # /// </summary>
    # /// <param name="point">Цетральная точка области</param>
    # /// <param name="windowSize">Размер окна</param>
    # /// <returns>Cуммарная интенсивность пикселей в области</returns>

    def __calculate_intensity(self, point, windowSizes):
        intensities = list()

        for window in windowSizes:
            intensity = 0
            start_x_coord = max(0, point.x - window) # не позволяет получить отриц значение
            end_x_coord = min(point.x + window, self.height - 1)
            start_y_coord = max(0, point.y - window)
            end_y_coord = min(point.y + window, self.width - 1)

            for i in range(start_x_coord, end_x_coord + 1):
                for j in range(start_y_coord, end_y_coord + 1):
                    intensity += self.image[i, j]

            intensities.append(intensity)

        return intensities

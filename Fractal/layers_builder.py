import math

import numpy as np

from least_squares import applyMethod
from layers import Layer
from structures import *


class LayersBuilder:

    def __init__(self, img):
        self.image = img
        self.width = img.shape[0]
        self.height = img.shape[1]

    # Двумерный массив плотности
    __Densities = np.array([])

    # <summary>
    # Определение границ сингулярности изображения
    # </summary>
    # <param name="image">Анализируемое изображение</param>
    # <param name="converterType">Тип конвертера</param>
    # <returns>Интервал сингулярностей изображения</returns>

    def getSingularityBounds(self):
        # заполняем матрицу плотности
        self.__calculateDensity()

        densityValues = self.__Densities
        return Interval(np.amin(densityValues), np.amax(densityValues))

    # /// <summary>
    # /// Определение множеств уровня исходного изображения
    # /// </summary>
    # /// <param name="singularityBounds">Интервал сингулярности</param>
    # /// <param name="singularityStep">Шаг сингулярности</param>
    # /// <returns>Список слоёв, каждый из которых - список точек</returns>

    # Interval singularityBounds, double singularityStep
    def splitByLayers(self, singularityBounds, singularityStep):
        layers = list()
        sin = singularityBounds.Begin
        while sin <= singularityBounds.End:
            layerSingularity = Interval(sin, sin + singularityStep)

            points = list()

            for i in range(0, self.height):
                for j in range(0, self.width):
                    if sin <= self.__Densities[i, j] < sin + singularityStep:
                        points.append(Point(i, j))

            layers.append(Layer(points, layerSingularity))

            sin += singularityStep
        return layers

    # /// <summary>
    # /// Вычисление функции плотности для всех точек изображения
    # /// </summary>

    def __calculateDensity(self):
        self.__Densities = np.array([[None] * self.width] * self.height)
        for i in range(0, self.height):
            for j in range(0, self.width):
                point = Point(i, j)
                density = self.__calculateDensityInPoint(point)
                self.__Densities[i, j] = density

    # /// <summary>
    # /// Вычисление функции плотности в окрестности данной точки
    # /// </summary>
    # /// <param name="point">Координаты точки</param>
    # /// <returns>Значение функции плотности в окрестности данной точки</returns>

    def __calculateDensityInPoint(self, point):
        points = list()
        window = [2, 3, 4, 5, 6, 7]  # максимальный размер окна?
        densitys_in_point = self.__calculateIntensity(point, window)

        for i in range(0, len(window)):
            x = math.log(2 * window[i] + 1)
            y = math.log(densitys_in_point[i] + 1)
            cord = (x, y)
            points.append(cord)
        return applyMethod(points)

    # /// <summary>
    # /// Вычисление суммарной интенсивности пикселей в прямоугольнике
    # /// </summary>
    # /// <param name="point">Цетральная точка области</param>
    # /// <param name="windowSize">Размер окна</param>
    # /// <returns>Cуммарная интенсивность пикселей в области</returns>

    def __calculateIntensity(self, point, windowSizes):
        intensity = list()

        for window in windowSizes:
            intensivity = 0
            start_x_coord = max(0, point.x - window) # не позволяет получить отриц значение
            end_x_coord = min(point.x + window, self.width)
            start_y_coord = max(0, point.y - window)
            end_y_coord = min(point.y + window, self.height)

            for i in range(start_x_coord, end_x_coord):
                for j in range(start_y_coord, end_y_coord):
                    intensivity += self.image[i, j]

            intensity.append(intensivity)

        return intensity

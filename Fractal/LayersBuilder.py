import cv2
import numpy as np
import math
from LeastSquares import LeastSquares
from Structures import *
from Layers import Layer
import time

# Самая главная проблема может быть в приведении типов и потери точности, так как
# я пока не очень понимаю, как тут все устроено и нет Double.


class LayersBuilder:
    # какая-то константа будет, но вот на сколько большая
    # надо будет решать
    def __init__(self):
        pass


    # Двумерный массив плотности
    __Densities = np.array([])

    # Двумерный массив интенсивности
    __Intensity = np.array([])

    # <summary>
    # Определение границ сингулярности изображения
    # </summary>
    # <param name="image">Анализируемое изображение</param>
    # <param name="converterType">Тип конвертера</param>
    # <returns>Интервал сингулярностей изображения</returns>

    def getSingularityBounds(self, image, converterType):
        # shape[0] - строка, shape[1] - столбец
        # надо проверить!: в Python нет double, хватит ли float?
        self.__Intensity = np.zeros((image.shape[0], image.shape[1]), float)

        # заполняем матрицу интенсивности

        self.calculateIntensities(image, converterType)

        # заполняем матрицу плотности
        start_time = time.time()
        self.__calculateDensity(image)
        print("--- %s seconds ---" % (time.time() - start_time))

        densityValues = self.__Densities
        return Interval(np.amax(densityValues), np.amin(densityValues))

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
            width = self.__Densities.shape[0]
            height = self.__Densities.shape[1]

            for i in range(0, width):
                for j in range(0, height):
                    if sin <= self.__Densities[i, j] < sin + singularityStep:
                        points.append(Point(i, j))

            layers.append(Layer(points, layerSingularity))

            sin += singularityStep
        return layers

    # /// <summary>
    # /// Вычисление функции плотности для всех точек изображения
    # /// </summary>

    def __calculateDensity(self, image):
        start_time = time.time()
        width = self.__Intensity.shape[0]
        height = self.__Intensity.shape[1]

        self.__Densities = np.array([[None] * width] * height)
        for i in range(0, height):
            for j in range(0, width):
                point = Point(i, j)
                density = self.__calculateDensityInPoint(point, image)
                self.__Densities[point.x, point.y] = density
        print("--- %s seconds of __calculateIntensity ---" % (time.time() - start_time))

    # /// <summary>
    # /// Вычисление функции плотности в окрестности данной точки
    # /// </summary>
    # /// <param name="point">Координаты точки</param>
    # /// <returns>Значение функции плотности в окрестности данной точки</returns>

    def __calculateDensityInPoint(self, point, image):
        points = list()
        window = [7, 5, 4, 3, 2]
        intens = self.__calculateIntensity(point, window, image)
        for windowSize in window:
            i = 0
            x = math.log2(2 * windowSize + 1)
            y = math.log2(intens[i] + 1)
            cord = (x, y)
            points.append(cord)
            i += 1
        return LeastSquares.applyMethod(points)

    # /// <summary>
    # /// Вычисление интенсивности пикселя
    # /// </summary>
    # /// <param name="pixel">Пиксель изображения</param>
    # /// <param name="converterType">Тип конвертера</param>
    # /// <returns>Интенсивность пикселя</returns>

    @staticmethod
    def __getIntensityFromPixel(pixel, converterType):
        # 1 == GrayScale, 5 == HSV_Hue. Конвертер преобразовывает матрицу, усредняя
        # пиксели, поэтому возвращаем просто само значение.
        #---------------------------------------------------------------------------------
        # Есть предложение сразу в конвертере сразу матрицу преобразовывать и тогда мы сможем
        # избавиться от этой функции и не передавать постоянно converterType, но не понятно,
        # как дорого/дешево по ресурсам это будет обходиться и есть ли в этом смысл в принципе.
        if converterType == 1 or converterType == 5:
            return pixel
        elif converterType == 2:
            return pixel[0]
        elif converterType == 3:
            return pixel[1]
        else:
            return pixel[2]

    @staticmethod
    def __makeZeroBorder(param):
        if param < 0:
            return 0

    # /// <summary>
    # /// Вычисление интенсивности пикселей анализируемого изображения
    # /// </summary>
    # /// <param name="image">Анализируемое изображение</param>
    # /// <param name="converterType">Тип конвертера</param>

    def calculateIntensities(self, img, converterType):
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                pixel = img[i][j]
                intensity = self.__getIntensityFromPixel(pixel, converterType)
                self.__Intensity[i, j] = intensity

    # /// <summary>
    # /// Вычисление суммарной интенсивности пикселей в прямоугольнике
    # /// </summary>
    # /// <param name="point">Цетральная точка области</param>
    # /// <param name="windowSize">Размер окна</param>
    # /// <returns>Cуммарная интенсивность пикселей в области</returns>

    def __calculateIntensity(self, point, windowSizes, image):
        # При обрезании картинки выходить за положительную границу можно,
        # происходит обычное приравнивание к размеру картинки, при отрицательном числе к 0 не
        # приравнивает, поэтому пришлось делать 0
        intensity = list()
        maxWindowSize = windowSizes[0]
        crop_img = image[self.__makeZeroBorder(point.x - maxWindowSize): point.x + maxWindowSize,
                   self.__makeZeroBorder(point.y - maxWindowSize): point.y + maxWindowSize]
        integral_matrix = cv2.integral(crop_img)
        for i in windowSizes:
            intensity.append(integral_matrix[integral_matrix.shape[0] - 1, integral_matrix.shape[1] - i + 1])
        return intensity

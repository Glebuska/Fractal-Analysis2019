import cv2
import math
import os

import numpy as np

import least_squares


class SpectrumBuilder:

    def __init__(self, img):
        self.image = img
        self.height = img.shape[0]
        self.width = img.shape[1]

    #    /// <summary>
    #    /// Вычисление мультифрактального спектра: создание уровней и измерение их размерности
    #    /// </summary>
    #    /// <param name="image">Анализируемое изображение</param>
    #    /// <param name="layers">Множества уровня</param>
    #    /// <param name="singularityBounds">Интервал сингулярности</param>
    #    /// <param name="singularityStep">Шаг сингулярности</param>
    #    /// <returns>Мультифракальный спектр изображения</returns>

    def calculate_spectrum(self, layers, singularityBounds, singularityStep):
        currentLayerSingularity = singularityBounds.begin
        spectrum = dict()

        for layer in layers:
            measure = self.__create_and_measure_layer(layer)
            spectrum[currentLayerSingularity] = measure
            currentLayerSingularity += singularityStep
        return spectrum

    # /// <summary>
    # /// Создание изображения, соответствующего данному уровню, и его измерение
    # /// </summary>
    # /// <param name="image">Анализируемое изображение</param>
    # /// <param name="layer">Множество уровня</param>
    # /// <returns>Изображение слоя и его фрактальная размерность</returns>

    def __create_and_measure_layer(self, layer):

        layer_image = 255 * np.ones(shape=[self.height, self.width, 3], dtype=np.uint8)

        for point in layer.Points:
            layer_image[point.x, point.y] = (0, 0, 0)
        self.__save_layer_image(layer, layer_image)
        return self.__calculate_measure(layer_image)

    # /// <summary>
    # /// Сохранение изображения множества уровня
    # /// </summary>
    # /// <param name="layer">Множество уровня</param>
    # /// <param name="layerImage">Изображение множества уровня</param>

    @staticmethod
    def __save_layer_image(layer, layerImage):
        min_singularity = str(round(layer.SingularityBounds.begin, 2))
        max_singularity = str(round(layer.SingularityBounds.end, 2))

        layer_name = str.join(" ", ["layer", min_singularity, max_singularity, ".jpg"])
        path_to_image = "C:\Pictures"
        abs_path = os.path.join(path_to_image, layer_name)

        cv2.imwrite(abs_path, layerImage)

    # /// <summary>
    # /// Вычисление фрактальной размерности изображения
    # /// </summary>
    # /// <param name="image">Анализируемое изображение</param>
    # /// <returns>Фрактальная размерность изображения</returns>

    def __calculate_measure(self, layers_img):

        points = list()
        windows = {2, 3, 4, 5, 6, 7}
        for window in windows:
            intensities = self.__calculate_black_windows(layers_img, window)
            x = math.log(1.0 / window)
            y = math.log(intensities + 1)
            points.append((x, y))

        return max(0.0, least_squares.apply_method(points))

    # /// <summary>
    # /// Подсчёт числа квадратиков, имеющих внутри себя хотя бы один чёрный пиксель
    # /// </summary>
    # /// <param name="image">Исследуемая область изображения</param>
    # /// <param name="window">Размер окна</param>
    # /// <returns>Число квадратиков, имеющих внутри себя хотя бы один чёрный пиксель </returns>

    def __calculate_black_windows(self, layers_img, window):
        black_windows = 0

        for i in range(0, self.height - window, window):
            for j in range(0, self.width - window, window):
                if self.__has_black_pixel(layers_img, i, j, window):
                    black_windows += 1

        return black_windows

    @staticmethod
    def __has_black_pixel(layers_img, start_x, start_y, window):
        for i in range(start_x, start_x + window):
            for j in range(start_y, start_y + window):
                color = layers_img[i, j]
                if color[0] == color[1] == color[2] == 0:
                    return True

        return False

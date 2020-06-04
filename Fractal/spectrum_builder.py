import cv2
import math
import os

import numpy as np
from scipy import ndimage

import least_squares


class SpectrumBuilder:

    def __init__(self, img, path, windows):
        self.image = img
        self.windows = windows
        self.max_window_size = windows[-1]
        self.height = img.shape[0]
        self.width = img.shape[1]
        self.path = path

    list_images = list()

    #    /// <summary>
    #    /// Вычисление мультифрактального спектра: создание уровней и измерение их размерности
    #    /// </summary>
    #    /// <param name="layers">Множества уровня</param>
    #    /// <param name="singularity_bounds">Интервал сингулярности</param>
    #    /// <param name="singularity_step">Шаг сингулярности</param>
    #    /// <returns>Мультифракальный спектр изображения</returns>

    def calculate_spectrum(self, layers, singularity_bounds, singularity_step):
        current_layer_singularity = singularity_bounds.begin
        spectrum = dict()

        for layer in layers:
            measure = self.__create_and_measure_layer(layer)
            spectrum[current_layer_singularity] = measure
            current_layer_singularity += singularity_step
        return spectrum

    # /// <summary>
    # /// Создание изображения, соответствующего данному уровню, и его измерение
    # /// </summary>
    # /// <param name="layer">Множество уровня</param>
    # /// <returns>Изображение слоя и его фрактальная размерность</returns>

    def __create_and_measure_layer(self, layer):
        new_height = self.height - self.max_window_size * 2
        new_width = self.width - self.max_window_size * 2
        layer_image = 255 * np.ones(shape=[new_height, new_width, 3], dtype=np.uint16)
        revers_layer_image = np.zeros(shape=[new_height, new_width], dtype=np.uint16)

        for point in layer.points:
            layer_image[point.x, point.y] = (0, 0, 0)
            revers_layer_image[point.x, point.y] = 1

        self.__save_layer_image(layer, layer_image)
        return self.__calculate_measure(revers_layer_image)

    # /// <summary>
    # /// Сохранение изображения множества уровня
    # /// </summary>
    # /// <param name="layer">Множество уровня</param>
    # /// <param name="layer_image">Изображение множества уровня</param>

    def __save_layer_image(self, layer, layer_image):
        self.list_images.append(layer_image)
        min_singularity = str(round(layer.singularity_bounds.begin, 2))
        max_singularity = str(round(layer.singularity_bounds.end, 2))
        layer_name = "layer(" + min_singularity + "-" + max_singularity + ")" + ".jpg"
        abs_path = os.path.join(self.path, layer_name)

        cv2.imwrite(abs_path, layer_image)

    # /// <summary>
    # /// Вычисление фрактальной размерности изображения
    # /// </summary>
    # /// <param name="revers_image">Анализируемое изображение</param>
    # /// <returns>Фрактальная размерность изображения</returns>

    def __calculate_measure(self, revers_img):
        intensities = self.__calculate_black_windows_convolve(revers_img, self.windows)
        x = np.log(self.windows)
        y = np.log(intensities + 1)

        return -least_squares.apply_method(list(zip(x, y)))

    # /// <summary>
    # /// Подсчёт числа квадратов, имеющих внутри себя хотя бы один чёрный пиксель
    # /// </summary>
    # /// <param name="layers_image">Исследуемая область изображения</param>
    # /// <param name="windows">Список окон</param>
    # /// <returns>Число квадратиков, имеющих внутри себя хотя бы один чёрный пиксель </returns>

    def __calculate_black_windows_convolve(self, layers_img, windows):
        black_windows_list = np.zeros(len(windows))
        new_height = self.height - self.max_window_size * 2
        new_width = self.width - self.max_window_size * 2

        black_pixels = np.zeros((len(windows), new_height, new_width), np.float)
        for i, win_size in enumerate(windows):
            kernel_size = win_size * 2 - 1
            kernel = [[1 if i < win_size and j < win_size else 0
                       for i in range(0, kernel_size)] for j in range(0, kernel_size)]
            black_pixels[i] = ndimage.convolve(layers_img, kernel, mode='constant')

        for k, window in enumerate(windows):
            count_black_pixel = 0
            for i in range(0, new_height - window, window):
                for j in range(0, new_width - window, window):
                    if black_pixels[k][i][j]:
                        count_black_pixel += 1
            black_windows_list[k] = count_black_pixel

        return black_windows_list

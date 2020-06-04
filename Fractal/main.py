import cv2
import os
import time

import numpy as np

from layers_builder import LayersBuilder
from spectrum_builder import SpectrumBuilder

from converter import convert

inputDirectory = r"C:\Pictures"
dir_list = os.listdir(inputDirectory)
directories = list(filter(lambda x: "Layers " in x, dir_list))


def create_directory():
    length = len(directories)
    if length > 0:
        directories.sort()
        num_of_directory = int(directories[-1][-1]) + 1
        new_dir = os.path.join(inputDirectory, "Layers " + str(num_of_directory))
        path = os.path.join(inputDirectory, new_dir)
        os.mkdir(path=path)
        return path
    else:
        new_dir = os.path.join(inputDirectory, "Layers 0")
        path = os.path.join(inputDirectory, new_dir)
        os.mkdir(path=path)
        return path


def main():
    print("Создайте папку C:\\Pictures, сохраните в ней тестовое изображение\n"
          "В этой же папке будут сохранены изображения, соответствующие множествам уровня")
    print("Введите имя файла, например img.jpg")
    print("Если вы хотите использовать другой путь, введите его целиком в формате "
          "C:\\test\image1.jpg")
    input_data = input()
    if ":" in input_data:
        img = cv2.imread(input_data, 1)
    else:
        path = os.path.join(inputDirectory, input_data)
        img = cv2.imread(path, 1)

    if img is None:
        print("Неверная загрузка картинки, проверьте входные данные")
        return

    print("Введите номер желаемого алгоритма обработки изображения:")
    print("1) монохромное изображение")
    print("2) красная компонента RGB")
    print("3) зелёная компонента RGB")
    print("4) синяя компонента RGB")
    print("5) компонента Hue палитры HSV")
    print()

    convert_number = input()
    try:
        convert_number = int(convert_number)
    except ValueError:
        raise Exception("Неверный номер алгоритма")

    print("Выберите шаг, например 0.2")
    step = float(input())
    print("Вычисление...")

    converted_image = convert(img, convert_number).astype(np.int64)

    windows = np.array([2, 3, 4, 5, 7])
    layers_builder = LayersBuilder(converted_image, windows)

    density_values = layers_builder.calculate_density()

    singularity_bounds = layers_builder.get_singularity_bounds(density_values)

    layers = layers_builder.split_by_layers(singularity_bounds, step, density_values)

    path_to_directory = create_directory()

    spectrum_builder = SpectrumBuilder(img, path_to_directory, windows)

    spectrum = spectrum_builder.calculate_spectrum(layers, singularity_bounds, step)

    print(spectrum)

    print("Результаты сохранены в исходной папке, доброго дня!")


main()

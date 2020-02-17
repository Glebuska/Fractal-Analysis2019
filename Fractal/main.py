import cv2
import os

from layers_builder import LayersBuilder
from spectrum_builder import SpectrumBuilder

from converter import convert

inputDirectory = "C:\Pictures"


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

    converted_image = convert(img, convert_number)

    layersBuilder = LayersBuilder(converted_image)

    densityValues = layersBuilder.calculate_density()

    singularityBounds = layersBuilder.get_singularity_bounds(densityValues)

    layers = layersBuilder.split_by_layers(singularityBounds, 0.2, densityValues)

    spectrum_builder = SpectrumBuilder(img)

    spectrum = spectrum_builder.calculate_spectrum(layers, singularityBounds, 0.2)
    file = open("guru99.txt", "w+")
    
    print(spectrum)


main()

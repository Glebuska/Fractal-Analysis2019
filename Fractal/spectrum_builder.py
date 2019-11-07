import structures


class SpectrumBuilder:

    #    /// <summary>
    #    /// Вычисление мультифрактального спектра: создание уровней и измерение их размерности
    #    /// </summary>
    #    /// <param name="image">Анализируемое изображение</param>
    #    /// <param name="layers">Множества уровня</param>
    #    /// <param name="singularityBounds">Интервал сингулярности</param>
    #    /// <param name="singularityStep">Шаг сингулярности</param>
    #    /// <returns>Мультифракальный спектр изображения</returns>

    def calculate_spectrum(self, image, layers, singularityBounds, singularityStep): pass

    # /// <summary>
    # /// Создание изображения, соответствующего данному уровню, и его измерение
    # /// </summary>
    # /// <param name="image">Анализируемое изображение</param>
    # /// <param name="layer">Множество уровня</param>
    # /// <returns>Изображение слоя и его фрактальная размерность</returns>

    def __create_and_measure_layer(self, image, layer): pass

    # /// <summary>
    # /// Сохранение изображения множества уровня
    # /// </summary>
    # /// <param name="layer">Множество уровня</param>
    # /// <param name="layerImage">Изображение множества уровня</param>

    def __save_layer_image(self, layer, layerImage): pass



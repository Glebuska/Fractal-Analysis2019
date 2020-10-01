# Research on fractal analysis methods

Supervised by Nataly B. Ampilova

  Тема работы связана с актуальными задачами нахождения классификационных признаков цифровых изображений, обладающих сложной структурой. Такие изображения возникают в самых разных предметных областях, таких как геология (изображения земных ландшафтов), биология (изображения процессов, происходящих в живых клетках), медицина (снимки всевозможных тканей),  техника (изображения срезов металлов). С ростом мощностей аппаратуры сложность  структуры изображений возрастает.
  Под классификационным признаком понимается некоторая числовая характеристика, которая может быть использована для разделения некоторого класса изображений на отдельные смысловые классы, например разделение изображений здоровой костной ткани и ткани с остеопорозом. <br>
Изображения со сложной текстурой часто имеют фрактальную или мультифрактальную структуру. <br>
  Поэтому для их анализа оказываются полезными методы фрактального и мультифрактального анализа. Фрактальный анализ позволяет получить приближенное значение фрактальной размерности исследуемого изображения. Мультифракталы представляют собой сложные объединения нескольких фрактальных множеств, каждое из которых обладает своей фрактальной размерностью. Основной характеристикой мультифрактального множества является мультифрактальный спектр, который представляет собой вектор фрактальных размерностей составляющих его подмножеств.<br>
  Существует несколько методов вычисления спектров.  Любой из них может быть использован для анализа изображений. Мы реализуем метод получения мультифрактального спектра с помощью так называемой локальной функции плотности. Для каждого пикселя изображения вычисляется определенная характеристика (функция плотности), и все изображение разбивается на области, которые содержат пиксели с близкими характеристиками. Фактически, это вариант метода сегментации изображения на фрактальные подмножества (множества уровня). Набор фрактальных размерностей множеств уровня есть мультифрактальный спектр изображения.<br>
  Визуализация множеств уровня позволяет лучше представить разбиение изображения на составляющие его подмножества. Важной особенностью данной реализации является представление изображения в 3D, которое является послойным изображением множеств уровня.<br>

# Примеры

Примеры вы можете [увидеть тут](https://github.com/Glebuska/Fractal-Analysis2019/tree/master/Examples)


# /// <summary>
# /// Уточнение результата вычислений с помощью МНК
# /// </summary>
# /// <param name="points">множество точек и значений в них</param>
# /// <returns>Уточнённое значение</returns>


def applyMethod(points):
    n = len(points)
    x_sum = y_sum = xy_sum = x_sqr_sum = 0
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
        x_sqr_sum = point[0] * point[0]
        xy_sum = point[0] * point[1]
    return (n * xy_sum - x_sum * y_sum) / (n * x_sqr_sum - x_sum * x_sum)

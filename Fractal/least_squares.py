import statistics
# /// <summary>
# /// Уточнение результата вычислений с помощью МНК
# /// </summary>
# /// <param name="points">множество точек и значений в них</param>
# /// <returns>Уточнённое значение</returns>


def apply_method(points):
    n = len(points)
    X = list()
    Y = list()
    for point in points:
        X.append(point[0])
        Y.append(point[1])

    X_mean = statistics.mean(X)
    Y_mean = statistics.mean(Y)

    num = 0
    den = 0
    for i in range(len(points)):
        num += (X[i] - X_mean) * (Y[i] - Y_mean)
        den += (X[i] - X_mean) ** 2
    m = num / den

    x_sum = y_sum = xy_sum = x_sqr_sum = 0
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
        x_sqr_sum += point[0] * point[0]
        xy_sum += point[0] * point[1]
    result = (n * xy_sum - x_sum * y_sum) / (n * x_sqr_sum - x_sum * x_sum)
    return result

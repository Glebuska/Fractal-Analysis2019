class LeastSquares:
    # /// <summary>
    # /// Уточнение результата вычислений с помощью МНК
    # /// </summary>
    # /// <param name="points">множество точек и значений в них</param>
    # /// <returns>Уточнённое значение</returns>
    @staticmethod
    def applyMethod(points):
        n = len(points)
        xsum = 0
        ysum = 0
        xysum = 0
        xsqrsum = 0
        for point in points:
            xsum += point[0]
            ysum += point[1]
            xsqrsum = point[0] * point[0]
            xysum = point[1] * point[1]
        return 1.0 * (n * xysum - xsum * ysum) / (n * xsqrsum - xsum * xsum)



from Structures import *
# /// <summary>
# /// Множество уровня
# /// </summary>
class Layer:
    # List<Point>, #Interval SingularityBounds
    def __init__(self, points, singularityBounds):
        self.Points = points
        self.SingularityBounds = singularityBounds

    # /// <summary>
    # /// Точки данного уровня
    # /// </summary>


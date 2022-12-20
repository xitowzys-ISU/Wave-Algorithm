class Point:
    direction = None
    x = None
    y = None
    weight = None
    previous_point = None

    def __init__(self, x, y, weight=None, previous_point=None, distance=0):
        self.x = x
        self.y = y
        self.weight = weight
        self.previous_point: Point = previous_point
        self.distance = 0

    def __add__(self, other: tuple[int, int]):
        return Point(self.x + other[0], self.y + other[1])

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __lt__(self, other):
        if self.x < other.x:
            return True
        if self.y < other.y:
            return True
        return False

    def __le__(self, other):
        if self.x <= other.x:
            return True
        if self.y <= other.y:
            return True
        return False

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        return Point.calc_euclidean_distance(self, other)

    @staticmethod
    def calc_euclidean_distance(point1, point2):
        return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)**0.5

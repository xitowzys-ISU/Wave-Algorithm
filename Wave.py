import numpy as np
from typing import Any
from Point import Point
from loguru import logger
from queue import PriorityQueue
import matplotlib.pyplot as plt

# The neighborhood of Neumann
neiman_neighborhood: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# The neighborhood of Moore
moore_neighborhood: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1),
                                             (-1, -1), (1, 1), (-1, 1), (1, -1)]


selected_adjacency: list[tuple[int, int]] = moore_neighborhood


class WaveAlgoException(Exception):
    """Wave algorithm. Exception class.
    """
    pass


class WaveAlgo:
    """Wave algorithm.

    Args:
        start (Point): The point to start from.
        finish (Point): Final point.
        neighborhood (str): Neighborhood method (moore, neiman).
    """

    def __init__(self, start: Point, finish: Point, neighborhood: str) -> None:

        if neighborhood.lower() == "neiman":
            self.selected_adjacency: list[tuple[int,
                                                int]] = neiman_neighborhood
        elif neighborhood.lower() == "moore":
            self.selected_adjacency: list[tuple[int, int]] = moore_neighborhood
        else:
            raise WaveAlgoException("The neighborhood is wrong")

        self.start_point: Point = start
        self.finish_point: Point = finish

        self.path: list[Any] = []

    def npy_read_map(self, path: str) -> None:
        """Reading a numpy array.

        Args:
            path (str): Array path.
        """
        with open(path, 'rb') as f:
            self.map_array: np.ndarray[float, float] = np.load(f)

    def search(self) -> None:
        """Search for a way.
        """
        iters: int = 0

        self.distances: Any = np.full(
            self.map_array.shape, 10000000)

        self.visited: Any = np.full(self.map_array.shape, False)

        self.visited[self.start_point.y, self.start_point.x] = True

        q: PriorityQueue[Any] = PriorityQueue()

        q.put((0, self.start_point))

        while not q.empty():
            iters += 1

            weight, cur_point = q.get()
            self.distances[cur_point.y, cur_point.x] = weight

            # If you found a point
            if cur_point.x == self.finish_point.x and cur_point.y == self.finish_point.y:
                logger.success("Finish")
                break

            for a in selected_adjacency:
                next_point: Point = Point(
                    cur_point.x + a[0], cur_point.y + a[1])

                # Leaving the map and point not visited
                if 0 <= next_point.x < self.map_array.shape[1] and 0 <= next_point.y < self.map_array.shape[0] and \
                        not self.visited[next_point.y][next_point.x] and self.map_array[next_point.y][next_point.x] != 1:
                    self.visited[next_point.y][next_point.x] = True

                    new_weight = Point.calc_euclidean_distance(
                        cur_point, next_point)

                    q.put((weight + new_weight, next_point))

                # Leaving the map
                if 0 <= next_point.x < self.map_array.shape[1] and 0 <= next_point.y < self.map_array.shape[0]:

                    # The point has not been visited yet
                    if not self.visited[next_point.y][next_point.x]:

                        # The point is not on the building
                        if self.map_array[next_point.y][next_point.x] != 1:
                            self.visited[next_point.y][next_point.x] = True

            if not iters % 1000:
                logger.debug(f"iter: {iters}")

    def build_way(self) -> list[Any]:
        """Building a way. Bypass from the back side.
        """

        m = np.zeros_like(self.map_array)
        cur_point: Point = Point(self.finish_point.x, self.finish_point.y)
        self.path.append(cur_point)
        iters: int = 0

        while cur_point != self.start_point:
            m[cur_point.y, cur_point.x] = 1
            iters += 1

            possible_points = []
            weights = []

            for a in selected_adjacency:
                new_point: Point = Point(
                    cur_point.x + a[0], cur_point.y + a[1])

                possible_points.append(new_point)
                weights.append(self.distances[new_point.y, new_point.x])

            x = np.argmin(weights)
            new_point = possible_points[x]
            self.path.append(new_point)
            cur_point = new_point

    def render_map(self) -> None:
        """Render a map.
        """
        path_on_map = self.map_array.copy()
        path_on_map *= 0.5

        for p in self.path:
            path_on_map[p.y, p.x] = 1

        plt.imshow(path_on_map)
        plt.show()

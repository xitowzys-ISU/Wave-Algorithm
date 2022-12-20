from Point import Point
from Wave import WaveAlgo

if __name__ == "__main__":
    start: Point = Point(160, 305)
    finish: Point = Point(1285, 690)

    wave: WaveAlgo = WaveAlgo(start=start, finish=finish, neighborhood="Moore")
    wave.npy_read_map('data/binary_map.npy')

    wave.search()
    wave.build_way()
    wave.render_map()

from problems import Location2D
from simulators import ConsoleSimulator


if __name__ == "__main__":
    map_: str = "resources/mazes/warehouse_medium"
    rests: list[Location2D] = [
        Location2D(1, 1),
        Location2D(75, 1),
        Location2D(1, 43),
        Location2D(75, 43),
    ]
    n: int = len(rests)
    ConsoleSimulator(map_, rests).run(n, n)

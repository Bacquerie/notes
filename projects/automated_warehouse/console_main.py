from problems import Location2D
from simulators import ConsoleSimulator


if __name__ == "__main__":
    map_: str = "resources/mazes/warehouse_medium"
    belts: list[Location2D] = [Location2D(1, 22), Location2D(74, 22)]
    rests: list[Location2D] = [
        Location2D(1, 1),
        Location2D(74, 1),
        Location2D(1, 45),
        Location2D(74, 45),
    ]
    n: int = len(rests)
    ConsoleSimulator(map_, belts, rests).run(n, n)

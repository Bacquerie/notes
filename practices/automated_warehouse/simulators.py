import abc
import enum
import itertools
import random
import time

import util
from models import Package
from models import Robot
from problems import Action
from problems import CellType
from problems import Grid2D
from problems import Location2D
from search import MultiPolicy


class Icon(enum.Enum):
    """
    Possible icons appearing in a `Grid2D` map, for `ConsoleSimulator`.
    """

    BELT: str = "🎞️"
    FREE: str = "⬜"
    PACKAGE: str = "📦"
    RACK: str = "🗄️"
    REST: str = "🛋️"
    ROBOT: str = "🤖"
    WALL: str = "🧱"


char_map: dict[str, str] = {
    CellType.BELT.value: Icon.BELT.value,
    CellType.FREE.value: Icon.FREE.value,
    CellType.RACK.value: Icon.RACK.value,
    CellType.WALL.value: Icon.WALL.value,
}


class Simulator(abc.ABC):
    """
    Abstracts the simulator, serving as a base class for distinct types of
    simulation front ends.
    """

    @abc.abstractmethod
    def run(self, n_robots: int = 1, n_packages: int = 1) -> None:
        """
        Runs the simulation using the given number of robots and packages.
        """
        raise NotImplementedError


class ConsoleSimulator(Simulator):
    """
    Implements `Simulator`, printing everything on the console.
    """

    def __init__(
        self,
        map_path: str,
        rests: list[Location2D]
    ) -> None:
        """
        :param map_path: File path of the warehouse layout.
        :param belts: Locations of the conveyor belts.
        :param rests: Resting locations.
        """
        self.map: list[str] = util.read_map(map_path)
        self.belts: list[Location2D] = self._get_cells(CellType.BELT)
        self.rests: list[Location2D] = rests
        # Optimal navigation policy for each conveyor belt.
        self.belt_policies: dict[
            Location2D, dict[Location2D, Action]] = self._get_policies(
            self.belts,
        )
        # Optional navigation policy for each resting location.
        self.rest_policies: dict[
            Location2D, dict[Location2D, Action]] = self._get_policies(
            self.rests,
        )
        # Run-dependent objects.
        self.packages: dict[Package, bool] = {}
        self.robots: list[Robot] = []

    def run(self, n_robots: int = 1, n_packages: int = 1) -> None:
        package_policies: dict[Package, dict[Location2D, Action]] = {}
        self.robots = self._create_robots(n_robots)
        while True:
            # Creates new packages if all previous have been delivered.
            all_free: bool = all(robot.is_free for robot in self.robots)
            if not self.packages and all_free:
                package_policies = self._new_packages(n_packages)
            # Queries all robots to try to make package assignations.
            for robot in self.robots:
                if robot.is_free:
                    # Tries to assign a package.
                    if package := self._get_package(self.packages, robot):
                        self.packages[package] = True
                        robot.prepare(
                            package,
                            package_policies[package],
                            self.belt_policies[package.destination],
                        )
                    # If not possible, it goes to a resting location.
                    elif rest := self._get_optimal_rest(robot):
                        robot.set_rest(rest, self.rest_policies[rest])
                if package := robot.step():
                    del self.packages[package]
            self._print()
            time.sleep(0.1)

    def _create_packages(self, n: int) -> dict[Package, bool]:
        """
        Returns `n` packages randomly distributed from the racks.
        """
        rack_cells: list[Location2D] = self._get_cells(CellType.RACK)
        return {
            Package(location, random.choice(self.belts)): False
            for location in random.sample(rack_cells, n)
        }

    def _create_robots(self, n: int) -> list[Robot]:
        """
        Returns `n` robots randomly distributed around the warehouse.
        """
        locations: list[Location2D] = self._get_cells(CellType.FREE)
        return [Robot(location) for location in random.sample(locations, n)]

    def _get_cells(self, type_: CellType) -> list[Location2D]:
        """
        Returns the cells in `self.map` of the given `type_`.
        """
        rows, cols = len(self.map), len(self.map[0])
        return [
            Location2D(j, i)
            for i, j in itertools.product(range(rows), range(cols))
            if self.map[i][j] == type_.value
        ]

    @staticmethod
    def _get_package(packages: dict[Package, bool], robot: Robot) -> Package:
        """
        Returns the package that's most "transport efficient" for `robot`.
        """

        def cost(package: Package) -> float:
            """
            Computes the cost of transporting `package`.
            """
            c1: float = util.distance(robot.location, package.location)
            c2: float = util.distance(package.location, package.destination)
            return c1 + c2

        packages: list = [pkg for pkg, taken in packages.items() if not taken]
        return min(packages, key=cost) if packages else None

    def _get_policies(
        self,
        targets: list[Location2D],
    ) -> dict[Location2D, dict[Location2D, Action]]:
        """
        Returns the optimal policy to reach each location in `targets`.
        """
        problem: Grid2D = Grid2D(self.map, targets, [])
        policies: dict = MultiPolicy().run(problem)
        return {t: util.reverse_policy(policies[t]) for t in targets}

    def _get_optimal_rest(self, robot: Robot) -> Location2D | None:
        """
        Returns the resting location closest `robot`, if not already in one.
        """
        if robot.rest or robot.location in self.rests:
            return None
        rests: list[Location2D] = self.rests[:]
        for robot in self.robots:
            if robot.rest:
                rests.remove(robot.rest)
        cost = lambda rest: util.distance(robot.location, rest)
        return min(rests, key=cost)

    def _new_packages(self, n: int) -> dict[Package, dict[Location2D, Action]]:
        """
        Creates a new set of packages and returns the policy to (independently)
        deliver each one.
        """
        self.packages = self._create_packages(n)
        return {
            package: self._get_policies([package.location])[package.location]
            for package in self.packages
        }

    def _print(self) -> None:
        layout: list[str] = []
        p_locations: list[Location2D] = [p.location for p in self.packages]
        r_locations: list[Location2D] = [r.location for r in self.robots]
        for i, row in enumerate(self.map):
            layout.append("")
            for j, cell in enumerate(row):
                if (j, i) in p_locations:
                    layout[-1] += Icon.PACKAGE.value
                elif (j, i) in r_locations:
                    layout[-1] += Icon.ROBOT.value
                elif (j, i) in self.rests:
                    layout[-1] += Icon.REST.value
                else:
                    layout[-1] += char_map[cell]
        print("\n".join(layout))

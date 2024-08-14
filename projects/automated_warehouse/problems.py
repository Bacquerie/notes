import abc
import enum
import math
from typing import NamedTuple


# GENERAL DEFINITIONS


class Successor(NamedTuple):
    """
    Contains information retrieved by `SearchProblem.get_successors`.
    """

    successor: any
    action: any
    cost: float


class SearchProblem(abc.ABC):
    """
    Defines a common interface for search problems.
    """

    @abc.abstractmethod
    def apply(self, state: any, action: any) -> any:
        """
        Returns the state resulting from applying `action` on `state`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_initial_state(self) -> any:
        """
        Returns the problems' initial state.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_successors(self, state: any) -> list[Successor]:
        """
        Returns the valid successors of `state`, accompanied by the action
        needed to go from `state` to the successor, and the cost of performing
        such action.
        :return: A list of tuples of the form ``(successor, action, cost)``.
        """
        raise NotImplementedError


# GRID 2D IMPLEMENTATION


class Location2D(NamedTuple):
    """
    Represents a 2D discrete location.
    """

    x: int
    y: int


class Action(enum.Enum):
    """
    Valid directions/actions for `Grid2D` problem instances.
    """

    N: Location2D = (-1, 0)
    #NE: Location2D = (-1, 1)
    E: Location2D = (0, 1)
    #SE: Location2D = (1, 1)
    S: Location2D = (1, 0)
    #SW: Location2D = (1, -1)
    W: Location2D = (0, -1)
    #NW: Location2D = (-1, -1)

    def apply(self, location: Location2D) -> Location2D:
        """
        Returns the state resulting from applying this action to `location`.
        """
        dy, dx = self.value
        return Location2D(location.x + dx, location.y + dy)

    def get_icon(self) -> str:
        i: int = _actions.index(self)
        #icons: list[str] = ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️"]
        icons: list[str] = ["⬆️", "➡️", "⬇️", "⬅️"]
        return icons[i]

    def reverse(self) -> "Action":
        n: int = len(_actions)
        i: int = (_actions.index(self) + n // 2) % n
        return _actions[i]


_actions: list[Action] = list(Action)


class CellType(enum.Enum):
    """
    Possible cells appearing in a `Grid2D` map.
    """

    FREE: str = " "
    RACK: str = "*"
    WALL: str = "#"


class Grid2D(SearchProblem):
    """
    Implements `SearchProblem` for 2D-grid-based search problems, where there
    are explicit initial and goal states (locations).
    """

    def __init__(
        self,
        grid: list[str],
        initial: list[Location2D],
        goals: list[Location2D],
    ) -> None:
        self._grid: list[str] = grid
        self._initial: list[Location2D] = initial
        self._goals: list[Location2D] = goals

    @property
    def grid(self) -> list[str]:
        return self._grid.copy()

    def apply(self, state: Location2D, action: Action) -> Location2D:
        new_state: Location2D = action.apply(state)
        return new_state if self._is_free(new_state) else None

    def get_initial_state(self) -> list[Location2D]:
        return self._initial

    def get_successors(self, state: Location2D) -> list[Successor]:
        successors: list[Successor] = []
        for action in self._get_actions(state):
            new_state: Location2D = self.apply(state, action)
            cost: float = self._cost(state, new_state)
            successors.append(Successor(new_state, action, cost))
        return successors

    @staticmethod
    def _cost(x: Location2D, y: Location2D) -> float:
        return math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(x, y)))

    def _get_actions(self, state: Location2D) -> list:
        return [action for action in Action if self.apply(state, action)]

    def _is_free(self, location: Location2D) -> bool:
        x, y = location
        return location in self and self._grid[y][x] == CellType.FREE.value

    def __contains__(self, location: Location2D) -> bool:
        rows, cols = len(self._grid), len(self._grid[0])
        x, y = location
        return 0 <= y < rows and 0 <= x < cols

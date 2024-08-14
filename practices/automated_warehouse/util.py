import heapq
import math

from problems import Action
from problems import Location2D
from problems import Successor


class PriorityQueue:
    """
    Defines a minimalistic Priority (Min) Queue.
    """

    def __init__(self, initial: any = None, priority: float = 0.0) -> None:
        """
        :param initial: Optional, to avoid 2-line initialization.
        """
        self._queue: list = []
        self._padding: int = 0
        if initial:
            self.update(initial, priority)

    def pop(self) -> any:
        """
        Removes the element with the minimum priority from the queue, returning
        such element.
        """
        _, _, item = heapq.heappop(self._queue)
        return item

    def update(self, item: any, priority: float) -> None:
        """
        Inserts a new `item` into the queue, or updates its priority if it
        already exists.
        """
        for i, (priority_, padding, item_) in enumerate(self._queue):
            if item_ == item and priority < priority_:
                del self._queue[i]
                self._queue.append((priority, padding, item_))
                heapq.heapify(self._queue)
                break
        else:
            heapq.heappush(self._queue, (priority, self._padding, item))
            self._padding += 1

    def __bool__(self) -> bool:
        return bool(self._queue)


def distance(x: Location2D, y: Location2D) -> float:
    """
    Euclidean distance between `x` and `y`.
    """
    return math.sqrt(sum((x_i - y_i) ** 2 for x_i, y_i in zip(x, y)))


def read_map(file_path: str) -> list[str]:
    """
    Reads the map layout from the given file.
    """
    with open(file_path) as file:
        return [line.strip() for line in file]


def reverse_policy(
    policy: dict[Location2D, Successor],
) -> dict[Location2D, Action]:
    """
    Constructs a "reverse" policy that indicates the actions required to go
    from any state to the problem's initial state.
    """
    return {
        state: action.reverse() if action else None
        for state, (_, action, _) in policy.items()
    }

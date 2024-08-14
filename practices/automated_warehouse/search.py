import abc
from collections import defaultdict

import util
from problems import Grid2D
from problems import Location2D
from problems import SearchProblem
from problems import Successor


class SearchAlgorithm(abc.ABC):
    """
    Defines a common interface for search algorithms.
    """

    @abc.abstractmethod
    def run(self, problem: SearchProblem) -> any:
        raise NotImplementedError

    def __call__(self, problem: SearchProblem) -> any:
        return self.run(problem)


class Dijkstra(SearchAlgorithm):
    """
    Implements Dijkstra's algorithm to find the shortest path between a
    problem's initial state(s) and every other state.
    """

    def run(self, problem: SearchProblem) -> dict[any, Successor]:
        policy: dict[any, Successor] = defaultdict(
            lambda: Successor(None, None, float("inf"))
        )
        # Elements are: ``(state, cost)``
        frontier: util.PriorityQueue = util.PriorityQueue()
        for state in problem.get_initial_state():
            policy[state] = Successor(None, None, 0)
            frontier.update((state, 0), 0)
        while frontier:
            state, cost = frontier.pop()
            for next_state, action, act_cost in problem.get_successors(state):
                total_cost: float = cost + act_cost
                if total_cost < policy[next_state].cost:
                    policy[next_state] = Successor(state, action, total_cost)
                    frontier.update((next_state, total_cost), total_cost)
        return dict(policy)


class MultiPolicy(SearchAlgorithm):
    """
    Runs Dijkstra's algorithm for each initial state in a `Grid2D` problem.
    """

    def run(
        self,
        problem: Grid2D,
    ) -> dict[Location2D, dict[Location2D, Successor]]:
        """
        Returns a policy for each initial state in `problem`.
        """
        return {
            state: Dijkstra().run(Grid2D(problem.grid, [state], []))
            for state in problem.get_initial_state()
        }

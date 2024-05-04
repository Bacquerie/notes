---
layout: page
nav_order: 2
title: Informed Search
grand_parent: CS 188 - Programming
parent: CS 188 - Playground
---


# Informed Search
{: .no_toc }
---


## Table of Contents
{: .no_toc .text-delta }

- TOC
{:toc}

---


## A*

This snippet is very similar to the one in [Uninformed Search - Uniform-cost Search], with the
additional consideration of the (forward) heuristic.

```python
def a_star_search(problem: SearchProblem, heuristic) -> list[Action]:
    start: State = problem.get_start_state()

    visited: set[State] = set()
    fringe: PriorityQueue = PriorityQueue()
    fringe.push((start, [], 0), heuristic(start, problem))
    while not fringe.is_empty():
        current, path, g_n = fringe.pop()
        if problem.is_goal_state(current):
            return path
        if current in visited:
            continue
        visited.add(current)
        for successor, action, step_cost in problem.get_successors(current):
            f_n: float = g_n + step_cost + heuristic(successor, problem)
            fringe.update((successor, path + [action], g_n + stepCost), f_n)
```


<!-- REFERENCES -->
[Uninformed Search - Uniform-cost Search]: ../uninformed-search/#uniform-cost-search
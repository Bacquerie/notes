---
layout: page
nav_order: 1
title: Uninformed Search
grand_parent: CS 188 - Programming
parent: CS 188 - Playground
---


# Uninformed Search
{: .no_toc }
---


## Table of Contents
{: .no_toc .text-delta }

- TOC
{:toc}

---


## Depth-first Search

The following snippet is based on my implementation for CS 188's **[Search project]**. Due to the
small changes, and missing type definitions, it could be taken as pseudocode.

Each state `s` in the `fringe` keeps the path from the start state to `s`, which is memory-expensive
but convenient for the return value.

```python
def depth_first_search(problem: SearchProblem) -> list[Action]:
    visited: set[State] = set()
    fringe: Stack = Stack()
    fringe.push((problem.get_start_state(), []))
    while not fringe.is_empty():
        current, path = fringe.pop()
        if problem.is_goal_state(current):
            return path
        if current in visited:
            continue
        visited.add(current)
        for successor, action in problem.get_successors(current):
            fringe.push((successor, path + [action]))
```
---

## Breadth-first Search

This implementation basically only changes the `Stack` for a `Queue`.

Given the code duplicity, the search function could be abstracted to not depend on particular
*queuing* data structures.

```python
def breadth_first_search(problem: SearchProblem) -> list[Action]:
    visited: set[State] = set()
    fringe: Queue = Queue()
    fringe.push((problem.get_start_state(), []))
    while not fringe.is_empty():
        current, path = fringe.pop()
        if problem.is_goal_state(current):
            return path
        if current in visited:
            continue
        visited.add(current)
        for successor, action in problem.get_successors(current):
            fringe.push((successor, path + [action]))
```
---

## Uniform-cost Search

Same as above snippets, but using a `PriorityQueue`, and considering the (backward) cost to reach
each node.

```python
def uniform_cost_search(problem: SearchProblem) -> list[Action]:
    visited: set[State] = set()
    fringe: PriorityQueue = PriorityQueue()
    fringe.push((problem.get_start_state(), [], 0), 0)
    while not fringe.is_empty():
        current, path, cost = fringe.pop()
        if problem.is_goal_state(current):
            return path
        if current in visited:
            continue
        visited.add(current)
        for successor, action, step_cost in problem.get_successors(current):
            total_cost: float = cost + step_cost
            fringe.update((successor, path + [action], total_cost), total_cost)
```


<!-- REFERENCES -->
[Search project]: https://inst.eecs.berkeley.edu/~cs188/sp24/projects/proj1/
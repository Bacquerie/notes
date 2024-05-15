---
layout: page
title: Uninformed Search
grand_parent: Programming
parent: Playground
---

# Uninformed Search Algorithms

```python
def depthFirstSearch(problem: SearchProblem):
    visited: set = set()
    fringe: util.Stack = util.Stack()
    fringe.push((problem.getStartState(), []))
    while not fringe.isEmpty():
        current, path = fringe.pop()
        if problem.isGoalState(current):
            return path
        if current in visited:
            continue
        visited.add(current)
        for successor, action, _ in problem.getSuccessors(current):
            fringe.push((successor, path + [action]))
```
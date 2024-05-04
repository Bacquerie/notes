---
layout: mathjax
nav_order: 1
title: Uninformed Search
grand_parent: CS 188
parent: CS 188 - Notes
toc: true
---

{% include mathjax.html %}


# Uninformed Search
---


## Reflex agents

Choose actions based only on their current state, and do not consider future consequences of such
actions. They are not rational, as they do not look to have an optimal behavior (minimize a cost
function).


## Planning agents

Elaborate a sequence of actions to reach a *goal*, considering how the world evolves in response to
their actions. They could be:

- **Optimal**, if they minimize a cost function
- **Complete**, if, given that a solution exists, they are able to find it


## Search problems

Consist of:
- A state space
- A successor function
- A start state and a goal test

A *solution* is a sequence of actions that goes from a start state to a goal state.


## Depth-first search

Expands the deepest node first. Frontier is usually a stack.

- Is it complete? No, as it could potentially grow infinitely
- Is it optimal? No. It's not exhaustive and settles for the first found solution
- Time complexity: $$O\pars{b^m}$$
- Space complexity: $$O\pars{bm}$$

Where $$m$$ is the maximum depth of the search tree.


## Breadth-first search

Expands one level at a time. Frontier is usually a queue.

- Is it complete? Yes, as it's exhaustive on a per-level basis
- Is it optimal? Yes, as only one depth level is explored at a time (if traverse cost is
        the same for all successors)
- Time complexity: $$O\pars{b^s}$$
- Space complexity: $$O\pars{b^s}$$

Where $$s$$ is the depth of the search tree where a solution exists.


## Iterative deepening

DFS with increasing depth limits.

- Is it complete? Yes, as it's exhaustive on a per-level basis
- Is it optimal? Yes, same as above
- Time complexity: $$O\pars{b^s}$$
- Space complexity: $$O\pars{bs}$$


## Uniform-cost search

Takes into account the *cost* of reaching a node. Frontier is usually a priority queue (based on
cumulative cost).

- Is it complete? Yes, as it's exhaustive on its path
- Is it optimal? Yes, as it looks to minimize the cost
- Time complexity: $$O\pars{b^{C / \epsilon}}$$
- Space complexity: $$O\pars{b^{C / \epsilon}}$$
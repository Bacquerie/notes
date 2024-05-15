---
layout: mathjax
nav_order: 3
title: Adversarial Search
grand_parent: CS 188
parent: CS 188 - Notes
---
{% include mathjax.html %}
# Adversarial Search
---


<!-- MINIMAX -------------------------------------------------------------------------------------->
## Minimax


The **Minimax** algorithm is a kind of deterministic, perfect information, zero-sum game, of 2
players (but extensible to N players) where one player (the *root player*) is looking to maximize
a utility function, while the other player is looking to maximize theirs (which is equivalent to
minimize the former player's utility).

Only terminal state possess a utility, while non-terminal states recursively iterate between
maximizing and minimizing said utility until they are able to reach terminal states.

Given the nature of the algorithm, each player assumes that the opponent always makes optimal
decisions (max utility vs min utility).

States under agent's control
{:.text-delta}

$$ V(s) = \underset{s' \in \mbox{successors(s)}}{\mbox{max}} \left\{V(s')\right\} $$

States under opponent's control
{:.text-delta}

$$ V(s') = \underset{s \in \mbox{successors(s')}}{\mbox{min}} \left\{V(s)\right\} $$


### Complexity

- **Time**: Just like DFS, $$O\pars{b^m}$$
- **Space**: Just like DFS, $$O\pars{bm}$$


## Depth-limited Search


As Minimax tree can grow too large, it may not be feasible to build/traverse all the tree. In that
case, a better option would be to look at states located at depth $$\le d$$. As depth-limited search
may not expand terminal nodes, and utilities cannot be computed exactly, we compute estimates
of utilities through an *evaluation function* (just like A* uses estimates to goal state or
heuristics).


## $$\alpha-\beta$$ Pruning

- $$\alpha$$ is the best value for *max* levels found so far.
- $$\beta$$ is the best value for *min* levels found so far.

> If at any time $$\alpha \ge \beta$$ we can stop going further down the pending subtrees, and
> go back in the recursion tree until that condition stops holding.
{:.highlight.py-4}

---


<!-- EXPECTIMAX ----------------------------------------------------------------------------------->
## Expectimax


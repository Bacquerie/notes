---
layout: mathjax
nav_order: 2
title: Informed Search
grand_parent: CS 188
parent: CS 188 - Notes
---
{% include mathjax.html %}
# INFORMED SEARCH
---


Informed search refers to a set of algorithms who possess (or are able to compute) additional
information about the problem or the goal, and use this additional information to make better
decisions about the nodes they expand.


## HEURISTICS

A *heuristic* is a function $$h(n)$$ that estimates how close a state is to the goal.


## GREEDY SEARCH

It's a type of informed search algorithm that at any given time, chooses the node closest (with
the minimum heuristic value) to the goal. It is also called *best-first search*.


## A* SEARCH

Combines the characteristics of uniform-cost search and greedy search as it takes into account both:

- The actual costs of reaching the current state (*backward cost* $$g(n)$$), and
- The estimated cost of reaching the goal (*forward cost* $$h(n)$$)

> A* cost function is $$f(n) = g(n) + h(n)$$.
{: .highlight .py-4 }


## ADMISSIBILITY AND CONSISTENCY

For A* *tree search* to work, its heuristic $$h$$ must be *admissible*; that is:

$$ 0 \le h(n) \le h^*(n) $$

where $$h^*(n)$$ is the true cost to reaching the goal.

For A* *graph search* to work, its heuristic $$h$$ must be *consistent*; that is:
$$ \forall A, B \in G  $$

$$ h(A) - h(B) \le \mbox{cost}(A, B) $$

where $$A, B$$ are nodes in the graph $$G$$.

> An admissible heuristic is not necessarily consistent, but a consistent heuristic is always
admissible.
{: .highlight .py-4 }
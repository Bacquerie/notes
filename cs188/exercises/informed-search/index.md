---
layout: mathjax
nav_order: 2
title: Informed Search
grand_parent: CS 188
parent: CS 188 - Exercises
---
{% include mathjax.html %}

# INFORMED SEARCH
{: .no_toc }
---

## Table of Contents
{: .no_toc .text-delta }
- TOC
{:toc}


---
<!-- EXERCISE 1 -->
## 1. State-Space Formulation

It is training day for Pacbabies, also known as Hungry Running Maze Games day. Each of $$k$$
Pacbabies starts in its own assigned start location $$s_i$$ in a large maze of size $$M \times N$$
and must return to its own Pacdad who is waiting patiently but proudly at $$g_i$$ along the way,
the Pacbabies must, between them, eat all the dots in the maze.

At each step, all $$k$$ Pacbabies move one unit to any open adjacent square. The only legal actions
are *Up, Down, Left, or Right*. It is illegal for a Pacbaby to wait in a square, attempt to move
into a wall, or attempt to occupy the same square as another Pacbaby. To set a record, the
Pacbabies must find an optimal collective solution.


- Define a minimal state space representation for this problem.
> <details>
>     <summary><b>Solution</b></summary>
>     
>     <p>The state space representation should exhaustively collect all possible configurations of
>     world states, taking into account only the elements that could possibly change from one
>     moment to the next.</p>
>
>     For this problem, the world states are the possible configurations of the maze and its
>     elements, and the only elements that could change from moment to moment are:
> 
>     <ul>
>       <li>The (unknown) positions of the food pellets, as they could exist or not, or exist and
>           then stop existing (being eaten)</li>
>       <li>The positions of the Pacbabies as they traverse the maze</li>
>     </ul>
> 
>     Other things like the possible directions of Pacbabies, help create new states but, per se,
>     are not visible world configurations, nor are they variable.
> </details>


- How large is the state space?
> <details>
>     <summary><b>Solution</b></summary>
> 
>     Given the above descriptions:
>     <ul>
>       <li>The food pellets might exist or not exist in each cell of the maze, creating
>           \(2^{mn}\) possible food configurations.</li>
>       <li>The Pacbabies can possibly traverse all cells in the maze of size \(mn\). Since there
>           are \(k\) Pacbabies, there are \(O\pars{(mn)^k}\) Pacbabies' position configurations.</li>
>     </ul>
> 
>     Creating a total of \(O\pars{(mn)^k \, 2^{mn}}\) world configurations.
> </details>


- What's the maximum branching factor?
> <details>
>     <summary><b>Solution</b></summary>
>
>     The branching factor of a search tree is determined by the possible actions that could create
>     new states. Since the only actions available are the Pacbabies' directions, we have an action
>     space of 4, and as we have \(k\) Pacbabies, the branching factor has a size of \(4^k\).
> </details>


---
<!-- EXERCISE 2 -->
## 2. Heuristics

You'd like to choose two heuristic functions, $$f$$ and $$g$$, such that max$$(f(n), g(n))$$ is an
admissible heuristic.


- What is a sufficient condition on $$f$$ and $$g$$ for $$h$$ to be admissible?
> <details>
>     <summary><b>Solution</b></summary>
>
>     Both, \(f\) and \(g\) have to be admissible.
> </details>


Now, you'd like to choose two heuristic functions such that
$$ h(n) = \alpha f(n) + (1 - \alpha) g(n) $$ is admissible for any value $$\alpha \in [0, 1]$$.


- What is a sufficient condition for $$h$$ to be admissible?
> <details>
>     <summary><b>Solution</b></summary>
>
>     Given that \(\alpha \in [0, 1]\), \(h(n)\) can only vary within the bounds of \(f\) and \(g\);
>     so, it is sufficient that both are admissible heuristics.
> </details>

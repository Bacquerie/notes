---
layout: mathjax
nav_order: 4
title: Optimization Algorithms
grand_parent: CS 230
parent: CS 230 - Notes
---
{% include mathjax.html %}
# Optimization Algorithms
---


## Mini Batch Gradient Descent

Train on small datasets instead of the whole training set, per epoch.

**Pros**:
- Convenient when the training set is too large to fit in memory
- Iterates faster

**Cons**:
- Each batch directs the gradient, which could make it more unstable; though, in practice, not
big of an inconvenient if training on many epochs
---
layout: mathjax
nav_order: 3
title: Improving Deep NN
grand_parent: CS 230
parent: CS 230 - Notes
---
{% include mathjax.html %}
# IMPROVING DEEP NEURAL NETWORKS
---


## Train / Dev / Test Sets

- The **training set** is used to train your algorithm
- The **dev set** is used to validate the efficiency of different algorithms or architectures,
    and be able to select the best-performing
- The **test set** is used to validate how well your chosen algorithm generalizes to completely
    new data


## Bias / Variance Intuition

Non-formally the bias and variance can be associated to whether your algorithm *underfits* or
*overfits* the training and dev sets. As a summary:

- High bias $$\approx$$ underfitting; very bad at training data and very bad at generalizing
- High variance $$\approx$$ overfitting; very good at training data and very bad at generalizing

A *just right* algorithm should be able to be very good at both sets; bias / variance not too low
but not too high. Both should be approximately equal and not too far from the **Bayes error**.


## Regularization

It's an additional term to the cost function that prevents weights from growing too large, by
penalizing them.

For neural networks with $$\mathcal{l}$$-2 regularization, it has the following general form:

$$ J =  \mbox{Usual cost function} + \frac{\lambda}{2m} \lVert w^{[k]} \rVert^2_F $$

Where $$\lVert \cdot \rVert^2_F$$ is called the *Fröbenius Norm*, and it's defined as the sum of
all the elements in the matrix; thus resulting in a scalar value (as every norm should).

With this additional term, there's an associated update to how the parameters $$w$$ are updated via
gradient descent.

$$ \partder{w^{[k]}}{J} = \mbox{Usual partial derivative} + \frac{\lambda}{m} w^{[k]} $$
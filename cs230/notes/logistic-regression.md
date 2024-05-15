---
layout: mathjax
nav_order: 1
title: Logistic Regression as a Neural Network
grand_parent: CS 230
parent: CS 230 - Notes
---
{% include mathjax.html %}
# LOGISTIC REGRESSION AS A NEURAL NETWORK
---


## Notation

Given $$x \in \mathbb{R}^n$$, $$y \in \bracks{0, 1}$$, the training set consists of $$m$$ examples
of the form $$\bracks{\pars{x^{(i)}, y^{(i)}}}$$, $$1 \le i \le m$$, with $$x^{(i)}$$ being a
column vector.


## Logistic Regression

Given $$\mathbf{X}$$, we want to compute $$\hat{y} = \prob{y = 1 | \mathbf{X}}$$. The core of the
logistic regression is the logistic function:

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

And we compute the predictions as:

\begin{equation}
    \hat{y} = \sigma\pars{\transp{w} \mathbf{X} + b}
\end{equation}
where $$w \in \mathbb{R}^n$$ and $$b \in \mathbb{R}$$ are the trainable parameters that will make the
classifier work.


### Loss Function

Given $$\hat{y} = \sigma\pars{z}$$, we want $$\hat{y} \approx y$$. We control this by adjusting the
parameters $$w$$ and $$b$$ to best fit the training data, and the way to better adjust these
parameters is minimizing a *loss* function that measures how well our predicted values $$\hat{y}$$
are.

The typical loss function used for logistic regression is the *binary cross-entropy* defined as:

\begin{equation}
    \mathcal{L}\pars{\hat{y}, y} = -y \log\pars{\hat{y}} - (1 - y) \log\pars{1 - \hat{y}}
\end{equation}
which guarantees convexity (required for minimization).


### Cost Function

Average loss over all examples.

\begin{equation}
    \mathcal{J}\pars{w, b} = \frac{1}{m} \sum_{i=1}^{m} \mathcal{L}\pars{\hat{y}^{(i)}, y^{(i)}}
\end{equation}


### Gradient Descent

It's the algorithm that will actually help the classifier find its optimal parameters, by
minimizing the cost function over the training set.

Repeat until convergence { \\
$$w \leftarrow w - \alpha \partder{w}{\mathcal{J}\pars{w, b}}$$ \\
$$b \leftarrow b - \alpha \partder{b}{\mathcal{J}\pars{w, b}}$$ \\
}


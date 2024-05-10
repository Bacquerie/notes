---
layout: mathjax
nav_order: 2
title: Deep Neural Networks
grand_parent: CS 230
parent: CS 230 - Notes
---
{% include mathjax.html %}
# DEEP NEURAL NETWORKS
---


## FORWARD PROPAGATION

Also called the *prediction step*, propagates the inputs $$\mathbf{X} = a^{[0]}$$ all the way to
the output layer, which produces the predicted output $$\hat{y}$$.

$$z^{[i]} = w^{[i]} a^{[i - 1]} + b^{[i]}$$ \\
$$a^{[i]} = \sigma^{[i]} \pars{z^{[i]}}$$
{: .text-center }

with sizes: $$z^{[i]} = (n_i, 1)$$, $$w^{[i]} = (n_i, n_{i - 1})$$,
$$a^{[i - 1]} = (n_{i - 1}, 1)$$, and $$b^{[i]} = (n_i, 1)$$, being $$n_k$$ the number of neurons
in layer $$k$$, assuming propagation of one example at a time, although it also works for multiple
examples at a time with the following changes in dimensions:

$$a^{[i - 1]} = (n_{i - 1}, m)$$ \\
$$w^{[i]} = (n_i, n_{i - 1})$$ \\
$$z^{[i]} = (n_i, m)$$ \\
$$a^{[i]} = (n_i, m)$$
{: .text-center }

> If $$k$$ is the last layer in the network, then $$\hat{y} = a^{[k]}$$.
{: .highlight .py-4 }


## BACKWARD PROPAGATION

In order for a neural network to be useful, it not only needs to be able to predict values, but to
improve the quality of those values, such that $$\hat{y} \approx y$$. What makes a neural network
improve its outputs is the *backward step* which adjusts the parameters $$w$$ and $$b$$ for each of
its layers.

This step is called backward because it works in reverse order: from the last layer, back to the
first one.

Recalling the gradient descent algorithm, each of the weights (trainable parameters) in layer $$k$$
are updated according to the formula:

$$ w^{[k]} \leftarrow w^{[k]} - \alpha \partder{w^{[k]}}{J\pars{y, \hat{y}}} $$ \\
$$ b^{[k]} \leftarrow b^{[k]} - \alpha \partder{b^{[k]}}{J\pars{y, \hat{y}}} $$
{: .text-center }

where $$J\pars{y, \hat{y}}$$ is an associated *cost function* that computes how accurate our
current $$\hat{y}$$ are. These loss functions will be explained in a later section, but for now
their precise definition is not relevant.

To be able to compute such derivatives we have to work very slowly, and recall the chain rule of
differentiation.

For $$\partder{w^{[k]}}{J\pars{y, \hat{y}}}$$ we have to create the chain of dependence that links
$$J$$ to $$w^{[k]}$$, and that relationship goes as follows:

- $$J$$ depends on $$\hat{y}$$
- $$\hat{y} = a^{[k]}$$ depends on $$z^{[k]}$$
- $$z^{[k]}$$ depends on $$w^{[k]}$$

Then, the corresponding gradient (through chain rule) is defined as:

$$
    \partder{w^{[k]}}{J\pars{y, \hat{y}}} = \partder{a^{[k]}}{J} \partder{z^{[k]}}{a^{[k]}}
        \partder{w^{[k]}}{z^{[k]}}
$$

Which results in:

$$
    \partder{w^{[k]}}{J\pars{y, \hat{y}}}
        = \pars{\partder{a^{[k]}}{J} \odot \sigma^{[k]}}'\pars{z^{[k]}} {a^{[k - 1]}}^\top
$$

For which I only remember the $$\odot$$ and the transposed because it makes dimensional sense.

There are $$(n_k, n_{k - 1})$$ weights $$w$$, that's the target dimension that the chain of
derivatives should produce. By the same logic:

- There are $$(n_k, 1)$$ values for $$a^{[k]}$$, so the gradient of $$J$$ must be that size
- There are $$(n_k, 1)$$ values for $$z^{[k]}$$
- There are $$(n_{k-1}, 1)$$ values for $$a^{[k - 1]}$$

Since $$a^{[k]}$$ and $${\sigma^{[k]}}'\pars{z^{[k]}}$$ have the same size, one possible way to
multiply these, is element by element, which is represented by the $$\odot$$.

Their product has also a size of $$(n_k, 1)$$. And the *dimensional way* to multiply this with
$$a^{[k - 1]}$$ is transposing it, thus producing a matrix of size
$$(n_k, 1) \times (1, n_{k-1}) = (n_k, n_{k - 1})$$, which is our desired output size.

We cannot reduce $$\partder{a^{[k]}}{J}$$ as we do not know the cost function, but plugging a
particular function (or its derivative, actually) should be straightforward.

> The same process and *dimensional logic* can be applied to compute
> $$\partder{b^{[k]}}{J\pars{y, \hat{y}}}$$.
{: .highlight .py-4 }


## ACTIVATION FUNCTIONS

### LINEAR

Also called *identity*, leaves the input unaltered:

$$ a(z) = z \hspace{5cm} a'(z) = 1 $$


### RELU

Rectified Linear Unit. Clips negative values to 0, leaving positive values unchanged:

$$ a(z) = \mbox{max}(0, z) \hspace{3cm} a'(z) = 1$$ where $$z \ge 0$$; 0 elsewhere
{: .text-center}


### SIGMOID

Outputs values between 0 and 1, making its output be interpretable as the probability that its
input is 1.

$$ a(z) = \frac{1}{1 + e^{-z}} \hspace{5cm} a'(z) = a(z) (1 - a(z))$$


## LOSS FUNCTIONS

### MEAN SQUARED LOSS

Mean squared euclidean distance between $$y$$ and $$\hat{y}$$.

$$
    \mathcal{L} = \frac{1}{2m} (\hat{y} - y)^\top (\hat{y} - y)
    \hspace{3cm}
    \mathcal{L}' = \frac{1}{m} \pars{\hat{y} - y}
$$


### BINARY CROSS-ENTROPY

It's the usual loss associated to binary classification.

$$
    \mathcal{L} = -\frac{1}{m} \sum_i y_i \log\pars{\hat{y_i}} + (1 - y_i) \log\pars{1 - \hat{y_i}}
    \hspace{2cm}
    \mathcal{L}' = -\frac{1}{m} \pars{\frac{y_i}{\hat{y_i}} - \frac{1 - y_i}{1 - \hat{y_i}}}
$$
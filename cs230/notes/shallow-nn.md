---
layout: mathjax
nav_order: 2
title: Shallow Neural Networks
grand_parent: CS 230
parent: CS 230 - Notes
---

{% include mathjax.html %}


# Shallow Neural Networks
---

## Forward propagation

Propagates the inputs $$\mathbf{X} = a^{[0]}$$ all the way to the output layer.
\begin{equation}
    \begin{gathered}
        z^{[i]} = w^{[i]} a^{[i - 1]} + b^{[i]} \\
        a^{[i]} = \sigma^{[i]} \pars{z^{[i]}} \\
    \end{gathered}
\end{equation}
with sizes: $$z^{[i]} = (n_i, 1)$$, $$w^{[i]} = (n_i, n_{i - 1})$$, $$a^{[i - 1]} = (n_{i - 1}, 1)$$,
and $$b^{[i]} = (n_i, 1)$$, being $$n_k$$ the number of neurons in layer $$k$$, assuming
propagation of one example at a time, although it also works for multiple examples at a time with
the following changes in dimensions:

$$a^{[i - 1]} = (n_{i - 1}, m)$$ \\
$$w^{[i]} = (n_i, n_{i - 1})$$ \\
$$z^{[i]} = (n_i, m)$$ \\
$$a^{[i]} = (n_i, m)$$
{: .text-center }
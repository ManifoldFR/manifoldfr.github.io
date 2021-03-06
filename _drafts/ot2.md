---
layout: post
title: "Optimal Transport: Gradient flows"
tags: optimal-transport
---
{% include mathjax.html %}

[Last time](2021-05-13-ot.md) we had an introductory look at OT, the definition and computation of the Wasserstein distance.

A year ago, I wrote a solver for this variational formulation of mean-field games, as part of a project. This eventually led to a [small C++ library](https://github.com/ManifoldFR/entropic-mfg) as a toy project, which I reworked a bit recently and might be usable.

## Mean-Field Games

The dynamics are defined by
$$
    dX_t = \alpha_t X_t\,dt + \sigma dW_t
$$
where \\( W \\) is a Brownian motion. Typically $$ W $$ could be an $$ \RR^d $$-brownian motion with independent components.

$$
    \inf_{\{\alpha_t\}_t} J(\alpha) = \EE\left[ \int_0^T \frac{1}{2}\|\alpha_t\|^2 + f(X_t, \rho_t) \,dt + g(X_T, \rho_T) \right]
$$

where $$ \rho_t = \mathcal{L}(X_t) $$ is the marginal distribution of the random variable $$ X_t $$.
The optimality condition for this stochastic control problem where established by Lasry and Lions: they are known as the *mean-field game equations*. They are a system of coupled Fokker-Planck and Hamilton-Jacobi-Bellman equations:
$$
\begin{align}
    \partial_t \rho &= \frac{\sigma^2}{2}\Delta \rho - \mathrm{div}(\rho\nabla u)  \\
    -\partial_t u - \frac{\sigma^2}{2}\Delta u + \frac{1}{2}|\nabla u|^2 &= f(x, \rho)  \\
    u(T,\cdot) &= g(x, \rho_T)
\end{align}
$$
These are nonlinear equations due to the control cost term $$ |\nabla u|^2 $$ in the second, HJB partial differential equation. The first PDE is a linear, Fokker-Planck PDE. The optimal control is given in feedback form as $$ \alpha^*_t = \nabla_x u(t, X_t) $$.
[Numerical methods](https://hal.archives-ouvertes.fr/hal-00392074/document) for these equations can involve a fair bit of finite-difference discretisation, Krylov subspace methods...

Here, we lay out a solution method for this particular case of MFG (some might say the control Hamiltonian has a rather specific form...) using optimal transport theory.

### A variational approach

Assume the integral $$ \int f(x, \rho)\, d\rho(x) $$ can be rewritten as real-valued function $$ F(\rho) $$, and that the same goes for $$ g $$.
The variational approach separates the probability distribution path $$ \{\rho_t\} $$ as a problem variable, and directly optimize over the feedback control function $$ v(t,x) = \nabla_x u (t,x) $$, which we recall should be drift coefficient of the underlying SDE.
That formulation, reads
$$
\begin{equation}
\begin{aligned}
    \inf_{\rho,v} \int_0^T \frac{1}{2}|v(t,x)|_2^2 + F(\rho_t)\,dt + G(\rho_T) \\
    \suchthat \partial_t\rho = \frac{\sigma^2}{2}\Delta\rho - \mathrm{div}(\rho v)
\end{aligned}
\end{equation}
$$
The optimality conditions of this equation, should yield the HJB equation from before.
There are several ways of solving this problem directly, by casting it as a nonlinear program: the transcription step will discretise the continuous space, (using a grid, triangulated mesh, PL manifold...), and discretise the integral and constraint in time. The obtained finite-dimensional program will be a traditional NLP. Benamou and Carlier introduced an augmented Lagrangian method for this problem in [1].

[2] introduces a Lagrangian variational formulation of the mean-field game, which reads
$$
\begin{align}
    \inf_{Q, \{\mu_t\}} \mathcal{K}(Q) + \int_0^T F(\mu_t)\, dt + G(\mu_T)   \\
    \suchthat P_tQ = \mu_t
\end{align}
$$
where $$ Q $$ is a measure over the space of trajectories $$ \mathbb{X} $$, and $$ P_t $$ denotes the marginal operator at time $$ t $$, which is the pushforward of the evaluation map $$ \delta_t: \omega \longmapsto \omega(t) $$.[^fn1]
The important part is the kinetic energy term $$ \mathcal{K}(Q) = \int_{\mathbb{X}} \int_{[0,T]} \frac{1}{2} |\dot{\omega}(t)|^2\,dt\,dQ(\omega) $$.

Now, you may ask where the dynamics went. It's all very subtle here, but they're actually not that far. They're actually baked into both the minimization and the concept of path distributions $$ Q $$.

---

* [1] Jean-David Benamou, Guillaume Carlier, *Augmented Lagrangian Methods for Transport Optimization, Mean-Field Games and Degenerate PDEs*. <https://www.ceremade.dauphine.fr/~carlier/ALG2_Draft.pdf>
* [2] Jean-David Benamou, Guillaume Carlier, Filippo Santambrogio, *Variational Mean Field Games*. <https://hal.archives-ouvertes.fr/hal-01295299/document>
* [2] Jean-David Benamou, Guillaume Carlier, Simone Marino, Luca Nenna, *An entropy minimization approach to second-order variational mean-field games*. <https://hal.archives-ouvertes.fr/hal-01848370v4/document>

[^fn1]: Meaning $$ P_t $$ takes a measure $$ Q $$ over the space of paths, and gives the marginal distribution of $$ \omega(t) $$ when $$ \omega \sim Q $$.

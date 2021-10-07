---
layout: post
title: "Augmented Lagrangian methods"
tags: optimization
---

In general nonlinear optimization, we seek to solve problems of the form
\\begin{equation}\tag{NLP}
\begin{aligned}
    &\min_z \ell(z)  \\\\\\
    &\mathrm{s.t.}\ c(z) = 0
\end{aligned}
\\end{equation}
This kind of formulation is often encountered in machine learning, control problems and others where structured, constrained optimization crops up.

In our recent work, we adopt a kind of proximal-point algorithm called the _method of multipliers_, which minimizes a penalized version of the problem Lagrangian called the <span style="color: blue">_augmented Lagrangian_</span>:
\\begin{equation}
    \calL(z, \lambda; \mu) = \ell(z) + \lambda^\top c(z) + \frac{\mu}{2}\\|c(z)  \\|_2^2
\\end{equation}
then updates the Lagrange multiplier $\lambda$:
\\begin{equation}\label{eq:MethMult}
\begin{aligned}
    z^{k+1} &\in \arg\min_z \calL_A(z, \lambda^k)  \\\\\\
    \lambda^{k+1} &= \lambda^k + \mu c(z^{k+1})
\end{aligned}
\\end{equation}

Why is this a proximal algorithm? In fact, under suitable assumptions the above update is equivalent to the dual proximal-point iteration:
\\begin{equation}\label{eq:ProxIter}
    \lambda^{k+1} = \arg\max_\lambda \\{ \min_z \calL(z, \lambda) - \frac{1}{2\mu}\\| \lambda - \lambda^k \\|_2^2 \\},
\\end{equation}
as can be seen by interverting $\min$ and $\max$ and noticing taking the maximum over $\lambda$ of the inner expression yields a minimization of $\calL_A(z, \lambda^k; \mu)$. You can also notice that, under convexity assumptions, the inner minimum is the dual objective function of (NLP). This link between the augmented Lagrangian method of multipliers \eqref{eq:MethMult} and dual proximal-point iterations \eqref{eq:ProxIter} was investigated in a 1976 paper[^Rock76] by R. Tyrrell Rockafellar, which is a good read that I recommend.

Anyway, this shows that the next primal-dual iterate can be computed as minimization-then-update, or by solving a saddle-point with the proximal penalty in $\lambda$.
One important aspect of this equivalence, is that the stationarity conditions for \eqref{eq:ProxIter} read
\\begin{equation}
\begin{aligned}
    \nabla\ell(z) + J_c(z)^\top\lambda &= 0  \\\\\\
    \lambda = \lambda^k + {}&\mu c(z)
\end{aligned}
\\end{equation}
which are exactly a rewrite of the first-order necessary conditions of \eqref{eq:MethMult} and the multiplier update.

This remark helps us later in the sequel, as it helps with reinterpreting the method of multipliers in the framework of inexact proximal point methods, of which the BCL strategy for the method of multipliers[^Conn91] is a well-known example.

## BCL and inexact proximal iterates

Solving the minimization in \eqref{eq:MethMult} (or equivalently the saddle-point \eqref{eq:ProxIter}) -- a step we will call the "**proximal subproblem**" -- exactly is a costly affair in general, outside of the classical linear-quadratic case. Indeed, in the general setting, one might have to use an iterative scheme such as gradient descent or (quasi-)Newton steps, with varying convergence speeds and computational costs depending on problem convexity, conditioning, and sparsity.

Anyway, one might want to accelerate overall convergence of the proximal algorithm, not in terms of the number of proximal iterates (although there are methods to accelerate that) but in the total number of inner iterations used to solve the successive subproblems.

What if we were to guarantee that we can still converge to the optimum without solving the subproblem exactly, but within a loose tolerance that we will tighten as optimization progresses? Something like,
\\begin{equation}
\begin{aligned}
    &\text{i.  solve } \lambda^{k+1} \approx \arg\max_\lambda \min_z \calL^\mathrm{prox}(z, \lambda; \lambda^k, \mu)\quad \text{within tolerance } \epsilon_k > 0  \\\\\\
    &\text{ii. update }\epsilon_{k+1} < \epsilon_k
\end{aligned}
\\end{equation}

This is the idea behind inexact proximal methods.

BCL can be seen as one of these. It chooses subsequent penalties $\mu_k$ and tolerances $\epsilon_k$ depending on what the value of the contraint $c(z^k)$ is, even rejecting the iterate if not good enough.

--------

[^Rock76]: R. T. Rockafellar, “Augmented Lagrangians and Applications of the Proximal Point Algorithm in Convex Programming,” Mathematics of Operations Research, vol. 1, no. 2, pp. 97–116, 1976.

[^Conn91]: A. Conn, N. Gould, and P. Toint, “A Globally Convergent Augmented Lagrangian Algorithm for Optimization with General Constraints and Simple Bounds,” SIAM Journal on Numerical Analysis, vol. 28, Apr. 1991, doi: 10.1137/0728030.

[^Carp21]: J. Carpentier, R. Budhiraja, and N. Mansard, “Proximal and Sparse Resolution of Constrained Dynamic Equations,” Austin / Virtual, United States, Jul. 2021. Accessed: Sep. 17, 2021. [Online]. Available: <https://hal.inria.fr/hal-03271811>

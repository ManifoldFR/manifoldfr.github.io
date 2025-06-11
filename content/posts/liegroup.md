+++
title = "Some notes on Lie groups"
tags = "lie-group geometry"
draft = false
date = 2024-10-10
+++

Lie groups are an essential element of modelling in applications such as computer vision and computer graphics (namely handling cameras), and also robotics and machine learning.

They do _not_ constitute an easy subject. A lot of presentation is either overly technical, or glosses over mathematical foundations or properties which enables practitioners to carry out computations on Lie groups by themselves, or understand often unsaid assumptions or conventions in many implementations.

In this blog post, we will be taking a tour of Lie groups, Lie algebras, and useful computational facts.

<!-- more -->

In the sequel, $G$ is a Lie group, and $\mathfrak{g}$ its Lie algebra.
The Lie algebra corresponds to the tangent space at the neutral element of the group $e \in G$.

## Left-multiplication, right-multiplication

The left-multiplication map by an element $g\in G$ is
$$
\begin{equation}
\begin{aligned}
    L_g \colon G &\longrightarrow G \\\\
        h &\longmapsto g\cdot h.
\end{aligned}
\end{equation}
$$
The right-multiplication map by an element $g\in G$ is
$$
\begin{equation}
\begin{aligned}
    R_g \colon G &\longrightarrow G \\\\
        h &\longmapsto h\cdot g.
\end{aligned}
\end{equation}
$$
These maps are smooth by the axioms of Lie groups, and their inverses $L_{g^{-1}}$ and $R_{g^{-1}}$ are also smooth. Thus they define _diffeomorphisms from $G$ to itself_.

This implies that for every $g\in G$, the differential of $L_g$ (or $R_g$) at $h\in G$ defines an isomorphism between tangent spaces:
$$
  (\dif L_g)_h \colon T_h G \xrightarrow{\simeq} T\_{gh } G.
$$

Furthermore, it holds that, as functions, $L\_{gh} = L_g \circ L_h$ for all $g,h\in G$. Hence $g \mapsto L_g$ is a group homomorphism between $G$ and the automorphism group $\Aut(G)$.

This further implies that for all $g,h\in G$, by the chain rule
$$
\begin{equation}
  (\dif L_{gh})_e = \dif (L_g \circ L_h)_e = (\dif L_g)_h \circ (\dif L_h)_e
\end{equation}
$$
This makes sense: the right factor maps $T_eG \to T_hG$, the left factor maps $T_hG \to T\_{gh} G $.

### Group action on the Lie algebra

We can define a (left) _group action_ of $G$ on its Lie algebra $\mathfrak{g}$ as follows: for $g\in G$ and $\xi \in \mathfrak{g}$,
\begin{equation}
    g \cdot \xi \defeq (\dif L_g)_e(\xi).
\end{equation}

Similarly, $G$ can act on $\mathfrak{g}$ from the right by defining
$$
  \xi \cdot g \defeq (\dif R_g)_e(\xi) = \frac{d}{dt}(\gamma(t)g)\lvert\_{t=0}
$$
(for some curve $\gamma$ satisfying $\gamma(0)=e$, $\dot\gamma(0) = \xi$).

## Trivialisations

The question of trivialisation is actually that of choosing _a representation of the tangent spaces_ to the Lie group $G$ through the Lie algebra $\mathfrak{g}$, using the isomorphisms given by the tangent maps $\dif L_g$ and $\dif R_g$.

_Left-trivialisation_, obviously, represents elements in the tangent space $ T_gG $ as $g \cdot \xi$ for $\xi \in \mathfrak{g}$ (where $\cdot$ is the group-on-Lie algebra action efined previously).

Pinocchio, for instance, uses _left-trivialisations_.

## Lie group exp and log

The Lie group $\exp$ map can be defined as the "natural choice" for a curve $\gamma$ from the Lie algebra to the group when defining derivatives.
We switch notation here, considering $X \in \mathfrak{g} = T_eG$ as a vector field, and $\gamma$ the integral curve of $X$ through $e$, i.e. solving the differential equation:
$$
  \dot\gamma(t) = X(\gamma(t)), \gamma(0) = e.
$$

The Riemannian $\mathrm{Exp}$ in this case is defined through the Lie group exponential map: given $g\in G$ and a tangent vector $\delta g\in T_gG$,
$$
  \mathrm{Exp}_g(\delta g) = g \exp(g^{-1} \cdot \delta g) = \exp(\delta g \cdot g^{-1})g.
$$
The two expressions on the right respectively correspond to a left- and right-trivialisation of the increment $\delta g$.

In Pinocchio, the `integrate(q, v)` function maps a configuration $q\in G$ and left-trivialised increment (or _body-frame velocity_) $v \in \mathfrak{g}$ to
$$
  \mathrm{Exp}_q(q \cdot v) = q \exp(v) = q \oplus v
$$
where the last notation often appears in the robotics literature.

## Some formulas

### Multiplication map

Denote $m(g, h) = g\cdot h$ the multiplication map $m\colon G\times G \rightarrow G$, which is smooth. For $(\xi, \eta) \in \mathfrak{g} \times \mathfrak{g}$, the differential of $m$ is
\begin{equation}
    \dif m_{(g,h)}(\xi, \eta) = \dif R_h\cdot \xi + \dif L_g\cdot \eta.
\end{equation}

### Differential of the inverse

Let $i$ denote the inverse map $i\colon g \mapsto g^{-1}$, which is smooth.
We start by considering $g = e$. Let $\gamma\colon (-\epsilon,\epsilon) \to G$ be a curve, such that $\gamma(0) = e$, $\dot\gamma(0) = v \in \mathfrak{g}$. Then,
$$
  0 = \frac{d}{dt}\gamma(t)\gamma(t)^{-1}\lvert_{t=0} = \gamma(0)\frac{d}{dt}\gamma(t)^{-1}\lvert_{t=0} + \frac{d}{dt}\gamma(t)\lvert_{t=0}\gamma(0)^{-1} = \frac{d}{dt}\gamma(t)^{-1}\lvert_{t=0} + v
$$
so that
$$
  \dif i_e(v) = \frac{d}{dt}\gamma(t)^{-1}\lvert_{t=0} = -v.
$$

Then, for all $g\in G$, $v \in T_gG$,
\begin{equation}
    \dif i_g(v) = - \dif (R_{g^{-1}} \circ L_{g^{-1}})\cdot v.
\end{equation}
If $G \subset \mathrm{GL}_{n}(\RR)$ is a subgroup of the general linear matrix Lie group, then this formula reduces to ($v$ is now a matrix in $\mathfrak{gl}_n(\RR)$):
\begin{equation}
    \dif i_g(v) = - g^{-1} v g^{-1}.
\end{equation}

## The Inner automorphism and the Adjoint map

$$
\begin{equation}
    \Phi_g(h) \triangleq g h g^{-1}
\end{equation}
$$
The derivative of this map at the neutral element $e\in G$, called the adjoint map, is the mapping
$$
\begin{aligned}
    \Ad_g \colon \mathfrak{g} &\longrightarrow \mathfrak{g}
    \\\\
    \xi &\longmapsto \Ad_g(\xi) = (\dif\Phi_g)_e(\xi).
\end{aligned}
$$


## Other resources

On [Maxime Tournier's blog](https://maxime-tournier.github.io/notes/lie-groups.html).

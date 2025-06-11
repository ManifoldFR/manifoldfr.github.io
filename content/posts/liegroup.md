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
  (\dif{L_g})_h \colon T_h G \xrightarrow{\simeq} T\_{gh } G.
$$

Furthermore, it holds that, as functions,
- $L_e = \operatorname{id}$,
- $L\_{gh} = L_g \circ L_h$ for all $g,h\in G$,
- and indeed $L_g^{-1} = L\_{g^{-1}}$ because $L\_{g^{-1}} \circ L_g = L_e = \operatorname{id}$.

Hence $g \mapsto L_g$ is a group homomorphism between $G$ and the automorphism group $\Aut(G)$.

This further implies that for all $g,h\in G$, by the chain rule
$$
\begin{equation}
  (\dif{L_{gh}})_e = \dif (L_g \circ L_h)_e = (\dif{L_g})_h \circ (\dif L_h)_e
\end{equation}
$$
This makes sense: the right factor maps $T_eG \to T_hG$, the left factor maps $T_hG \to T\_{gh} G $.

**Properties on the right-multiplication**

It holds that for all $g,h\in G$,
$$
  R\_{gh} = R_h \circ R_g,
$$
so we have similar properties for the right-multiplication, except that the morphism from the group product on $G$ to composition on $\Aut(G)$ is reversed.

### Group action on the Lie algebra: the adjoint action $\\,\Ad$

We can define a (left) _group action_ of $G$ on its Lie algebra $\mathfrak{g}$ as follows: for $g\in G$ and $\xi \in \mathfrak{g}$,
\begin{equation}
    g \cdot \xi \defeq \dif(R\_{g^{-1}} \circ L_g)_e(\xi) \in \mathfrak{g}.
\end{equation}
In fact, this action is the differential map of the inner automorphism $\Phi_g$ defined by $\Phi_g(h) = g h g^{-1}$, or
$$
  \Phi_g = R\_{g^{-1}} \circ L_g.
$$
Remarking this, we can see that it is indeed an action, because it holds that
$$
  h \cdot (g\cdot \xi) = (hg) \cdot \xi.
$$


This action is called the *adjoint* action, denoted
$$
\begin{aligned}
    \Ad_g \colon \mathfrak{g} &\longrightarrow \mathfrak{g}
    \\\\
    \xi &\longmapsto \Ad_g(\xi) = (\dif\Phi_g)_e(\xi)
\end{aligned}
$$

Note that
$$
\begin{equation}
  \Ad_g(\xi) = (\dif R_g)^{-1}_e \circ (\dif L_g)_e (\xi).
\end{equation}
$$

**Some properties**
- Given $g\in G$, the mapping $\Ad_g$ is a linear automorphism in $\mathfrak g$, with inverse $\Ad_g^{-1} = \Ad_{g^{-1}}$.
- The adjoint action, seen as a mapping $g\in G\mapsto \Ad_g \in \GL(\mathfrak g)$, is a group homomorphism.


## Trivialisations

The question of trivialisation is actually that of choosing _a representation of the tangent spaces_ to the Lie group $G$ through the Lie algebra $\mathfrak{g}$, using the isomorphisms given by the tangent maps $(\dif L_g)_e$ and $(\dif R_g)_e$.

_Left-trivialisation_, obviously, represents elements in the tangent space $ T_gG $ as $g \cdot \xi$ for $\xi \in \mathfrak{g}$.

Pinocchio, for instance, uses _left-trivialisations_.

The tool for going from left- to right-trivialisations is the adjoint action. Indeed, given a vector $v \in T_gG$ expressed simultaneously as $v = (\dif L_g)_e\xi $ with $\xi \in \mathfrak{g}$ the left-trivialisation, and $v = (\dif R_g)_e\eta$ with $\eta$ the right-trivialisation, it holds that:
$$
  v = (\dif L_g)_e\xi = (\dif R_g)_e\eta
$$
thus
$$
\begin{equation}
\boxed{
  \eta = (\dif R_g)^{-1}_e \circ (\dif L_g)_e \xi = \Ad_g(\xi).
}
\end{equation}
$$


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

## Trivialisation and differential calculus

Let $f \colon G \to H$ be a smooth mapping between two Lie groups $G$ and $H$, and $g\in G$. As usual, one can define the tangent map to $f$ at $g$, as the linear mapping
$$
  \dif f_g \colon v \in T_gG \longmapsto \dif f_g(v) \in T\_{f(g)}H.
$$

The machinery of Lie groups and the invariances due to the group structure allow us to rethink of this tangent map as one between the Lie algebras $\mathfrak g$ and $\mathfrak h$.

*Twice* left-trivialisation of the tangent map consists in left-trivialising both the input vector $v$ and the output $w = \dif f_g(v) \in T_hH$ (where $h = f(g)\in H$).

This means writing $v = (\dif L^G_g)_e\xi$, and $w = (\dif L^H_h)_e\eta$. In fact, we can prove there exists a *left-Jacobian* $J\colon \mathfrak g \to \mathfrak h$ such that
$$
  w = \dif f_g(v) = (\dif f_g) \circ (\dif L^G_g)_e = (\dif L^H_h)_e \circ J(\xi),
$$
i.e.
$$
\begin{equation}
\boxed{
  J(\xi) \defeq (\dif L_h^H)_e^{-1} \circ (\dif f_g) \circ (\dif L_g^G)_e.
}
\end{equation}
$$

## Some formulas

### Multiplication map

Denote $m(g, h) = gh$ the multiplication map $m\colon G\times G \rightarrow G$, which is smooth. For $(u, v) \in T_gG \times T_hG$, the differential of $m$ is
\begin{equation}
    \dif m_{(g,h)}(u, v) = (\dif R_h)_g(u) + (\dif L_g)_h(v) \in T\_{gh}G.
\end{equation}

Trivialising the tangent vectors as $u = (\dif L_g)_e\xi$, $v = (\dif L_h)_e \eta$ with $(\xi,\eta) \in \mathfrak{g}\times \mathfrak{g}$, we can now write a left-trivialised Jacobian mapping $J_m(g,h) \colon \mathfrak g \times \mathfrak g \to \mathfrak g$ of $m$:
$$
\begin{equation}
\begin{aligned}
    (\dif L\_{gh})_e
    J_m(g, h) [\xi, \eta] &= \dif m\_{(g,h)}(u,v)
    \\\\
    &=
    (\dif R_h)_g \circ (\dif L_g)_e\xi + (\dif L_g)_h \circ (\dif L_h)_e\eta \\\\
    &= (\dif R_h)_g \circ (\dif R_g)_e \circ \Ad_g(\xi)  + (\dif L\_{gh})_e(\eta) \\\\
    &= (\dif R\_{gh})_e \Ad_g (\xi) + (\dif L\_{gh})_e(\eta).
\end{aligned}
\end{equation}
$$

Thus:
$$
  J_m(g,h)[\xi, \nu] = \Ad\_{gh}^{-1}\circ \Ad_g(\xi) + \eta
    = \Ad_{h}^{-1}(\xi) + \eta.
$$

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


## Other resources

On [Maxime Tournier's blog](https://maxime-tournier.github.io/notes/lie-groups.html).

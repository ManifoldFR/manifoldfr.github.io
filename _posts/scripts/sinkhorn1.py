from re import T
import numpy as np


def sinkhorn(mu, nu, C, eps):
    u = np.zeros_like(mu)
    v = np.empty_like(nu)
    K = np.exp(-C/eps)
    thresh = 1e-9
    max_iter = 4000
    ress_ = []
    for t in range(max_iter):
        u[:] = mu / (K @ v)
        ktu = K.T @ u
        r = v * ktu

        v[:] = nu / ktu
        s = u * (K @ v)
        res_mu = sum(abs(s - mu))
        res_nu = sum(abs(r - nu))
        res = res_mu + res_nu
        ress_.append(res)
        if res < thresh:
            break
    P_opt = np.diag(u) @ K @ np.diag(v)
    return P_opt, u, v, ress_


import matplotlib.pyplot as plt
from scipy.spatial import distance


np.random.seed(42)
xg = np.random.randn(200, 2)
xg[:, 0] = xg[:, 0] * 0.1

ny0 = 60
yg = np.random.rand(ny0, 2) + [1., 0]
yg[:, 1] = yg[:, 1] * 0.45
ny1 = 60
yg = np.concatenate((
    yg, np.random.randn(ny1, 2) * 0.1 + [-1.5, 1.]
), axis=0)
mu = np.ones(xg.shape[0])
mu /= mu.sum()
nu = np.ones(yg.shape[0])
nu /= nu.sum()
Costm = distance.cdist(xg, yg)
epsilon = 0.08
P_opt, _, _, ress_ = sinkhorn(mu, nu, Costm, eps=epsilon)


plt.rcParams['text.usetex'] = True
gs = plt.GridSpec(3, 2)

plt.gcf().set_size_inches(6, 6)
plt.subplot(gs[0, 0])
plt.plot(ress_, lw=1.)
plt.xlabel("Iterates")
plt.ylabel("Residuals $r_k$")
plt.yscale("log")
plt.title("Convergence of Sinkhorn iterations\n"
          r"Residuals are $r_k = \|\gamma 1-\mu\|_1 + \|\gamma^\top 1-\nu\|_1$")
plt.grid(True, axis='y')

plt.subplot(gs[:, 1])
plt.imshow(P_opt)
plt.title("Transport plan $\gamma^\star$")
plt.xlabel("$i$")
plt.ylabel("$j$")


plt.subplot(gs[1:, 0])
sstyle = dict(s=10, edgecolors='k', lw=.4)
plt.scatter(*xg.T, color='C0', label='$x_i$', **sstyle)
plt.scatter(*yg.T, color='C1', label='$y_j$', **sstyle)
thrsh = .4
strength_mat = P_opt * (P_opt > P_opt.max() * thrsh)
iidx, jidx = np.where(strength_mat != 0)
lines = plt.plot([xg[iidx, 0], yg[jidx, 0]], [xg[iidx, 1], yg[jidx, 1]], color='k', ls=':', lw=.9, zorder=0)


handles, labels = plt.gca().get_legend_handles_labels()
handles.append(lines[0])
labels.append("$\mathcal{A}$")


plt.axis('off')
plt.text(0.5, -2.8, r"($\mathcal{A}$ is the set of $[x_i, y_j]$"
         "\nwhere $\gamma_{i,j} > %g\\bar{\gamma}, \\bar{\gamma}=\max \gamma$)" % thrsh,
         wrap=True, horizontalalignment='center')
plt.legend(handles, labels, loc='upper left')

plt.tight_layout()
fig = plt.gcf()
plt.show()



# -*- coding: utf-8 -*-
"""極簡 2D 剛架勁度法（忽略軸向變形以大 A 近似），供圖 4-1 取得真實彎矩圖。"""
import numpy as np


def solve(nodes, members, fixed_dofs, loads, udl=None, EA=1e8):
    """nodes: [(x,y)]；members: [(i,j,EI)]；fixed_dofs: set of (node,dof)；
    loads: {(node,dof): value}；udl: {member_index: q}（局部 +y 方向分佈載重）。
    回傳 (d, member_end_forces[local: (n_i,v_i,m_i,n_j,v_j,m_j)], reactions)。"""
    udl = udl or {}
    n = len(nodes) * 3
    K = np.zeros((n, n)); F = np.zeros(n)
    for (nd, dof), v in loads.items():
        F[nd * 3 + dof] += v
    T_all, k_all, fe_all = [], [], []
    for mi, (i, j, EI) in enumerate(members):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        Lm = np.hypot(x2 - x1, y2 - y1); c, s = (x2 - x1) / Lm, (y2 - y1) / Lm
        k = np.zeros((6, 6))
        a = EA / Lm; b = 12 * EI / Lm ** 3; cc = 6 * EI / Lm ** 2; d = 4 * EI / Lm; e = 2 * EI / Lm
        k[np.ix_([0, 3], [0, 3])] = [[a, -a], [-a, a]]
        k[np.ix_([1, 2, 4, 5], [1, 2, 4, 5])] = [[b, cc, -b, cc], [cc, d, -cc, e], [-b, -cc, b, -cc], [cc, e, -cc, d]]
        T = np.zeros((6, 6)); R = [[c, s, 0], [-s, c, 0], [0, 0, 1]]
        T[:3, :3] = R; T[3:, 3:] = R
        q = udl.get(mi, 0.0)
        fe = np.array([0, q * Lm / 2, q * Lm ** 2 / 12, 0, q * Lm / 2, -q * Lm ** 2 / 12])  # 等效節點力（局部）
        idx = [i * 3, i * 3 + 1, i * 3 + 2, j * 3, j * 3 + 1, j * 3 + 2]
        K[np.ix_(idx, idx)] += T.T @ k @ T
        F[idx] += T.T @ fe
        T_all.append(T); k_all.append(k); fe_all.append(fe)
    fixed = sorted(nd * 3 + dof for nd, dof in fixed_dofs)
    free = [i for i in range(n) if i not in fixed]
    d = np.zeros(n)
    d[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    ends = []
    for mi, (i, j, EI) in enumerate(members):
        idx = [i * 3, i * 3 + 1, i * 3 + 2, j * 3, j * 3 + 1, j * 3 + 2]
        ends.append(k_all[mi] @ (T_all[mi] @ d[idx]) - fe_all[mi])
    Rxn = K @ d - F
    return d, ends, Rxn


def moment_along(end, q, Lm, s):
    """局部座標內力彎矩 M(s) = -m_i + v_i s + q s^2/2（正值：-y 側受拉）。"""
    return -end[2] + end[1] * s + q * s ** 2 / 2

# -*- coding: utf-8 -*-
"""獨立驗算用的小型有限元素求解器（直接勁度法），只給 calcs.py 交叉驗算用。

  Frame：平面剛架元素（每節點 ux、uy、θ），可在元素端點釋放彎矩（內鉸），軸向可設很大（不計軸變）。
  Truss：平面桁架元素（每節點 ux、uy），EA 相同。

三次元素在「節點受集中力」時的節點位移與反力是精確解，所以影響線一律把單位載重放在節點上，
節點取得夠密（梁每 0.25 m 一點），就能逐點驗算教科書與題解的閉合解。
座標：x 向右、y 向上；單位載重向下（−y）；反力向上為正。"""
import numpy as np


class Frame:
    def __init__(self):
        self.xy = []          # 節點座標
        self.el = []          # (i, j, EI, EA, rel_i, rel_j)
        self.fix = {}         # 節點 → (ux, uy, rz) 是否固定

    def node(self, x, y=0.0):
        for k, p in enumerate(self.xy):
            if abs(p[0] - x) < 1e-9 and abs(p[1] - y) < 1e-9:
                return k
        self.xy.append((float(x), float(y)))
        return len(self.xy) - 1

    def member(self, p, q, EI=1.0, EA=1e9, n=1, rel_i=False, rel_j=False):
        """由 p 到 q 切成 n 段；rel_i／rel_j＝起點／終點彎矩釋放（內鉸）。回傳沿線節點編號。"""
        ids = [self.node(p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n) for k in range(n + 1)]
        for k in range(n):
            self.el.append((ids[k], ids[k + 1], EI, EA, rel_i and k == 0, rel_j and k == n - 1))
        return ids

    def support(self, x, y=0.0, ux=False, uy=True, rz=False):
        self.fix[self.node(x, y)] = (ux, uy, rz)

    @staticmethod
    def _klocal(L, EI, EA, ri, rj):
        k = np.zeros((6, 6))
        a = EA / L
        k[0, 0] = k[3, 3] = a; k[0, 3] = k[3, 0] = -a
        c = EI / L ** 3
        kb = c * np.array([[12, 6 * L, -12, 6 * L], [6 * L, 4 * L * L, -6 * L, 2 * L * L],
                           [-12, -6 * L, 12, -6 * L], [6 * L, 2 * L * L, -6 * L, 4 * L * L]])
        idx = [1, 2, 4, 5]
        for r in range(4):
            for s in range(4):
                k[idx[r], idx[s]] = kb[r, s]
        rel = [d for d, flag in ((2, ri), (5, rj)) if flag]
        if rel:   # 靜態凝聚：被釋放的端彎矩＝0
            keep = [d for d in range(6) if d not in rel]
            krr = k[np.ix_(rel, rel)]
            kkr = k[np.ix_(keep, rel)]
            kc = k[np.ix_(keep, keep)] - kkr @ np.linalg.solve(krr, kkr.T)
            k = np.zeros((6, 6))
            k[np.ix_(keep, keep)] = kc
        return k

    def solve(self, loads):
        """loads：{節點: (Fx, Fy, Mz)}。回傳 (位移向量 u[n,3], 反力 R[n,3])。"""
        n = len(self.xy)
        K = np.zeros((3 * n, 3 * n))
        for i, j, EI, EA, ri, rj in self.el:
            (x1, y1), (x2, y2) = self.xy[i], self.xy[j]
            L = np.hypot(x2 - x1, y2 - y1)
            c, s = (x2 - x1) / L, (y2 - y1) / L
            Tm = np.zeros((6, 6))
            r3 = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
            Tm[:3, :3] = Tm[3:, 3:] = r3
            kg = Tm.T @ self._klocal(L, EI, EA, ri, rj) @ Tm
            d = [3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2]
            K[np.ix_(d, d)] += kg
        F = np.zeros(3 * n)
        for nd, v in loads.items():
            F[3 * nd:3 * nd + 3] += v
        fixed = [3 * nd + k for nd, fl in self.fix.items() for k in range(3) if fl[k]]
        # 節點旋轉若只連到被釋放的元素端（不會發生在本書模型），用極小勁度避免奇異
        diag0 = [d for d in range(3 * n) if d % 3 == 2 and abs(K[d, d]) < 1e-12 and d not in fixed]
        for d in diag0:
            K[d, d] = 1.0
        free = [d for d in range(3 * n) if d not in fixed]
        u = np.zeros(3 * n)
        u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
        R = K @ u - F
        return u.reshape(n, 3), R.reshape(n, 3)

    def unit_down(self, nd):
        return self.solve({nd: (0.0, -1.0, 0.0)})


class Truss:
    def __init__(self, nodes, members, supports):
        """nodes：{名: (x,y)}；members：[(名1, 名2)]；supports：{名: (ux固定, uy固定)}。"""
        self.names = list(nodes)
        self.ix = {n: k for k, n in enumerate(self.names)}
        self.xy = np.array([nodes[n] for n in self.names], float)
        self.mem = members
        self.sup = supports

    def solve(self, loads, EA=1.0):
        n = len(self.names)
        K = np.zeros((2 * n, 2 * n))
        geo = []
        for a, b in self.mem:
            i, j = self.ix[a], self.ix[b]
            d = self.xy[j] - self.xy[i]
            L = np.hypot(*d)
            c, s = d / L
            v = np.array([-c, -s, c, s])
            dofs = [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
            K[np.ix_(dofs, dofs)] += EA / L * np.outer(v, v)
            geo.append((dofs, v, L))
        F = np.zeros(2 * n)
        for nm, (fx, fy) in loads.items():
            F[2 * self.ix[nm]] += fx
            F[2 * self.ix[nm] + 1] += fy
        fixed = [2 * self.ix[nm] + k for nm, fl in self.sup.items() for k in range(2) if fl[k]]
        free = [d for d in range(2 * n) if d not in fixed]
        u = np.zeros(2 * n)
        u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
        R = K @ u - F
        N = {m: EA / L * v @ u[dofs] for m, (dofs, v, L) in zip(self.mem, geo)}
        return u.reshape(n, 2), {nm: R[2 * self.ix[nm]:2 * self.ix[nm] + 2] for nm in self.sup}, N

    def force(self, N, a, b):
        return N[(a, b)] if (a, b) in N else N[(b, a)]

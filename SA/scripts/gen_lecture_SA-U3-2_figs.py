#!/usr/bin/env python3
"""gen_lecture_SA-U3-2_figs.py — 產生 study/lecture-SA-U3-2.html 的計算式 SVG 圖解

做法同 gen_lecture_SA-U2-4_figs.py：HTML 內以 <!--FIG:id--> 標記圖位，本腳本只替換標記後
<div class="fig"> 裡的 <svg>…</svg>，圖說與正文不動，可重複執行（兩次結果逐位元相同）。

所有數字由 calcs 段重算並 assert 對照 raw/solutions/ 現行正本（2026-11-08 勘誤後）：
SA-2018-1（8 層牆–構架示意模型）、SA-2019-2（中點反曲點近似法＋等 EI 精確剛架對照）、
SA-2020-4（2 自由度勁度矩陣）、SA-2021-4（剛心法與 3 自由度勁度矩陣兩路徑）、
SA-2023-4（EBF 剛性三角形運動學）。任何一個對不上就停止、不寫檔。

用法：python scripts/gen_lecture_SA-U3-2_figs.py [study/lecture-SA-U3-2.html]
"""
# ======================= svglib.py (same as gen_lecture_SA-U1-2_figs.py) =======================
"""Tiny SVG drawing helpers for structural-analysis lecture figures.

All geometry is in screen px; structural drawings use World(...) to map
metres -> px so that every figure is drawn to scale.  No <marker> elements
are used (arrowheads are explicit polygons) so several SVGs can live inline
in one HTML page without id clashes.
"""
import math

INK = '#37474f'
LOAD = '#c62828'
REAC = '#1565c0'
MOM = '#6a1b9a'
DIM = '#78909c'
GOOD = '#2e7d32'
ORG = '#ef6c00'
GHOST = '#b0bec5'
MUT = '#607d8b'


def f(v):
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class SVG:
    def __init__(self, w, h, title=''):
        self.w, self.h, self.el, self.title = w, h, [], title

    def add(self, s):
        self.el.append(s)

    # ---------- primitives ----------
    def line(self, x1, y1, x2, y2, c=INK, w=2, dash=None, cap='round', op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" '
                 f'stroke-width="{w}" stroke-linecap="{cap}"{d}{o}/>')

    def pl(self, pts, c=INK, w=2, fill='none', dash=None, close=False, op=None, join='round'):
        p = ' '.join(f'{f(x)},{f(y)}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<{tag} points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}" '
                 f'stroke-linejoin="{join}"{d}{o}/>')

    def area(self, pts, fill, op=0.25, c='none', w=0):
        p = ' '.join(f'{f(x)},{f(y)}' for x, y in pts)
        self.add(f'<polygon points="{p}" fill="{fill}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}"/>')

    def rect(self, x, y, w, h, fill='#fff', c=INK, sw=1, rx=0, op=None, dash=None):
        o = f' fill-opacity="{op}"' if op is not None else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}"{o} '
                 f'stroke="{c}" stroke-width="{sw}"{d}/>')

    def circ(self, x, y, r, fill='#fff', c=INK, w=2):
        self.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>')

    def text(self, x, y, t, size=12.5, c=INK, anchor='middle', bold=False, italic=False, raw=False):
        b = ' font-weight="bold"' if bold else ''
        i = ' font-style="italic"' if italic else ''
        tt = t if raw else esc(t)
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{b}{i}>{tt}</text>')

    def halo(self, x, y, t, size=12.5, c=INK, anchor='middle', bold=False):
        """text with white halo for legibility over lines"""
        b = ' font-weight="bold"' if bold else ''
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{b} '
                 f'stroke="#fff" stroke-width="4" paint-order="stroke" stroke-linejoin="round">{esc(t)}</text>')

    # ---------- arrows ----------
    def head(self, x, y, ang, c, L=10, W=4.5):
        """arrowhead with tip at (x,y) pointing along angle ang (screen radians)"""
        ca, sa = math.cos(ang), math.sin(ang)
        bx, by = x - L * ca, y - L * sa
        p1 = (bx + W * sa, by - W * ca)
        p2 = (bx - W * sa, by + W * ca)
        self.add(f'<polygon points="{f(x)},{f(y)} {f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])}" fill="{c}"/>')

    def arrow(self, x1, y1, x2, y2, c=LOAD, w=2.5, L=10, W=4.5, dash=None, both=False):
        ang = math.atan2(y2 - y1, x2 - x1)
        ex, ey = x2 - (L - 2) * math.cos(ang), y2 - (L - 2) * math.sin(ang)
        sx, sy = x1, y1
        if both:
            sx, sy = x1 + (L - 2) * math.cos(ang), y1 + (L - 2) * math.sin(ang)
        self.line(sx, sy, ex, ey, c, w, dash=dash, cap='butt')
        self.head(x2, y2, ang, c, L, W)
        if both:
            self.head(x1, y1, ang + math.pi, c, L, W)

    def moment(self, cx, cy, r, ccw=True, c=MOM, w=2.4, a0=None, span=270):
        """circular moment arrow. ccw in the *screen-visual* sense."""
        if a0 is None:
            a0 = -135 if ccw else -45
        # visual angles: measured from +x, counter-clockwise visually (y up)
        sgn = 1 if ccw else -1
        a1 = a0 + sgn * span
        n = 40
        pts = []
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
        self.pl(pts[:-3], c, w)
        # tangent at end
        a = math.radians(a1)
        tx, ty = -math.sin(a) * sgn, -math.cos(a) * sgn  # derivative wrt angle, y flipped
        ex, ey = pts[-1]
        self.head(ex, ey, math.atan2(ty, tx), c, 9, 4.5)

    # ---------- supports (drawn pointing 'down' then rotated) ----------
    def _g(self, x, y, rot, body):
        self.add(f'<g transform="translate({f(x)},{f(y)}) rotate({rot})">{body}</g>')

    def pin(self, x, y, rot=0, s=1.0, c=INK):
        h, b = 16 * s, 11 * s
        body = (f'<polygon points="0,0 {-b},{h} {b},{h}" fill="#fff" stroke="{c}" stroke-width="2"/>'
                + self._ground(h, b * 1.5, c))
        self._g(x, y, rot, body)
        self.circ(x, y, 3.2 * s, '#fff', c, 1.8)

    def roller(self, x, y, rot=0, s=1.0, c=INK):
        h, b = 13 * s, 10 * s
        r = 3.6 * s
        body = (f'<polygon points="0,0 {-b},{h} {b},{h}" fill="#fff" stroke="{c}" stroke-width="2"/>'
                f'<circle cx="{-b*0.5}" cy="{h+r}" r="{r}" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
                f'<circle cx="{b*0.5}" cy="{h+r}" r="{r}" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
                + self._ground(h + 2 * r, b * 1.6, c))
        self._g(x, y, rot, body)
        self.circ(x, y, 3.2 * s, '#fff', c, 1.8)

    def fixed(self, x, y, rot=0, s=1.0, c=INK, half=16):
        body = f'<line x1="{-half*s}" y1="0" x2="{half*s}" y2="0" stroke="{c}" stroke-width="3"/>'
        for k in range(6):
            xx = -half * s + k * (2 * half * s / 5)
            body += f'<line x1="{f(xx)}" y1="0" x2="{f(xx-6*s)}" y2="{f(8*s)}" stroke="{c}" stroke-width="1.4"/>'
        self._g(x, y, rot, body)

    def _ground(self, y, half, c):
        g = f'<line x1="{-half}" y1="{y}" x2="{half}" y2="{y}" stroke="{c}" stroke-width="2"/>'
        n = 5
        for k in range(n):
            xx = -half + 4 + k * (2 * half - 4) / (n - 1)
            g += f'<line x1="{f(xx)}" y1="{y}" x2="{f(xx-6)}" y2="{y+7}" stroke="{c}" stroke-width="1.3"/>'
        return g

    def hinge(self, x, y, r=5.5, c=INK):
        self.circ(x, y, r, '#fff', c, 2.2)

    def node(self, x, y, r=3.4, c=INK):
        self.circ(x, y, r, '#fff', c, 1.6)

    def wall(self, x, y1, y2, side=1, c=INK):
        """vertical wall line at x; hatching on side (+1 right, -1 left)"""
        self.line(x, y1, x, y2, c, 2.5)
        n = int((y2 - y1) / 9)
        for k in range(n + 1):
            yy = y1 + k * (y2 - y1) / n
            self.line(x, yy, x + side * 7, yy - 6, c, 1.3)

    def dim(self, x1, y1, x2, y2, label, off=0, c=DIM, size=12, lab_off=None):
        """dimension line between two points, offset perpendicular by off px"""
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = -math.sin(ang), math.cos(ang)
        a1, b1 = x1 + nx * off, y1 + ny * off
        a2, b2 = x2 + nx * off, y2 + ny * off
        if off:
            self.line(x1, y1, a1 + nx * 4 * (1 if off > 0 else -1), b1 + ny * 4 * (1 if off > 0 else -1), c, 0.8)
            self.line(x2, y2, a2 + nx * 4 * (1 if off > 0 else -1), b2 + ny * 4 * (1 if off > 0 else -1), c, 0.8)
        self.arrow(a1, b1, a2, b2, c, 1, L=7, W=3, both=True)
        lo = lab_off if lab_off is not None else (-6 if abs(ang) < 1e-6 or abs(abs(ang) - math.pi) < 1e-6 else 0)
        mx, my = (a1 + a2) / 2, (b1 + b2) / 2
        if abs(math.cos(ang)) > 0.5:
            self.halo(mx, my + lo, label, size, c)
        else:
            self.halo(mx - 6, my + 4, label, size, c, anchor='end')

    def render(self, extra_style=''):
        t = f'<title>{esc(self.title)}</title>' if self.title else ''
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" font-family="&quot;Microsoft JhengHei&quot;,&quot;Noto Sans TC&quot;,sans-serif">'
                f'{t}' + ''.join(self.el) + '</svg>')


class World:
    """metres -> px.  y up in world, down on screen."""

    def __init__(self, ox, oy, s, sy=None):
        self.ox, self.oy, self.s = ox, oy, s
        self.sy = s if sy is None else sy

    def __call__(self, x, y=0):
        return self.ox + self.s * x, self.oy - self.sy * y

    def X(self, x):
        return self.ox + self.s * x

    def Y(self, y):
        return self.oy - self.sy * y
# ======================= mech.py =======================
"""Tiny plane-frame direct-stiffness solver (pure Python) + member shape / BMD helpers.

Every number drawn in the U2-4 figures comes from here, so the drawings are
consistent with the hand solutions quoted in the text (asserted in each fig_*).
Conventions: global x right, y up, rotations counter-clockwise positive.
Member local axis i->j; local +y = local x rotated +90 deg.
Member loads act in local -y (i.e. 'downward' for a beam drawn left->right).
"""


def _solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-14:
            raise ValueError('singular stiffness matrix')
        for r in range(n):
            if r != c:
                fct = M[r][c] / piv
                if fct:
                    for k in range(c, n + 1):
                        M[r][k] -= fct * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


class Frame:
    def __init__(self):
        self.N, self.E, self.fix, self.F, self.spr = [], [], {}, {}, []

    def node(self, x, y):
        self.N.append((x, y))
        return len(self.N) - 1

    def el(self, i, j, EI=1.0, EA=1e9, load=None):
        """load: ('udl', w) | ('pt', P, a)  (local -y)"""
        self.E.append(dict(i=i, j=j, EI=EI, EA=EA, load=load))
        return len(self.E) - 1

    def support(self, n, ux=1, uy=1, rz=1):
        self.fix[n] = (ux, uy, rz)

    def load(self, n, fx=0.0, fy=0.0, m=0.0):
        a = self.F.get(n, [0.0, 0.0, 0.0])
        self.F[n] = [a[0] + fx, a[1] + fy, a[2] + m]

    def spring(self, n1, dof, k, n2=None):
        """dof 0/1/2 ; n2=None -> grounded spring"""
        self.spr.append((n1, dof, k, n2))

    # ---- element kinematics ----
    def geom(self, e):
        (x1, y1), (x2, y2) = self.N[e['i']], self.N[e['j']]
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return L, (x2 - x1) / L, (y2 - y1) / L

    @staticmethod
    def kloc(L, EI, EA):
        a, b, c, d, g = EA / L, 12 * EI / L ** 3, 6 * EI / L ** 2, 4 * EI / L, 2 * EI / L
        return [[a, 0, 0, -a, 0, 0], [0, b, c, 0, -b, c], [0, c, d, 0, -c, g],
                [-a, 0, 0, a, 0, 0], [0, -b, -c, 0, b, -c], [0, c, g, 0, -c, d]]

    @staticmethod
    def T(c, s):
        t = [[0.0] * 6 for _ in range(6)]
        for o in (0, 3):
            t[o][o], t[o][o + 1], t[o + 1][o], t[o + 1][o + 1], t[o + 2][o + 2] = c, s, -s, c, 1
        return t

    @staticmethod
    def fef(L, load):
        """fixed-end forces ON the member, local, [Fx,Fy,M]i + [Fx,Fy,M]j"""
        if not load:
            return [0.0] * 6
        if load[0] == 'udl':
            w = load[1]
            return [0, w * L / 2, w * L * L / 12, 0, w * L / 2, -w * L * L / 12]
        P, a = load[1], load[2]
        b = L - a
        return [0, P * b * b * (3 * a + b) / L ** 3, P * a * b * b / L ** 2,
                0, P * a * a * (a + 3 * b) / L ** 3, -P * a * a * b / L ** 2]

    def solve(self):
        n = 3 * len(self.N)
        K = [[0.0] * n for _ in range(n)]
        R = [0.0] * n
        for nd, f in self.F.items():
            for k in range(3):
                R[3 * nd + k] += f[k]
        for e in self.E:
            L, c, s = self.geom(e)
            kl, t, ff = self.kloc(L, e['EI'], e['EA']), self.T(c, s), self.fef(L, e['load'])
            kg = [[sum(t[a][p] * kl[a][b] * t[b][q] for a in range(6) for b in range(6))
                   for q in range(6)] for p in range(6)]
            idx = [3 * e['i'] + k for k in range(3)] + [3 * e['j'] + k for k in range(3)]
            for p in range(6):
                R[idx[p]] -= sum(t[a][p] * ff[a] for a in range(6))
                for q in range(6):
                    K[idx[p]][idx[q]] += kg[p][q]
        for n1, dof, k, n2 in self.spr:
            a = 3 * n1 + dof
            K[a][a] += k
            if n2 is not None:
                b = 3 * n2 + dof
                K[b][b] += k
                K[a][b] -= k
                K[b][a] -= k
        free = [d for d in range(n) if not self.fix.get(d // 3, (0, 0, 0))[d % 3]]
        x = _solve([[K[p][q] for q in free] for p in free], [R[p] for p in free])
        self.D = [0.0] * n
        for d, v in zip(free, x):
            self.D[d] = v
        return self

    def d(self, nd):
        return self.D[3 * nd:3 * nd + 3]

    def end_forces(self, k):
        """local end forces on member k: [Ni,Vi,Mi,Nj,Vj,Mj] (+y local, ccw)"""
        e = self.E[k]
        L, c, s = self.geom(e)
        kl, t, ff = self.kloc(L, e['EI'], e['EA']), self.T(c, s), self.fef(L, e['load'])
        dg = self.d(e['i']) + self.d(e['j'])
        dl = [sum(t[a][b] * dg[b] for b in range(6)) for a in range(6)]
        return [sum(kl[a][b] * dl[b] for b in range(6)) + ff[a] for a in range(6)]

    def M_of(self, k):
        """internal moment M(x) of member k (sagging + , i.e. tension on local -y side)"""
        e = self.E[k]
        L, _, _ = self.geom(e)
        f = self.end_forces(k)
        Mi, Vi, load = f[2], f[1], e['load']

        def M(x):
            m = -Mi + Vi * x
            if load and load[0] == 'udl':
                m -= load[1] * x * x / 2
            elif load:
                m -= load[1] * max(0.0, x - load[2])
            return m
        return M, L

    def shape(self, k, amp, n=60):
        """deformed member polyline (world coords): v'' = M/EI integrated from end i"""
        e = self.E[k]
        L, c, s = self.geom(e)
        t = self.T(c, s)
        dg = self.d(e['i']) + self.d(e['j'])
        dl = [sum(t[a][b] * dg[b] for b in range(6)) for a in range(6)]
        M, _ = self.M_of(k)
        h = L / n
        v, th = dl[1], dl[2]
        vs = [v]
        for m in range(n):
            x0 = m * h
            k1 = M(x0) / e['EI']; k2 = M(x0 + h / 2) / e['EI']; k3 = M(x0 + h) / e['EI']
            v += th * h + h * h * (k1 / 3 + k2 * 2 / 3) / 2     # Simpson-ish 2nd integral
            th += h * (k1 + 4 * k2 + k3) / 6
            vs.append(v)
        err = abs(vs[-1] - dl[4]) + abs(th - dl[5])
        scale = max(1e-9, max(abs(q) for q in dl))
        assert err < 2e-3 * scale + 1e-9, ('shape closure', k, err)
        # remove tiny numerical drift linearly so the end lands exactly on node j
        drift = vs[-1] - dl[4]
        (x1, y1) = self.N[e['i']]
        pts = []
        for m, vv in enumerate(vs):
            xi = m / n
            vv -= drift * xi
            ua = dl[0] + (dl[3] - dl[0]) * xi
            pts.append((x1 + c * xi * L + amp * (ua * c - vv * s),
                        y1 + s * xi * L + amp * (ua * s + vv * c)))
        return pts

    def bmd(self, k, sc, n=60):
        """BMD polygon (world coords) drawn on the tension side; returns (pts, M(x), L)"""
        e = self.E[k]
        L, c, s = self.geom(e)
        M, _ = self.M_of(k)
        (x1, y1) = self.N[e['i']]
        nx, ny = -s, c
        pts = [(x1, y1)]
        for m in range(n + 1):
            x = L * m / n
            off = -M(x) * sc
            pts.append((x1 + c * x + nx * off, y1 + s * x + ny * off))
        pts.append((x1 + c * L, y1 + s * L))
        return pts, M, L

    def bmd_at(self, k, xi, sc):
        """screen-independent: point at fraction xi on member k offset to the BMD line"""
        e = self.E[k]
        L, c, s = self.geom(e)
        M, _ = self.M_of(k)
        (x1, y1) = self.N[e['i']]
        off = -M(xi * L) * sc
        return (x1 + c * xi * L - s * off, y1 + s * xi * L + c * off), M(xi * L)


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))


def frac(v, den=(1, 2, 3, 4, 5, 6, 7, 8, 12, 14, 16, 24, 48, 96)):
    """pretty fraction string for a value known to be a simple rational"""
    for d in den:
        n = round(v * d)
        if abs(n / d - v) < 1e-6:
            if d == 1:
                return f'{n}'
            return f'{n}/{d}'
    return f'{v:.3f}'


def impose(F, vals):
    """set nodal displacements directly (unit-displacement experiments); vals {(node,dof): v}"""
    F.D = [0.0] * (3 * len(F.N))
    for (nd, k), v in vals.items():
        F.D[3 * nd + k] = v
    return F


def node_force(F, nd):
    """resultant global force the members exert ON node nd reversed = force that must be applied"""
    out = [0.0, 0.0, 0.0]
    for k, e in enumerate(F.E):
        if nd not in (e['i'], e['j']):
            continue
        L, c, s = F.geom(e)
        f = F.end_forces(k)
        o = 0 if e['i'] == nd else 3
        out[0] += c * f[o] - s * f[o + 1]
        out[1] += s * f[o] + c * f[o + 1]
        out[2] += f[o + 2]
    return out
# ======================= figs_a.py =======================
"""shared helpers + §0–§2 figures"""
BLUE_D = '#0d47a1'
# ======================= calcs.py =======================
"""本講義所有數字的唯一來源。每個函式以 assert 對照 raw/solutions/ 現行正本（2026-11-08 勘誤後版本）。"""
import numpy as np

NS = 8


def wall_frame(EI=5 / 12, k=1.0, ns=NS):
    """SA-2018-1 示意模型：牆＝ns 層懸臂撓曲梁（樓高 1），構架＝剪力型樓層彈簧 k；連桿使同層同位移。
    回傳 (構架樓層力, 牆樓層力, 合體位移, 牆單獨位移, 構架單獨位移)，外力各層 1。"""
    z = np.arange(1, ns + 1, dtype=float)
    fw = np.array([[min(a, b) ** 2 * (3 * max(a, b) - min(a, b)) / (6 * EI) for b in z] for a in z])
    Kw = np.linalg.inv(fw)
    Kf = np.zeros((ns, ns))
    for s in range(ns):
        Kf[s, s] += k
        if s:
            Kf[s - 1, s - 1] += k; Kf[s, s - 1] -= k; Kf[s - 1, s] -= k
    P = np.ones(ns)
    u = np.linalg.solve(Kw + Kf, P)
    return Kf @ u, Kw @ u, u, fw @ P, np.linalg.solve(Kf, P)


def c2018():
    ff, fw, u, uw, uf = wall_frame()
    exp_f = [-2.44, 0.41, 0.90, 0.98, 0.99, 0.95, 0.71, 1.35]
    exp_w = [3.44, 0.59, 0.10, 0.02, 0.01, 0.05, 0.29, -0.35]
    assert all(abs(a - b) < 0.006 for a, b in zip(ff, exp_f)), ff
    assert all(abs(a - b) < 0.006 for a, b in zip(fw, exp_w)), fw
    assert np.allclose(ff + fw, 1)
    ff2 = wall_frame(EI=5 / 3)[0]          # 另一種換算 3EI/h³ = 5k
    assert all(abs(a - b) < 0.006 for a, b in zip(ff2, [-2.23, -0.46, 0.32, 0.66, 0.77, 0.72, 0.48, 1.88])), ff2
    return dict(ff=ff, fw=fw, u=u, uw=uw, uf=uf, ff2=ff2)


def c2020():
    """SA-2020-4：柱 EI=81920、h=3.2 → k_c=30000；Kw 題給。"""
    EI, h = 81920.0, 3.2
    kc = 12 * EI / h ** 3
    assert abs(kc - 30000) < 1e-6
    Kf = 2 * kc * np.array([[1, -1], [-1, 2]])
    Kw = 30000 * np.array([[1, -2], [-2, 6]])
    P = np.array([60.0, 60.0])
    D = np.linalg.solve(Kf + Kw, P)
    Fw, Ff = Kw @ D, Kf @ D
    assert np.allclose(D, [0.002, 0.001])
    assert np.allclose(Fw, [0, 60]) and np.allclose(Ff, [60, 0])
    Veh = kc * D[1]; Meh = Veh * h / 2
    assert abs(Veh - 30) < 1e-9 and abs(Meh - 48) < 1e-9
    # 「為什麼 bc 為 0」：牆單獨承受一樓 60、構架單獨承受頂層 60，變形相同
    Dw = np.linalg.solve(Kw, [0, 60]); Df = np.linalg.solve(Kf, [60, 0])
    assert np.allclose(Dw, [0.002, 0.001]) and np.allclose(Df, [0.002, 0.001])
    # 照「勁度比」直覺分配會錯：各層牆/構架對角線勁度
    return dict(kc=kc, D=D, Fw=Fw, Ff=Ff, Veh=Veh, Meh=Meh, h=h)


C2021_COLS = {'C1': (-3, -2, 2500), 'C2': (3, -2, 12500), 'C3': (-3, 2, 2500), 'C4': (3, 2, 12500)}


def c2021():
    h = 3.6
    kd, ke = 12 * 9720 / h ** 3, 12 * 48600 / h ** 3
    assert abs(kd - 2500) < 1e-6 and abs(ke - 12500) < 1e-6
    cols = C2021_COLS
    K = sum(c[2] for c in cols.values())
    xr = sum(c[2] * c[0] for c in cols.values()) / K
    yr = sum(c[2] * c[1] for c in cols.values()) / K
    assert (xr, yr) == (2, 0)
    Fy = 4 * 27.0
    Mt = Fy * (0 - xr)
    Kt = sum(c[2] * ((c[1] - yr) ** 2 + (c[0] - xr) ** 2) for c in cols.values())
    assert Kt == 270000 and Mt == -216
    dy, th = Fy / K, Mt / Kt
    assert abs(dy - 0.0036) < 1e-12 and abs(th + 0.0008) < 1e-12
    out = {}
    for n, (x, y, k) in cols.items():
        u = 0 - th * (y - yr); v = dy + th * (x - xr)
        out[n] = dict(u=u, v=v, Vx=k * u, Vy=k * v, k=k, x=x, y=y)
    assert np.allclose([out['C3'][q] for q in ('u', 'v', 'Vx', 'Vy')], [0.0016, 0.0076, 4, 19])
    assert np.allclose([out['C4'][q] for q in ('u', 'v', 'Vx', 'Vy')], [0.0016, 0.0028, 20, 35])
    # 第二路徑：3 自由度勁度矩陣（對原點）直接求解
    Kg = np.zeros((3, 3)); Pg = np.array([0, Fy, 0.0])
    for x, y, k in cols.values():
        a = np.array([[1, 0, -y], [0, 1, x]])
        Kg += k * a.T @ a
    d = np.linalg.solve(Kg, Pg)
    for n, (x, y, k) in cols.items():
        assert abs(d[0] - y * d[2] - out[n]['u']) < 1e-12 and abs(d[1] + x * d[2] - out[n]['v']) < 1e-12
    assert abs(sum(o['Vy'] for o in out.values()) - Fy) < 1e-9 and abs(sum(o['Vx'] for o in out.values())) < 1e-9
    # 若四柱同勁度（對照）：剛心在中央、無扭轉
    return dict(xr=xr, yr=yr, Mt=Mt, Kt=Kt, dy=dy, th=th, cols=out, K=K)


def c2019():
    """SA-2019-2 范倫迪爾桁架近似法（中點反曲點）＋同一桁架的精確剛架解作對照。"""
    a, h, P = 4.0, 6.0, 100.0
    R = 1.5 * P
    xm = [2, 6, 10, 14]
    V = [R - P * sum(1 for xp in (4, 8, 12) if xp < x) for x in xm]
    M = [R * x - P * sum(x - xp for xp in (4, 8, 12) if xp < x) for x in xm]
    assert V == [150, 50, -50, -150] and M == [300, 700, 700, 300]
    Ntop = [-m / h for m in M]; Nbot = [m / h for m in M]
    Vch = [v / 2 for v in V]                       # 上下弦各分一半
    # 上弦節點 F..J：腹桿剪力 = 左右上弦軸力差；腹桿軸力 = 左右上弦剪力差
    Nt = [0] + Ntop + [0]; Vt = [0] + Vch + [0]
    Vpost = [Nt[i + 1] - Nt[i] if i else -Nt[1] for i in range(5)]
    Vpost = [-(Nt[1])] + [Nt[i] - Nt[i + 1] for i in range(1, 5)]
    Npost = [Vt[i] - Vt[i + 1] for i in range(5)]
    Mchord = [abs(v) * a / 2 for v in Vch]
    Mpost = [abs(v) * h / 2 for v in Vpost]
    assert np.allclose(Ntop, [-50, -350 / 3, -350 / 3, -50])
    assert np.allclose(Vpost, [50, 200 / 3, 0, -200 / 3, -50])
    assert np.allclose(Npost, [-75, 50, 50, 50, -75])
    assert np.allclose(Mchord, [150, 50, 50, 150]) and np.allclose(Mpost, [150, 200, 0, 200, 150])
    # 精確解：等 EI 剛接剛架
    F = Frame()
    bot = [F.node(4 * i, 0) for i in range(5)]
    top = [F.node(4 * i, 6) for i in range(5)]
    ch_b = [F.el(bot[i], bot[i + 1]) for i in range(4)]
    ch_t = [F.el(top[i], top[i + 1]) for i in range(4)]
    posts = [F.el(bot[i], top[i]) for i in range(5)]
    F.support(bot[0], 1, 1, 0); F.support(bot[4], 0, 1, 0)
    for i in (1, 2, 3):
        F.load(bot[i], fy=-P)
    F.solve()
    ex_ch = [max(abs(F.end_forces(k)[2]), abs(F.end_forces(k)[5])) for k in ch_b]
    ex_post = [max(abs(F.end_forces(k)[2]), abs(F.end_forces(k)[5])) for k in posts]
    ex_Nt = [F.end_forces(k)[0] * -1 for k in ch_t]   # 以拉為正：Ni 在 i 端的局部 x 力，拉力時為負
    return dict(V=V, M=M, Ntop=Ntop, Nbot=Nbot, Vch=Vch, Vpost=Vpost, Npost=Npost,
                Mchord=Mchord, Mpost=Mpost, ex_ch=ex_ch, ex_post=ex_post, ex_Nt=ex_Nt)


def c2023():
    h, e, L1 = 4.0, 0.6, 4.0
    L = 2 * L1 + e
    F = [600, 450, 300]                      # 由上而下（頂、二、一樓）；每端或合計比例相同
    V3 = F[0]; V2 = F[0] + F[1]; V1 = sum(F)
    Vs = [V1, V2, V3]
    D = [0.06 * v / sum(Vs) for v in Vs]
    th = [d / h for d in D]
    g = [L / e * t for t in th]
    assert np.allclose(D, [0.027, 0.021, 0.012])
    assert np.allclose(g, [0.09675, 0.07525, 0.043])
    # 運動學驗證：左、右剛性三角形各繞底角轉 θ，量連梁兩端位移
    t = 1e-3
    def rotL(x, y): return (x + y * t, y - x * t)
    def rotR(x, y): return (x + y * t, y - (x - L) * t)
    l = rotL(L1, h); r = rotR(L1 + e, h)
    chord = (r[1] - l[1]) / e                 # 連梁弦轉角（逆時針為正）
    gam = chord + t                           # 端點隨三角形順時針轉 t，相對弦的端轉角
    assert abs(gam / t - L / e) < 1e-9 and abs(rotL(0, h)[0] - (rotR(L, h)[0] - L)) < 1e-12
    return dict(h=h, e=e, L=L, L1=L1, Vs=Vs, D=D, th=th, g=g)


def run_all():
    return dict(r2018=c2018(), r2019=c2019(), r2020=c2020(), r2021=c2021(), r2023=c2023())
# ======================= figs.py =======================
BLUE_D = '#0d47a1'
GRN_D = '#1b5e20'
FRM = '#1565c0'     # 構架
WAL = '#ef6c00'     # 剪力牆
R = run_all()


def sg(v, nd=2):
    s = f'{v:+.{nd}f}'
    return s.replace('+', '+').replace('-', '−')


def dist_cols(S, x0, ytop, rowh, ff, fw, sc, labels=True, title_f='構架', title_w='剪力牆', fs=11.5):
    """樓層水平力分布：兩欄（構架｜剪力牆），每欄一條零線、一條外力 F 虛線；回傳總寬"""
    n = len(ff)
    xs = []
    cur = x0
    for vals, col, ttl in ((ff, FRM, title_f), (fw, WAL, title_w)):
        neg = max(0.0, -min(vals)); pos = max(1.0, max(vals))
        z = cur + 18 + neg * sc + (34 if labels else 0) * (neg > 0)
        ybot = ytop + n * rowh
        S.line(z, ytop - 6, z, ybot + 4, INK, 1.4)
        S.line(z + sc, ytop - 6, z + sc, ybot + 4, GHOST, 1.2, dash='5 4')
        S.text(z + sc, ybot + 18, 'F', 11.5, MUT)
        S.text(z, ybot + 18, '0', 11.5, MUT)
        S.text((z + sc / 2), ytop - 14, ttl, 13, col, bold=True)
        for i, v in enumerate(vals):          # i = 0 為一樓，畫在最下面
            yc = ybot - (i + 0.5) * rowh
            w = v * sc
            S.rect(min(z, z + w), yc - rowh * 0.32, abs(w), rowh * 0.64, col, 'none', 0, op=0.85 if v >= 0 else 0.55)
            S.line(z, yc, z + sc, yc, GHOST, 1, dash='3 3')
            if labels:
                if v >= 0:
                    S.halo(z + w + 5, yc + 4, f'{v:.2f}'.replace('-', '−'), fs, col, 'start')
                else:
                    S.text(z + w - 5, yc + 4, f'{v:.2f}'.replace('-', '−'), fs, col, 'end', bold=True)
        right = z + pos * sc + (44 if labels else 10)
        xs.append((cur, right))
        cur = right + 16
    return cur - x0


def floor_labels(S, x, ytop, rowh, n, fs=11):
    for i in range(n):
        S.text(x, ytop + n * rowh - (i + 0.5) * rowh + 4, f'{i + 1}F', fs, MUT, 'end')


def fig_0_1():
    r = R['r2018']
    S = SVG(900, 360, '§0 同一句題文、兩種力學模型')
    S.line(450, 20, 450, 330, GHOST, 1.5, dash='6 5')
    S.text(225, 24, '若牆和構架「變形形狀相同」', 14, INK, bold=True)
    S.text(225, 42, '（兩個剪力型彈簧並聯）→ 每層照勁度 1 : 5', 12, MUT)
    S.text(675, 24, '實際：彎曲型牆 ＋ 剪力型構架', 14, INK, bold=True)
    S.text(675, 42, '（連桿強迫同位移）→ 互制，力沿高度重分配', 12, MUT)
    n = 8; rowh = 27; yt = 78
    lit_f = [1 / 6] * n; lit_w = [5 / 6] * n
    floor_labels(S, 52, yt, rowh, n)
    dist_cols(S, 58, yt, rowh, lit_f, lit_w, 60, labels=False)
    S.text(140, yt + n * rowh + 40, '構架每層 F/6', 12, FRM, bold=True)
    S.text(300, yt + n * rowh + 40, '牆每層 5F/6', 12, WAL, bold=True)
    floor_labels(S, 488, yt, rowh, n)
    dist_cols(S, 492, yt, rowh, r['ff'], r['fw'], 26, labels=False)
    S.halo(675, yt + n * rowh + 40, '構架：1F 反向 −2.44F、8F 1.35F', 12, FRM, bold=True)
    S.halo(675, yt + n * rowh + 58, '牆：1F 3.44F、8F 反向 −0.35F', 12, WAL, bold=True)
    S.text(225, yt + n * rowh + 58, '沿高度均勻 —— 理由一句話就說完', 12, MUT)
    return S.render()


def fig_1_1():
    S = SVG(900, 350, '§1 柱的側向勁度：兩端不轉 vs 頂端自由')
    H = 200; yb = 280; amp = 46
    # (a) fixed-fixed（梁剛性）
    def panel(cx, kind, title, ktxt, note):
        S.text(cx + 40, 26, title, 13.5, INK, bold=True)
        S.line(cx, yb, cx, yb - H, GHOST, 2.2, dash='5 4')
        pts = []
        for m in range(101):
            xi = m / 100
            v = (3 * xi ** 2 - 2 * xi ** 3) if kind == 'ff' else (3 * xi ** 2 - xi ** 3) / 2
            pts.append((cx + amp * v, yb - H * xi))
        S.pl(pts, FRM, 3.2)
        S.fixed(cx, yb, 0, 0.9)
        if kind == 'ff':
            S.rect(cx + amp - 50, yb - H - 9, 100, 9, '#90a4ae', INK, 1)   # 剛性梁：頂端不轉
            S.text(cx + amp - 54, yb - H - 1, '梁 I=∞', 11, MUT, 'end')
            S.circ(cx + amp * 0.5, yb - H * 0.5, 4.5, '#fff', LOAD, 2)
            S.halo(cx + amp * 0.5 + 10, yb - H * 0.5 + 4, '反曲點在中點', 11.5, LOAD, 'start', bold=True)
        S.arrow(cx + amp - 62, yb - H + 14, cx + amp - 6, yb - H + 14, LOAD, 2.5)
        S.text(cx + amp - 66, yb - H + 18, 'V', 13, LOAD, 'end', bold=True)
        S.dim(cx, yb - H - 26, cx + amp, yb - H - 26, 'Δ', 0, DIM, 12)
        # 彎矩圖（畫在柱右方，線性分布）
        bx = cx + 175
        S.line(bx, yb, bx, yb - H, INK, 1.4)
        if kind == 'ff':
            S.pl([(bx, yb), (bx + 34, yb), (bx - 34, yb - H), (bx, yb - H)], MOM, 2)
            S.area([(bx, yb), (bx + 34, yb), (bx, yb - H / 2)], MOM, 0.18)
            S.area([(bx, yb - H / 2), (bx - 34, yb - H), (bx, yb - H)], MOM, 0.18)
            S.text(bx + 38, yb + 4, '6EIΔ/h²', 11, MOM, 'start')
            S.text(bx - 38, yb - H - 6, '6EIΔ/h²', 11, MOM, 'end')
        else:
            S.pl([(bx, yb), (bx + 34, yb), (bx, yb - H)], MOM, 2)
            S.area([(bx, yb), (bx + 34, yb), (bx, yb - H)], MOM, 0.18)
            S.text(bx + 38, yb + 4, '3EIΔ/h²', 11, MOM, 'start')
            S.text(bx + 8, yb - H + 4, '0', 11, MOM, 'start')
        S.text(bx, yb - H - 22, 'M', 12, MOM, bold=True)
        S.text(cx + 60, yb + 30, ktxt, 13, BLUE_D, bold=True)
        S.text(cx + 60, yb + 48, note, 11.5, MUT)
    panel(60, 'ff', '(a) 柱頂接剛性梁：兩端不轉', 'k = 12EI/h³', '構架柱（SA-2020-4、2021-4）')
    panel(350, 'cf', '(b) 柱頂自由轉動（懸臂）', 'k = 3EI/h³', '同 EI、h，只剩 (a) 的 1/4')
    # (c) 並聯/串聯
    cx = 700
    S.text(cx + 80, 26, '(c) 彈簧怎麼組', 13.5, INK, bold=True)
    S.text(cx + 80, 62, '同一層的柱：並聯', 12.5, FRM, bold=True)
    S.text(cx + 80, 82, 'K_層 = Σ k_柱', 12.5, INK)
    S.text(cx + 80, 100, '（同一位移，力相加）', 11, MUT)
    S.text(cx + 80, 140, '上下疊的樓層：串聯', 12.5, FRM, bold=True)
    S.text(cx + 80, 160, '1/K = Σ 1/K_層', 12.5, INK)
    S.text(cx + 80, 178, '（同一剪力，位移相加）', 11, MUT)
    S.text(cx + 80, 218, '兩元件用連桿或剛性樓板', 12.5, WAL, bold=True)
    S.text(cx + 80, 238, '綁成同位移：並聯', 12.5, WAL, bold=True)
    S.text(cx + 80, 258, 'K_總 = K_構架 + K_牆', 12.5, INK)
    S.text(cx + 80, 276, '（矩陣直接相加）', 11, MUT)
    return S.render()


def fig_2_1():
    r = R['r2018']
    S = SVG(900, 400, '§2 剪力型與彎曲型的變形形狀')
    n = 8
    def prof(u):
        return [0.0] + list(u / u[-1])
    curves = [(prof(r['uf']), FRM, '構架單獨（剪力型）', None),
              (prof(r['uw']), WAL, '牆單獨（彎曲型）', None),
              (prof(r['u']), GRN_D, '綁在一起', '7 4')]
    ox, oy, Wd, Hd = 80, 330, 300, 280
    S.line(ox, oy, ox + Wd + 10, oy, INK, 1.4); S.line(ox, oy, ox, oy - Hd - 10, INK, 1.4)
    for i in range(n + 1):
        y = oy - Hd * i / n
        S.line(ox - 4, y, ox, y, INK, 1); S.text(ox - 8, y + 4, f'{i}' if i else '地面', 10.5, MUT, 'end')
    S.text(ox + Wd / 2, oy + 30, '樓層位移 ÷ 頂層位移', 12, MUT)
    S.text(ox + Wd, oy + 16, '1', 10.5, MUT)
    S.text(ox - 8, oy - Hd - 18, '樓', 11, MUT, 'end')
    for pts, col, lab, dash in curves:
        P = [(ox + Wd * u, oy - Hd * i / n) for i, u in enumerate(pts)]
        S.pl(P, col, 3 if not dash else 2.6, dash=dash)
        for p in P[1:]:
            S.circ(p[0], p[1], 3, col, col, 1)
    S.halo(ox + Wd * 0.40, oy - Hd * 0.22, '構架：下部就跑出去', 11.5, FRM, 'start', bold=True)
    S.halo(ox + Wd * 0.03, oy - Hd * 0.60, '牆：上部才甩開', 11.5, WAL, 'start', bold=True)
    S.halo(ox + Wd * 0.52, oy - Hd * 0.52, '合體：下段像牆、上段像構架', 11.5, GRN_D, 'start', bold=True)
    # 右：每層層間位移（各自歸一到最大）
    S.text(690, 30, '每層「層間位移」分布（各自 ÷ 最大值）', 13, INK, bold=True)
    bx, rowh, yt = 520, 30, 60
    def drifts(u):
        d = np.diff(np.r_[0, u]); return d / d.max()
    df, dw = drifts(r['uf']), drifts(r['uw'])
    for i in range(n):
        yc = yt + (n - i - 0.5) * rowh
        S.text(bx - 8, yc + 4, f'{i + 1}F', 11, MUT, 'end')
        S.rect(bx, yc - 11, 150 * df[i], 10, FRM, 'none', 0, op=0.85)
        S.rect(bx, yc + 1, 150 * dw[i], 10, WAL, 'none', 0, op=0.85)
    S.line(bx, yt - 4, bx, yt + n * rowh + 4, INK, 1.2)
    S.rect(bx + 190, yt + 40, 14, 10, FRM, 'none', 0); S.text(bx + 210, yt + 49, '構架：層間位移 ∝ 層剪力', 11.5, FRM, 'start')
    S.text(bx + 210, yt + 66, '→ 往上遞減', 11.5, FRM, 'start')
    S.rect(bx + 190, yt + 110, 14, 10, WAL, 'none', 0); S.text(bx + 210, yt + 119, '牆：層間位移 ∝ 斜率', 11.5, WAL, 'start')
    S.text(bx + 210, yt + 136, '→ 往上遞增', 11.5, WAL, 'start')
    S.text(690, oy + 30, '同一組外力（每層 F），兩條形狀「相反」', 12, MUT)
    return S.render()


def fig_3_1():
    r = R['r2018']
    S = SVG(900, 380, 'SA-2018-1 樓層水平力分布（示意數值）')
    n = 8; rowh = 32; yt = 52
    floor_labels(S, 90, yt, rowh, n, 12)
    w = dist_cols(S, 96, yt, rowh, r['ff'], r['fw'], 44, labels=True, fs=11.5)
    tx = 96 + w + 20
    S.text(tx, 70, '讀圖', 13.5, INK, 'start', bold=True)
    for k, (t, c) in enumerate((('灰虛線 = 外力 F（量尺）', MUT), ('同一層：構架 + 牆 = F', INK),
                                 ('構架反向只在 1F（本模型）', FRM), ('8F 構架 > F，牆反向', FRM),
                                 ('牆在 1F 吃 3.44F', WAL), ('中間樓層牆幾乎不分力', WAL))):
        S.text(tx, 96 + 22 * k, t, 12, c, 'start')
    S.text(tx, 246, '模型：牆 = 8 層懸臂撓曲梁', 11.5, MUT, 'start')
    S.text(tx, 264, '構架 = 樓層彈簧 k', 11.5, MUT, 'start')
    S.text(tx, 282, '「5 倍」取 12EI/h³ = 5k', 11.5, MUT, 'start')
    S.text(tx, 300, '取 3EI/h³ = 5k 時構架 1、2F', 11.5, MUT, 'start')
    S.text(tx, 318, '都反向、8F 達 1.88F', 11.5, MUT, 'start')
    return S.render()


def fig_3_2():
    r = R['r2020']
    S = SVG(900, 380, 'SA-2020-4 兩層牆–構架：誰接走了哪一層的力')
    W = World(110, 318, 38)     # 1 m = 38 px
    h = r['h']
    amp = 0.6 / 0.002           # 2 mm 畫成 0.6 m
    D = [0, r['D'][1], r['D'][0]]   # 地面、1F、頂層位移
    lv = [0, h, 2 * h]
    # 構架原形（灰）與變形（藍）
    for x in (0, 3.2):
        S.line(*W(x, 0), *W(x, 2 * h), GHOST, 2, dash='5 4')
    for s in range(2):
        for x in (0, 3.2):
            pts = []
            for m in range(41):
                xi = m / 40
                v = D[s] + (D[s + 1] - D[s]) * (3 * xi ** 2 - 2 * xi ** 3)
                pts.append(W(x + amp * v, lv[s] + h * xi))
            S.pl(pts, FRM, 3)
        S.line(*W(amp * D[s + 1] - 0.15, lv[s + 1]), *W(3.2 + amp * D[s + 1] + 0.15, lv[s + 1]), INK, 6)
    for x in (0, 3.2):
        S.fixed(*W(x, 0), 0, 0.7)
    # 牆
    wx = 5.6
    S.rect(W.X(wx), W.Y(2 * h), 0.7 * 38, 2 * h * 38, '#fff3e0', GHOST, 1, dash='4 3')
    wp = [W(wx + 0.35 + amp * D[i], lv[i]) for i in range(3)]
    S.pl(wp, WAL, 3)
    for p in wp[1:]:
        S.circ(p[0], p[1], 4, WAL, WAL, 1)
    S.fixed(*W(wx + 0.35, 0), 0, 1.1)
    S.text(W.X(wx + 0.35), W.Y(0) + 34, '剪力牆', 12, WAL, bold=True)
    S.text(W.X(1.6), W.Y(0) + 34, '構架（梁 I=∞）', 12, FRM, bold=True)
    # 連桿
    for s, lab in ((2, 'bc'), (1, 'ef')):
        x1 = W.X(3.2 + amp * D[s]); x2 = wp[s][0]; y = W.Y(lv[s])
        S.line(x1 + 6, y, x2 - 4, y, INK, 2)
        S.circ(x1 + 6, y, 3.5); S.circ(x2 - 4, y, 3.5)
        S.text((x1 + x2) / 2, y - 8, lab, 11.5, INK)
    # 外力
    for s in (1, 2):
        X = W.X(amp * D[s]) - 8; Y = W.Y(lv[s])
        S.arrow(X - 52, Y, X, Y, LOAD, 2.6)
        S.text(X - 56, Y + 4, '60', 12, LOAD, 'end', bold=True)
    S.halo(W.X(3.2 + amp * D[2]) + 46, W.Y(2 * h) - 26, 'Δ₁ = 2 mm', 12, GRN_D, 'middle', bold=True)
    S.halo(W.X(3.2 + amp * D[1]) + 46, W.Y(h) - 26, 'Δ₂ = 1 mm', 12, GRN_D, 'middle', bold=True)
    # 右側：分配表
    tx = 520
    S.text(tx, 40, '解出來的分配（kN）', 13.5, INK, 'start', bold=True)
    rows = [('', '頂層', '一樓'), ('外力', '60', '60'), ('構架接', f"{abs(r['Ff'][0]):.0f}", f"{abs(r['Ff'][1]):.0f}"),
            ('牆接', f"{abs(r['Fw'][0]):.0f}", f"{abs(r['Fw'][1]):.0f}"), ('連桿', 'bc = 0', 'ef = 60 壓')]
    for i, rw in enumerate(rows):
        y = 74 + 26 * i
        cols = (INK, FRM, WAL) if i else (MUT, MUT, MUT)
        S.text(tx, y, rw[0], 12.5, (INK, INK, FRM, WAL, INK)[i], 'start', bold=i in (2, 3))
        S.text(tx + 130, y, rw[1], 12.5, INK)
        S.text(tx + 230, y, rw[2], 12.5, INK)
    S.line(tx, 82, tx + 290, 82, GHOST, 1)
    S.text(tx, 222, '同一個 (2, 1) mm 變形：', 12.5, GRN_D, 'start', bold=True)
    S.text(tx, 244, '構架單獨只推頂層 60 → (2, 1) mm', 12, FRM, 'start')
    S.text(tx, 266, '牆單獨只推一樓 60 → (2, 1) mm', 12, WAL, 'start')
    S.text(tx, 292, '兩者本來就「長得一樣」，', 12, MUT, 'start')
    S.text(tx, 312, '所以頂層連桿不用出力。', 12, MUT, 'start')
    S.text(tx, 340, 'eh 柱：V = 30 kN、兩端 M = 48 kN-m', 12, FRM, 'start', bold=True)
    S.text(W.X(3), 28, f'變形放大 {amp:.0f} 倍（柱形狀為兩端不轉的三次曲線）', 11, MUT)
    return S.render()


def fig_4_1():
    r = R['r2021']
    S = SVG(900, 450, 'SA-2021-4 剛性樓板：剛心、扭矩、變形')
    W = World(150, 215, 34)
    def slab(Wd, amp=0.0, col=INK, dash=None, w=2):
        pts = []
        for (x, y) in ((-4, -3), (4, -3), (4, 3), (-4, 3)):
            u = -r['th'] * (y - r['yr']) * amp; v = (r['dy'] + r['th'] * (x - r['xr'])) * amp
            pts.append(Wd(x + u, y + v))
        S.pl(pts, col, w, dash=dash, close=True)
    # 左：配置
    S.text(W.X(0), 26, '(a) 配置：剛心被 C2、C4 拉到右邊', 13.5, INK, bold=True)
    slab(W, 0, INK, None, 1.8)
    for n, c in r['cols'].items():
        s = 9 if c['k'] == 2500 else 9 * 5 ** 0.5
        X, Y = W(c['x'], c['y'])
        S.rect(X - s / 2, Y - s / 2, s, s, FRM if c['k'] > 2500 else '#90caf9', INK, 1)
        S.text(X + (-14 if c['x'] < 0 else 14), Y + (-12 if c['y'] > 0 else 22), n, 12, INK,
               'end' if c['x'] < 0 else 'start', bold=True)
        S.text(X + (-14 if c['x'] < 0 else 14), Y + (4 if c['y'] > 0 else 6) + (0 if c['y'] > 0 else 0),
               'k' if c['k'] == 2500 else '5k', 11, MUT, 'end' if c['x'] < 0 else 'start')
    X0, Y0 = W(0, 0); Xr, Yr = W(r['xr'], r['yr'])
    S.arrow(X0, Y0 + 48, X0, Y0 - 2, LOAD, 3)
    S.text(X0 - 6, Y0 + 62, '108 kN', 12, LOAD, 'end', bold=True)
    S.text(X0 + 4, Y0 + 62, '（合力在中心）', 11, LOAD, 'start')
    S.circ(Xr, Yr, 6, '#fff', GRN_D, 2.4); S.line(Xr - 9, Yr, Xr + 9, Yr, GRN_D, 1.5); S.line(Xr, Yr - 9, Xr, Yr + 9, GRN_D, 1.5)
    S.text(Xr + 10, Yr - 10, 'CR (2, 0)', 12, GRN_D, 'start', bold=True)
    S.dim(X0, W.Y(-3) + 30, Xr, W.Y(-3) + 30, 'e = 2 m', 0, DIM, 12)
    S.text(W.X(0), W.Y(-3) + 66, 'T = 108 × 2 = 216 kN-m（順時針）', 12.5, MOM, bold=True)
    S.text(W.X(0), W.Y(-3) + 86, 'Kθ = 48k + 60k = 108k', 12, MUT)
    S.text(W.X(0), W.Y(-3) + 104, '（樓板外框僅示意）', 10.5, MUT)
    # 右：變形
    W2 = World(640, 215, 34)
    amp = 0.9 / 0.0076 / 1.0      # 7.6 mm → 0.9 m
    S.text(W2.X(0), 26, f'(b) 樓板位移（放大 {amp:.0f} 倍）', 13.5, INK, bold=True)
    slab(W2, 0, GHOST, '5 4', 1.6)
    slab(W2, amp, GRN_D, None, 2.4)
    for n, c in r['cols'].items():
        X, Y = W2(c['x'], c['y'])
        X2, Y2 = W2(c['x'] + amp * c['u'], c['y'] + amp * c['v'])
        S.circ(X, Y, 3.5, GHOST, GHOST, 1)
        S.arrow(X, Y, X2, Y2, FRM, 2.4, L=8, W=4)
        mm = (c['u'] * 1000, c['v'] * 1000)
        S.halo(X2 + (-10 if c['x'] < 0 else 10), Y2 - 8, f"{n} ({mm[0]:+.1f}, {mm[1]:.1f}) mm".replace('+', '+').replace('-', '−'),
               11.5, BLUE_D, 'end' if c['x'] < 0 else 'start', bold=n in ('C3', 'C4'))
    Xr, Yr = W2(r['xr'], r['yr'])
    S.circ(Xr, Yr, 5, '#fff', GRN_D, 2)
    S.text(W2.X(0), W.Y(-3) + 66, '平移 3.6 mm ＋ 繞 CR 順轉 0.0008 rad', 12.5, GRN_D, bold=True)
    S.text(W2.X(0), W.Y(-3) + 86, '離 CR 遠的弱柱 C1、C3 位移最大（7.6 mm）', 12, MUT)
    S.text(W2.X(0), W.Y(-3) + 104, '剪力 = k × 位移：C3 (4, 19)、C4 (20, 35) kN', 12, FRM, bold=True)
    return S.render()


def viere_hinged():
    """中點放鉸（＝近似法假設）以勁度法解：鉸以兩個重合節點＋平移硬彈簧＋極小轉動彈簧表示"""
    F = Frame()
    bot = [F.node(4 * i, 0) for i in range(5)]
    top = [F.node(4 * i, 6) for i in range(5)]
    mem = []
    def split(i, j, tag):
        (x1, y1), (x2, y2) = F.N[i], F.N[j]
        m1 = F.node((x1 + x2) / 2, (y1 + y2) / 2); m2 = F.node((x1 + x2) / 2, (y1 + y2) / 2)
        a = F.el(i, m1); b = F.el(m2, j)
        F.spring(m1, 0, 1e7, m2); F.spring(m1, 1, 1e7, m2); F.spring(m1, 2, 1e-4, m2)
        mem.append((tag, a, b))
    for i in range(4):
        split(bot[i], bot[i + 1], 'b%d' % i)
    for i in range(4):
        split(top[i], top[i + 1], 't%d' % i)
    for i in range(5):
        split(bot[i], top[i], 'p%d' % i)
    F.support(bot[0], 1, 1, 0); F.support(bot[4], 0, 1, 0)
    for i in (1, 2, 3):
        F.load(bot[i], fy=-100)
    F.solve()
    return F, mem, bot, top


def fig_5_1():
    S = SVG(900, 420, '范倫迪爾桁架：剪力怎麼過一格')
    W = World(80, 330, 34)
    # 左體 A–B–F–G，切在第 2 格中點 x=6
    for (x1, y1, x2, y2) in ((0, 0, 4, 0), (4, 0, 6, 0), (0, 6, 4, 6), (4, 6, 6, 6), (0, 0, 0, 6), (4, 0, 4, 6)):
        S.line(*W(x1, y1), *W(x2, y2), INK, 5)
    for x, y in ((6, 0), (6, 6)):
        S.circ(*W(x, y), 5.5, '#fff', LOAD, 2)
    S.pin(*W(0, 0), 0, 0.9)
    S.arrow(W.X(0), W.Y(0) + 70, W.X(0), W.Y(0) + 22, REAC, 2.8)
    S.text(W.X(0) + 8, W.Y(0) + 62, 'R_A = 150', 12, REAC, 'start', bold=True)
    S.arrow(W.X(4) + 16, W.Y(0) - 56, W.X(4) + 16, W.Y(0) - 8, LOAD, 2.6)
    S.line(W.X(4) + 16, W.Y(0) - 8, W.X(4) + 3, W.Y(0) - 3, LOAD, 1.2)
    S.text(W.X(4) + 22, W.Y(0) - 42, '100（作用在 B）', 12, LOAD, 'start', bold=True)
    # 切口內力（作用在左體上）
    S.arrow(W.X(6) + 54, W.Y(6), W.X(6) + 8, W.Y(6), LOAD, 2.6)
    S.text(W.X(6) + 58, W.Y(6) + 4, 'N = 116.67（壓）', 12, LOAD, 'start', bold=True)
    S.arrow(W.X(6) + 8, W.Y(0), W.X(6) + 54, W.Y(0), REAC, 2.6)
    S.text(W.X(6) + 58, W.Y(0) + 4, 'N = 116.67（拉）', 12, REAC, 'start', bold=True)
    for y in (6, 0):
        S.arrow(W.X(6), W.Y(y) - 6 - 34, W.X(6), W.Y(y) - 8, MOM, 2.4)
        S.text(W.X(6) - 6, W.Y(y) - 30, '25', 12, MOM, 'end', bold=True)
    S.text(W.X(3), 26, '切在第 2 格中點（兩個反曲點 = 兩個鉸）', 13.5, INK, bold=True)
    S.text(W.X(3), 46, 'M_切 = 150×6 − 100×2 = 700 → N = 700/6', 12, MUT)
    S.text(W.X(3), 64, 'V_切 = 150 − 100 = 50 → 上下弦各 25', 12, MUT)
    for t, xx, yy in (('A', 0, 0), ('B', 4, 0), ('F', 0, 6), ('G', 4, 6)):
        S.halo(W.X(xx) - 10, W.Y(yy) - 8, t, 12, INK, 'end', bold=True)
    # 右：對照普通桁架
    tx = 560
    S.text(tx + 140, 96, '同一格，兩種傳剪方式', 13.5, INK, bold=True)
    S.rect(tx, 116, 280, 70, '#e8f5e9', '#a5d6a7', 1, rx=8)
    S.text(tx + 140, 140, '有斜桿（一般桁架）', 12.5, GRN_D, bold=True)
    S.text(tx + 140, 162, '剪力 = 斜桿軸力的垂直分量', 12, INK)
    S.text(tx + 140, 178, '桿件只受軸力', 11.5, MUT)
    S.rect(tx, 200, 280, 86, '#ffebee', '#ef9a9a', 1, rx=8)
    S.text(tx + 140, 224, '無斜桿（范倫迪爾）', 12.5, LOAD, bold=True)
    S.text(tx + 140, 246, '剪力 = 上下弦的「彎曲剪力」', 12, INK)
    S.text(tx + 140, 264, '弦桿端彎矩 = (V/2)(a/2)', 12, INK)
    S.text(tx + 140, 280, '節點必須剛接才撐得住', 11.5, MUT)
    return S.render()


def fig_5_2():
    r = R['r2019']
    F, mem, bot, top = viere_hinged()
    S = SVG(900, 400, 'SA-2019-2 近似法彎矩圖')
    W = World(146, 330, 38)
    for tag, a, b in mem:
        for k in (a, b):
            e = F.E[k]
            S.line(*W(*F.N[e['i']]), *W(*F.N[e['j']]), GHOST, 2.2)
    sc = 0.95 / 200     # 200 kN-m → 0.95 m
    got = {}
    for tag, a, b in mem:
        Mi = F.M_of(a)[0](0.0); Mj = F.M_of(b)[0](F.geom(F.E[b])[0])
        got[tag] = (Mi, Mj)
        for k in (a, b):
            pts, M, L = F.bmd(k, sc)
            S.area([W(*p) for p in pts], MOM, 0.18)
            S.pl([W(*p) for p in pts[1:-1]], MOM, 2)
    # 對帳：端彎矩大小 = 近似法靜力結果
    for i in range(4):
        for t in ('b', 't'):
            Mi, Mj = got['%s%d' % (t, i)]
            assert abs(abs(Mi) - r['Mchord'][i]) < 0.5 and abs(abs(Mj) - r['Mchord'][i]) < 0.5, (t, i, Mi, Mj)
    for i in range(5):
        Mi, Mj = got['p%d' % i]
        assert abs(abs(Mi) - r['Mpost'][i]) < 0.5 and abs(abs(Mj) - r['Mpost'][i]) < 0.5, (i, Mi, Mj)
    S.pin(*W(0, 0), 0, 0.9); S.roller(*W(16, 0), 0, 0.9)
    for t, xx, yy in zip('ABCDEFGHIJ', [0, 4, 8, 12, 16] * 2, [0] * 5 + [6] * 5):
        S.halo(W.X(xx) - 8, W.Y(yy) + (16 if yy == 0 else -8), t, 12, INK, 'end', bold=True)
    # 標值：弦桿端
    for i in range(4):
        S.halo(W.X(4 * i + 0.25), W.Y(6) - 30, f"{r['Mchord'][i]:.0f}", 11.5, MOM, 'start', bold=True)
    for i, v in enumerate(r['Mpost']):
        S.halo(W.X(4 * i) + 34, W.Y(4.8), f"{v:.0f}", 11.5, MOM, 'start', bold=True)
    S.text(W.X(8), 26, '近似法（中點放鉸）彎矩圖，kN-m；B、C、D 各 100 kN ↓', 13.5, INK, bold=True)
    S.text(W.X(8), W.Y(0) + 46, '每根桿都是過中點的反對稱直線；CH 因左右剪力相同而為 0', 12, MUT)
    return S.render()


def fig_6_1():
    r = R['r2023']
    h, e, L, L1 = r['h'], r['e'], r['L'], r['L1']
    S = SVG(900, 360, 'EBF 連梁旋轉角的運動學')
    W = World(70, 300, 52)
    t = 0.045                         # 示意用放大轉角
    def rL(x, y): return (x + y * t, y - x * t)
    def rR(x, y): return (x + y * t, y - (x - L) * t)
    triL = [(0, 0), (0, h), (L1, h)]; triR = [(L, 0), (L, h), (L1 + e, h)]
    for tri in (triL, triR):
        S.pl([W(*p) for p in tri], GHOST, 1.8, dash='5 4', close=True)
    S.line(*W(L1, h), *W(L1 + e, h), GHOST, 1.8, dash='5 4')
    tl = [rL(*p) for p in triL]; tr = [rR(*p) for p in triR]
    for tri in (tl, tr):
        S.area([W(*p) for p in tri], '#90a4ae', 0.35)
        S.pl([W(*p) for p in tri], INK, 2.6, close=True)
    # 連梁：兩端各隨三角形轉 θ（端切線），中間為反對稱 S 形（端轉角固定的三次曲線）
    a = rL(L1, h); b = rR(L1 + e, h)
    pts = []
    for m in range(41):
        xi = m / 40
        x = a[0] + (b[0] - a[0]) * xi
        # Hermite：端點位置 a、b，端斜率 −t（隨三角形順時針轉）
        dx = b[0] - a[0]
        h00, h10, h01, h11 = 2 * xi ** 3 - 3 * xi ** 2 + 1, xi ** 3 - 2 * xi ** 2 + xi, -2 * xi ** 3 + 3 * xi ** 2, xi ** 3 - xi ** 2
        y = h00 * a[1] + h10 * dx * (-t) + h01 * b[1] + h11 * dx * (-t)
        pts.append(W(x, y))
    S.pl(pts, LOAD, 4)
    S.fixed(*W(0, 0), 0, 0.7); S.fixed(*W(L, 0), 0, 0.7)
    S.line(W.X(-0.6), W.Y(0), W.X(L + 0.6), W.Y(0), INK, 1.2)
    # 標註
    S.dim(W.X(0), W.Y(0) + 26, W.X(L1), W.Y(0) + 26, '4 m', 0, DIM, 11.5)
    S.dim(W.X(L1), W.Y(0) + 26, W.X(L1 + e), W.Y(0) + 26, 'e', 0, DIM, 11.5)
    S.dim(W.X(L1 + e), W.Y(0) + 26, W.X(L), W.Y(0) + 26, '4 m', 0, DIM, 11.5)
    S.arrow(W.X(0), W.Y(h) - 18, W.X(h * t), W.Y(h) - 18, GRN_D, 2, L=7, W=3.5)
    S.text(W.X(h * t) + 6, W.Y(h) - 14, 'Δ = hθ', 11.5, GRN_D, 'start', bold=True)
    S.halo(W(*a)[0] - 30, W(*a)[1] - 6, '左端 ↓ 4θ', 11.5, LOAD, 'end', bold=True)
    S.halo(W(*b)[0] + 8, W(*b)[1] - 12, '右端 ↑ 4θ', 11.5, LOAD, 'start', bold=True)
    S.text(W.X(L1 + e / 2), 26, f'剛性三角形各繞底角轉 θ（圖中 θ 放大到 {t} rad）', 13, INK, bold=True)
    tx = 560
    S.text(tx, 80, '連梁要吸收的轉角', 13.5, INK, 'start', bold=True)
    S.text(tx, 106, '兩端相對垂直位移 = (4 + 4)θ', 12, INK, 'start')
    S.text(tx, 128, '弦轉角 = 8θ / e（逆時針）', 12, INK, 'start')
    S.text(tx, 150, '端點隨三角形再轉 θ（順時針）', 12, INK, 'start')
    S.text(tx, 176, 'γ = 8θ/e + θ = (L/e) θ', 13, LOAD, 'start', bold=True)
    S.text(tx, 200, f'L/e = 8.6/0.6 = {L / e:.2f}', 12.5, LOAD, 'start')
    S.text(tx, 236, '極限檢查', 12.5, GRN_D, 'start', bold=True)
    S.text(tx, 258, 'e → L：γ → θ（就是抗彎構架）', 12, INK, 'start')
    S.text(tx, 280, 'e → 0：γ → ∞（同心斜撐，沒有連梁）', 12, INK, 'start')
    return S.render()


def fig_6_2():
    r = R['r2023']
    S = SVG(900, 330, 'SA-2023-4 層剪力 → 層間位移 → 連梁轉角')
    # 左：三層 V、Δ、γ 長條
    labels = ['1 樓', '2 樓', '3 樓（頂）']
    cols = [('層剪力 V（比例）', [v / 150 for v in r['Vs']], [f'{v / 150:.0f}' for v in r['Vs']], FRM, 6),
            ('層間位移 Δ（cm）', [d * 100 for d in r['D']], [f'{d * 100:.1f}' for d in r['D']], GRN_D, 22),
            ('θ = Δ/h（rad）', [t * 1000 for t in r['th']], [f'{t:.5f}'.rstrip('0') for t in r['th']], MUT, 16),
            ('γ = 14.33θ（rad）', [g * 1000 for g in r['g']], [f'{g:.5f}'.rstrip('0') for g in r['g']], LOAD, 1.25)]
    x0 = 120; rowh = 54; yt = 70
    for i in range(3):
        S.text(x0 - 12, yt + (2 - i) * rowh + 32, labels[i], 12, INK, 'end', bold=True)
    for c, (ttl, vals, txts, col, sc) in enumerate(cols):
        cx = x0 + c * 190
        S.text(cx + 70, yt - 10, ttl, 12.5, col, bold=True)
        S.line(cx, yt, cx, yt + 3 * rowh, INK, 1)
        for i in range(3):
            y = yt + (2 - i) * rowh + 18
            S.rect(cx, y, vals[i] * sc, 24, col, 'none', 0, op=0.8)
            S.text(cx + vals[i] * sc + 6, y + 17, txts[i], 12, col, 'start', bold=True)
    S.text(450, yt + 3 * rowh + 34, '各層幾何與連梁 EI 相同 → 樓層勁度相同 → Δ ∝ V：9 : 7 : 4，總和 6 cm', 12.5, INK, bold=True)
    S.text(450, yt + 3 * rowh + 56, '外力每端或兩端合計，比例都是 9 : 7 : 4（答案不變）', 12, MUT)
    return S.render()


def fig_7_1():
    S = SVG(900, 600, '§7 解題決策流程')
    def box(x, y, w, h, t, fill='#e3f2fd', c=FRM, sz=12.5):
        S.rect(x - w / 2, y - h / 2, w, h, fill, c, 1.4, rx=8)
        lines = t.split('\n')
        for k, ln in enumerate(lines):
            S.text(x, y + 4 + (k - (len(lines) - 1) / 2) * 17, ln, sz, INK)
    def dia(x, y, w, h, t):
        S.pl([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], ORG, 1.6, fill='#fff3e0', close=True)
        lines = t.split('\n')
        for k, ln in enumerate(lines):
            S.text(x, y + 4 + (k - (len(lines) - 1) / 2) * 16, ln, 12, INK)
    def lab(x, y, t, a='start'):
        S.text(x, y, t, 11.5, GRN_D, a, bold=True)
    box(450, 34, 330, 40, '題目給一棟「系統」：先畫運動學（誰被迫一起動）')
    dia(450, 118, 300, 84, '構件之間用什麼綁？')
    S.arrow(450, 54, 450, 76, INK, 1.6)
    # 三個分支
    S.arrow(300, 118, 175, 118, INK, 1.6); S.arrow(175, 118, 175, 180, INK, 1.6)
    lab(230, 110, '連桿（只傳軸力）', 'middle')
    S.arrow(450, 160, 450, 196, INK, 1.6); lab(458, 182, '剛性樓板')
    S.arrow(600, 118, 740, 118, INK, 1.6); S.arrow(740, 118, 740, 176, INK, 1.6)
    lab(670, 110, '剛接／剛性區', 'middle')
    # 左支：牆–構架
    dia(175, 222, 220, 80, '有數值勁度矩陣\n或 EI？')
    lab(80, 286, '是')
    S.arrow(120, 254, 96, 300, INK, 1.6)
    box(96, 330, 156, 56, 'K_總 = K_f + K_w\n解 Δ，回代各自力', sz=12)
    lab(240, 286, '否（示意）')
    S.arrow(230, 254, 256, 300, INK, 1.6)
    box(256, 330, 150, 56, '畫形狀：底部牆大\n頂部構架 > F', sz=12)
    # 中支：剛性樓板
    dia(450, 240, 220, 80, '剛心 = 力的作用線？')
    lab(470, 300, '否')
    S.arrow(450, 280, 450, 300, INK, 1.6)
    box(450, 330, 200, 56, '平移 + 扭轉 T = V·e\nKθ = Σk·d²', sz=12)
    S.text(580, 300, '是：只平移', 11.5, GRN_D, 'start', bold=True)
    # 右支：剛接
    dia(740, 222, 220, 80, '題目說「反曲點」\n或「剛性區域」？')
    lab(662, 286, '反曲點')
    S.arrow(690, 262, 672, 300, INK, 1.6)
    box(660, 330, 150, 56, '中點放鉸 → 靜定\n切面 N = M/h、V/2', sz=12)
    lab(812, 286, '剛性區')
    S.arrow(790, 262, 810, 300, INK, 1.6)
    box(812, 330, 150, 56, '剛體轉 θ → 幾何\nγ = (L/e)θ', sz=12)
    # 匯流
    for x in (96, 256, 450, 660, 812):
        S.line(x, 358, x, 420, INK, 1.4)
    S.line(96, 420, 812, 420, INK, 1.4)
    S.arrow(450, 420, 450, 450, INK, 1.6)
    box(450, 486, 520, 56, '回代：每個元件的力 = 自己的勁度 × 共同位移\n逐層檢查 Σ(各元件力) = 外力', '#e8f5e9', GRN_D)
    S.arrow(450, 514, 450, 540, INK, 1.6)
    box(450, 566, 520, 40, '極限檢查：勁度比 → 1 或 ∞ 時答案是否合理', '#f3e5f5', MOM)
    # 中支「是」分支：繞到匯流線
    S.line(560, 240, 572, 240, INK, 1.4)
    S.pl([(560, 240), (572, 240), (572, 420)], INK, 1.4)
    return S.render()


FIGS = {'0-1': fig_0_1, '1-1': fig_1_1, '2-1': fig_2_1, '3-1': fig_3_1, '3-2': fig_3_2,
        '4-1': fig_4_1, '5-1': fig_5_1, '5-2': fig_5_2, '6-1': fig_6_1, '6-2': fig_6_2, '7-1': fig_7_1}


def inject(html):
    import re
    n = 0
    for fid, fn in FIGS.items():
        pat = re.compile(r'(<!--FIG:%s-->\s*<div class="fig">\s*)<svg.*?</svg>' % re.escape(fid), re.S)
        html, k = pat.subn(lambda m: m.group(1) + fn(), html)
        if k != 1:
            raise SystemExit(f'marker FIG:{fid} found {k} times')
        n += k
    return html, n


if __name__ == '__main__':
    import sys, pathlib
    p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                     pathlib.Path(__file__).resolve().parent.parent / 'study' / 'lecture-SA-U3-2.html')
    html, n = inject(p.read_text(encoding='utf-8'))
    p.write_text(html, encoding='utf-8')
    print(f'{p}: {n} figures regenerated')

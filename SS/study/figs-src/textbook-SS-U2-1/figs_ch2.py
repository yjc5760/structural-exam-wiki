# -*- coding: utf-8 -*-
"""第 2 章：全塑化應力塊與 C=T、四題的 ENA vs PNA、M–φ 曲線與中性軸移動。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import _section


def fig2_1():
    s = S20
    W, H = 900, 520
    sc = 6.0
    ytop = 60
    o, ybot, cx = _section(s, 190, ytop, sc)
    yp = ybot - s.ypna * sc
    ye = ybot - s.ybar * sc
    o += L(cx - 120, ye, cx + 120, ye, AC, 1.6, '6 5')
    o += T(cx - 126, ye + 5, 'ENA', 15, AC, 'end')
    o += L(cx - 120, yp, cx + 120, yp, KEY, 2.6)
    o += T(cx - 126, yp + 5, 'PNA', 16, KEY, 'end', 'bold')
    o += T(cx + 22, (ytop + yp) / 2 + 40, f'上方 *A*/2 = {s.A / 2:.2f}', 14, COMP, 'start', 'bold')
    o += T(cx + 22, (yp + ybot) / 2 + 30, f'下方 *A*/2 = {s.A / 2:.2f}', 14, TEN, 'start', 'bold')
    o += dim(cx - 150, ytop, cx - 150, yp, f'{s.H - s.ypna:.2f}', KEY, 0, 15, -1)
    # 應力塊
    sx, scs = 520, 100
    o += L(sx, ytop - 12, sx, ybot + 12, INK, 1.4)
    o += R(sx - scs, ytop, scs, yp - ytop, COMP2, COMP, 2)
    o += R(sx, yp, scs, ybot - yp, TEN2, TEN, 2)
    o += L(sx - 140, yp, sx + 140, yp, KEY, 2.2)
    o += T(sx - scs, ytop - 18, '−*F*_{y}（全壓）', 15, COMP, 'middle', 'bold')
    o += T(sx + scs, ybot + 26, '+*F*_{y}（全拉）', 15, TEN, 'middle', 'bold')
    # 合力位置：上半形心距 PNA = yt，下半 = yc_
    yC = yp - s.yt * sc
    yT = yp + s.yc_ * sc
    o += A(sx + 130, yC, sx + 20, yC, COMP, 3.2, 13)
    o += T(sx + 136, yC + 6, f'*C* = *F*_{{y}}·*A*/2 = {s.Fy * s.A / 2:.1f} tf', 15, COMP, 'start', 'bold')
    o += A(sx + 20, yT, sx + 130, yT, TEN, 3.2, 13)
    o += T(sx + 136, yT + 6, f'*T* = {s.Fy * s.A / 2:.1f} tf', 15, TEN, 'start', 'bold')
    o += dim(sx + 300, yC + 16, sx + 300, yT - 4, '', KEY, 0)
    o += T(sx + 290, (yC + yT) / 2 - 8, f'力臂 {s.arm:.2f}', 15, KEY, 'end', 'bold')
    o += T(sx + 290, (yC + yT) / 2 + 14, f'= {s.yt:.2f} + {s.yc_:.2f}', 14, KEY, 'end')
    o += R(20, 444, 330, 66, KEY2, KEY, 1.4, 10)
    o += T(185, 470, f'*M*_{{p}} = *C* × 力臂 = {s.Mp:,.0f} tf·cm', 15, KEY, 'middle', 'bold')
    o += T(185, 496, f'→ *Z* = *M*_{{p}}/*F*_{{y}} = {s.Z:,.0f} cm^{{3}}', 15, INK, 'middle')
    return svg(W, H, o, 'SS-2020-2 全塑化應力塊與力偶')


def fig2_2():
    cases = [(S20, 'SS-2020-2 非對稱 H'), (S23, 'SS-2023-3 非對稱 I'), (S10, 'SS-2010-1 階梯'), (S05, 'SS-2005-4 T 型')]
    W, H = 900, 420
    o = ''
    box_h, box_w = 230, 150
    for i, (s, t) in enumerate(cases):
        x0 = 20 + i * 222
        bmax = max(r[1] for r in s.rects)
        sc = min(box_h / s.H, box_w / bmax)
        ytop = 92 + (box_h - s.H * sc) / 2
        so, ybot, cx = _section(s, x0 + 90, ytop, sc)
        o += so
        ye, yp = ybot - s.ybar * sc, ybot - s.ypna * sc
        o += L(cx - 88, ye, cx + 88, ye, AC, 2, '6 4')
        o += L(cx - 88, yp, cx + 88, yp, KEY, 2.6)
        o += T(x0 + 90, 62, t, 15, INK, 'middle', 'bold')
        o += T(x0 + 90, 356, f'ENA 距頂 {s.H - s.ybar:.2f}', 14, AC, 'middle')
        o += T(x0 + 90, 378, f'PNA 距頂 {s.H - s.ypna:.2f}', 14, KEY, 'middle', 'bold')
        o += T(x0 + 90, 400, f'PNA 在{s.which_block_pna()[:3] if s is not S10 else "②、③交界"}', 14, MUT, 'middle')
    o += L(250, 18, 290, 18, AC, 2, '6 4') + T(296, 23, 'ENA（形心）', 14, AC)
    o += L(470, 18, 510, 18, KEY, 2.6) + T(516, 23, 'PNA（等面積）', 14, KEY, 'start', 'bold')
    return svg(W, H, o, '四題的 ENA 與 PNA 位置對照')


_MPHI = {}


def _mphi(s):
    if s.name not in _MPHI:
        py = s.phi_y()
        ks = [0.1 * i for i in range(1, 10)] + [1 + 0.25 * i for i in range(0, 37)]
        pts = []
        for k in ks:
            m, yn = s.moment_at_curvature(k * py, n=1500)
            pts.append((k, m / s.My, yn))
        _MPHI[s.name] = [(0, 0, s.ybar)] + pts
    return _MPHI[s.name]


def fig2_3():
    W, H = 900, 420
    pl = Plot(80, 50, 440, 290, 0, 10, 0, 1.6)
    o = pl.axes([0, 1, 2, 4, 6, 8, 10], [0, 0.5, 1.0, 1.27, 1.5], 'φ/φ_{y}', '*M*/*M*_{y}', size=14,
                yfmt=lambda v: f'{v:g}')
    for s, c in ((RECT, TEN), (S20, KEY)):
        pts = _mphi(s)
        o += P([pl.pt(k, m) for k, m, _ in pts], c, 3)
        o += pl.hline(s.f, c=c, w=1.4)
    o += pl.dot(1, 1, AC, 5)
    o += T(pl.X(1) + 10, pl.Y(1) + 22, '*M*_{y}', 15, AC, 'start', 'bold')
    o += T(pl.X(9.8), pl.Y(1.5) - 10, f'矩形 → *f* = {RECT.f:.2f}', 15, TEN, 'end', 'bold')
    o += T(pl.X(9.8), pl.Y(S20.f) + 24, f'SS-2020-2 → *f* = {S20.f:.2f}', 15, KEY, 'end', 'bold')
    o += T(pl.X(5), 30, '(a) 彎矩–曲率：*M*_{p} 是漸近線', 16, INK, 'middle', 'bold')
    # 右：中性軸位置（距底）
    s = S20
    pr = Plot(630, 50, 200, 290, 0, 10, 30, 40)
    o += pr.axes([0, 2, 4, 6, 8, 10], [30, 32, 34, 36, 38, 40], 'φ/φ_{y}', '', size=14)
    pts = _mphi(s)
    o += P([pr.pt(k, yn) for k, _, yn in pts], KEY, 3)
    o += pr.hline(s.ybar, c=AC, w=1.6)
    o += pr.hline(s.ypna, c=KEY, w=1.6)
    o += T(pr.X(10), pr.Y(s.ybar) + 22, f'ENA {s.ybar:.2f}', 14, AC, 'end', 'bold')
    o += T(pr.X(10), pr.Y(s.ypna) - 10, f'PNA {s.ypna:.2f}', 14, KEY, 'end', 'bold')
    o += T(735, 22, '(b) 2020-2 中性軸距底 (cm)', 16, INK, 'middle', 'bold')
    o += T(450, 400, '曲線由 calcs.py 以纖維積分（每個曲率都重新用 Σ*F* = 0 找中性軸）求得', 14, MUT, 'middle')
    return svg(W, H, o, '彎矩曲率關係與中性軸移動')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}

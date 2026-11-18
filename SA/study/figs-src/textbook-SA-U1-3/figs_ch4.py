# -*- coding: utf-8 -*-
"""第 4 章：求最大效應。影響線與面積、輪壓位置、掃描曲線全部由 calcs.py 算出。"""
from figs_common import *  # noqa
from plot import Plot
import calcs as K

Lm, a, LD = K.L, K.a, K.LD
CIRC = ['①', '②', '③', '④']


def fm(v):
    return f(v).replace('-', '−')


def truck(ax, y, x_front, h=38, c=COMP, show=(0, 1, 2, 3), size=14, num=True):
    """卡車輪壓（向下箭頭，尖端在 y）。x_front＝① 號軸位置（m）。"""
    o = ''
    for k, (p, d) in enumerate(zip(K.AXLE_P, K.AXLE_DX)):
        if k not in show:
            continue
        X = ax(x_front + d)
        o += A(X, y - h, X, y - 2, c, 2.4, 10)
        o += T(X, y - h - 6, f'{int(p)}', size, c, 'middle', 'bold')
        if num:
            o += T(X, y - h - 24, CIRC[k], size, c, 'middle')
    return o


def load_bar(ax, y, x1, x2, c, label, n=None):
    """在影響線下方標「均布載重鋪這段」。"""
    o = udl(ax(x1), ax(x2), y, c, 18, n=n)
    o += T(ax(x2) + 10, y - 4, label, 15, c, 'start', 'bold')
    return o


def fig4_1():
    """均布載重：只鋪在同號那一段（懸臂梁的 M_C、V_C）。"""
    W, H = 900, 900
    ax = Ax(90, 44)                   # 13 m → 572 px
    o = ''
    yb = 70
    o += beam(ax, yb, 0, LD, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', -16), (LD, 'D', 16)])
    o += L(ax(a), yb - 12, ax(a), yb + 12, KEY, 3) + T(ax(a), yb - 18, 'C', 16, KEY, 'middle', 'bold')
    t = (0, a, Lm, LD)
    # M_C
    base, sy = 300, 50
    o += il(ax, base, sy, [(0, 0), (a, K.MC_PEAK), (Lm, 0), (LD, K.OH_MC_D)], name='IL *M*_{*C*}', name_x=8, ticks=t,
            vals=[(a, K.MC_PEAK, '2.4 m'), (LD, K.OH_MC_D, '−1.8 m', 'e')])
    o += T(ax(4.6), base - 30, '+12 m²', 16, AC, 'middle', 'bold')
    o += T(ax(11.9), base + 30, '−2.7 m²', 15, COMP, 'middle', 'bold')
    o += load_bar(ax, base + 130, 0, Lm, AC, f'求最大：{f(K.UDL_KN["MC+"])} kN·m', n=14)
    o += load_bar(ax, base + 180, Lm, LD, COMP, f'求最小：{fm(K.UDL_KN["MC-"])} kN·m', n=4)
    # V_C
    base, sy = 560, 120
    vc = [(0, 0), (a, K.VC_LEFT), (a, K.VC_RIGHT), (Lm, 0), (LD, K.OH_VC_D)]
    o += il(ax, base, sy, vc, name='IL *V*_{*C*}', name_x=8, ticks=t,
            vals=[(a, K.VC_LEFT, '−0.6', (-26, 22)), (a, K.VC_RIGHT, '+0.4', (26, -8)), (LD, K.OH_VC_D, '−0.3', 'e')])
    o += T(ax(8.7), base - 28, '+0.8', 15, AC, 'middle', 'bold')
    o += T(ax(4), base + 30, '−1.8', 15, COMP, 'middle', 'bold')
    o += T(ax(11.9), base + 40, '−0.45', 15, COMP, 'middle', 'bold')
    o += load_bar(ax, base + 150, a, Lm, AC, f'求最大：{f(K.UDL_KN["VC+"])} kN', n=6)
    o += load_bar(ax, base + 200, 0, a, COMP, '', n=8)
    o += udl(ax(Lm), ax(LD), base + 200, COMP, 18, n=4)
    o += T(ax(LD) + 10, base + 196, f'求最小：{fm(K.UDL_KN["VC-"])} kN', 15, COMP, 'start', 'bold')
    o += T(ax(8), base + 218, '兩段分開鋪，中間空著', 14, COMP, 'middle')
    o += L(ax(Lm), yb + 30, ax(Lm), 800, STEEL, 1, '3 4') + L(ax(a), yb + 30, ax(a), 800, STEEL, 1, '3 4')
    o += R(90, 822, 720, 62, KEY2, KEY, 1.3, 9)
    o += T(450, 848, '效應 ＝ *w* × 面積（面積有正負）', 16, KEY, 'middle', 'bold')
    o += T(450, 874, f'*w* = {f(K.W_UDL)} kN/m；「全部鋪滿」得 *M*_{{*C*}} = {f(K.UDL_FULL_MC)} kN·m，比最大值少 27', 15, INK, 'middle')
    return svg(W, H, o, '均布載重只鋪同號區')


def fig4_2():
    """三角形影響線上的輪壓列：判定法的來源。"""
    W, H = 900, 560
    ax = Ax(110, 16)                  # 40 m → 640 px
    o = ''
    base, sy = 330, 220
    pts = [(x, K.t4_Nbc(x)) for x in K.T4_X]
    o += il(ax, base, sy, pts, ticks=(0, 10, 40), vals=[(10, 0.75, '0.75', (-30, 4))])
    o += T(ax(0), base + 26, '0', 15, MUT, 'middle') + T(ax(10), base + 26, '*a* = 10', 15, MUT, 'middle') + T(ax(40), base + 26, '*L* = 40', 15, MUT, 'middle')
    xf = 10 - K.AXLE_DX[1]
    # 輪子壓在影響線上
    for k, (p, d) in enumerate(zip(K.AXLE_P, K.AXLE_DX)):
        x = xf + d
        Y = base - sy * K.t4_Nbc(x)
        o += A(ax(x), 82, ax(x), Y - 3, COMP, 2.4, 10)
        o += T(ax(x), 74, f'{int(p)}', 15, COMP, 'middle', 'bold')
        o += T(ax(x), 50, CIRC[k], 15, COMP, 'middle')
    o += T(ax(xf) - 16, 74, 'kN', 15, COMP, 'end')
    o += T(ax(3.4), 160, '左坡：斜率 +*h*/*a*', 15, AC, 'middle', 'bold')
    o += T(ax(28), base - sy * 0.3 - 30, '右坡：斜率 −*h*/*b*', 15, AC, 'middle', 'bold')
    o += A(ax(26), 150, ax(32), 150, INK, 2, 10)
    o += T(ax(26) - 8, 155, '整台車往右挪 *dx*', 15, INK, 'end', 'bold')
    o += R(40, 408, 820, 140, KEY2, KEY, 1.3, 10)
    o += T(450, 436, '左坡上的輪子（合計 *W*_{*L*}）升 (*h*/*a*)*dx*；右坡上的（合計 *W*_{*R*}）降 (*h*/*b*)*dx*', 16, KEY, 'middle', 'bold')
    o += T(450, 466, 'd效應 / d*x* ＝ *h* ( *W*_{*L*}/*a* − *W*_{*R*}/*b* )　→　某一輪越過峰頂時才會由正變負', 16, INK, 'middle')
    o += T(450, 498, '⇒ 臨界輪 *P* 在峰頂：　*W*_{*L*}/*a*　≤　*W*/*L*　≤　(*W*_{*L*} + *P*)/*a*', 17, KEY, 'middle', 'bold')
    o += T(450, 530, '白話：把全車重平均攤到全跨（*W*/*L*），臨界輪就是讓「左坡平均」剛好跨過它的那一輪', 15, INK, 'middle')
    return svg(W, H, o, '輪壓列判定法')


def fig4_3():
    """SA-2004-2：卡車開過 b，N_bc 隨位置的變化（逐 5 mm 掃描，放大在峰值附近）。"""
    W, H = 900, 480
    xs, vs = K.T4_SCAN
    pl = Plot(110, 50, 640, 340, 0, 16, 60, 100)
    o = pl.axes([0, 2, 4, 6, 8, 10, 12, 14, 16], [60, 70, 80, 90, 100], '① 號軸位置（m）', '*N*_{*bc*}（kN）', size=14)
    sel = [(x, v) for x, v in zip(xs, vs) if 0 <= x <= 16 and v >= 60]
    o += P([pl.pt(x, v) for x, v in sel[::4]], AC, 2.6)
    offs = {1: (0, 34), 2: (-84, 0), 3: (30, 34), 4: (0, 34)}
    for k in range(4):
        x = 10 - K.AXLE_DX[k]
        v = K.T4_NBC_TRY[k + 1]
        best = (k + 1) == K.T4_NBC_CR
        col = COMP if best else AC
        o += pl.dot(x, v, col, 6 if best else 4.5)
        dx, dy = offs[k + 1]
        o += T(pl.X(x) + dx, pl.Y(v) + dy, f'{CIRC[k]} 在 b：{f(v)}', 15, col, 'middle', 'bold')
    o += T(pl.X(10.4), pl.Y(64), '每一段都是直線：沒有輪子跨過峰頂時，斜率不變', 15, MUT, 'start')
    o += T(pl.X(8.4), pl.Y(99.3), '最大值只在某一輪壓在峰頂時出現：試 4 個位置就好', 15, KEY, 'start', 'bold')
    return svg(W, H, o, 'N_bc 掃描')


def fig4_4():
    """SA-2007-3：三鉸拱桁架，A_y、A_x、F_FG 影響線與卡車最不利位置。"""
    W, H = 900, 1080
    F = Frame(110, 290, 13.5)         # 48 m → 648 px
    ax = Ax(110, 13.5)
    o = ''
    lab = {'A': (-16, 8), 'B': (16, 8), 'E': (0, -14), 'F': (0, -14), 'G': (0, -14), 'H': (0, -14), 'I': (0, -14),
           'C': (-14, 20), 'D': (14, 20)}
    o += truss_draw(F, K.T7, K.T7_MEM, {'A': 'pin', 'B': 'pin'}, lab, {('F', 'G'): (WARN, 5)})
    o += C(F(24, 17)[0], F(24, 17)[1], 10, 'none', COMP, 2)
    o += T(F(24, 17)[0], F(24, 17)[1] - 40, 'G：左右兩半只靠它相連（第三個鉸）', 15, COMP, 'middle', 'bold')
    o += dim(F(0, 0)[0], 350, F(48, 0)[0], 350, '4 @ 12 m = 48 m', MUT, size=15)
    tk = K.T7_X
    rows = [
        (490, 90, list(zip(tk, K.T7_AY)), 'IL *A*_{*y*}', [(0, 1, '1', 'w')]),
        (620, 110, list(zip(tk, K.T7_AX)), 'IL *A*_{*x*}', [(24, K.T7_AX[2], '12/17', 'n')]),
        (880, 140, list(zip(tk, K.T7_FG)), 'IL *F*_{*FG*}', [(12, K.T7_FG[1], '−81/85', (-34, 18)), (24, K.T7_FG[2], '+42/85', 'n'),
                                                         (36, K.T7_FG[3], '+21/85', 'n')]),
    ]
    for base, sy, pts, nm, vals in rows:
        o += il(ax, base, sy, pts, name=nm, ticks=tk, vals=vals)
    o += T(ax(2), 518, '① 在 E（車頭剛上橋）→ *A*_{*y*} 最大 130.25 kN', 15, COMP, 'start', 'bold')
    # 卡車位置（F_FG）
    xf_c = 12 - K.AXLE_DX[2]
    o += truck(ax, 878, xf_c, h=34, c=COMP, num=False)
    o += T(ax(xf_c) - 14, 860, '③ 在 F → 壓 115.22 kN', 15, COMP, 'end', 'bold')
    xf_t = 24 - K.AXLE_DX[1]
    o += truck(ax, 760, xf_t, h=34, c=AC, num=False)
    o += T(ax(xf_t + 5.4) + 12, 750, '② 在 G → 拉 59.68 kN', 15, AC, 'start', 'bold')
    for x in (12, 24):
        o += L(ax(x), 360, ax(x), 1040, STEEL, 1, '3 4')
    return svg(W, H, o, 'SA-2007-3 影響線')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}

# -*- coding: utf-8 -*-
"""第 9 章：ASD 互制三式與 LRFD 的對照。"""
from plot import *  # noqa
from calcs import ex2019, ex2003, Fa_asd, EX2003


def fig9_1():
    W_, H = 900, 460
    pl = Plot(90, 50, 500, 350, 0, 1.1, 0, 1.1)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0, 0.15, 0.2, 0.4, 0.6, 0.8, 1.0], '彎矩用掉的比例', '軸力用掉的比例', size=14)
    o += P([pl.pt(0, 1), pl.pt(0.9, 0.2), pl.pt(1, 0)], KEY, 3.4)
    o += P([pl.pt(0, 1), pl.pt(1, 0)], WARN, 3.0, dash='9 5')
    o += pl.hline(0.15, 0, 0.85, c=WARN, w=1.2, dash='3 4')
    o += T(pl.X(0.02), pl.Y(0.15) + 20, '*f*_{a}/*F*_{a} = 0.15', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.56), pl.Y(0.62), 'LRFD H1（紫）', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.30), pl.Y(0.52), 'ASD 直線（橘虛）', 15, WARN, 'end', 'bold')
    o += T(pl.X(0.6), pl.Y(0.05), '低軸力區 LRFD 較寬鬆', 14, MUT, 'start')
    lx = 612
    o += R(lx, 60, 278, 330, WARN2, WARN, 1.4, 8)
    o += T(lx + 139, 88, 'ASD 三式各管什麼', 15, WARN, 'middle', 'bold')
    txt = [('① 穩定式（中段）', True), ('*f*_{a}/*F*_{a} ＋ 放大後的 *f*_{b}/*F*_{b}', False),
           ('*F*_{a} 含挫屈、*f*_{b} 乘 *C*_{m}/(1 − *f*_{a}/*F*′_{e})', False),
           ('② 強度式（端部）', True), ('*f*_{a}/0.6*F*_{y} ＋ *f*_{b}/*F*_{b}', False), ('端部不挫屈、不放大', False),
           ('③ *f*_{a}/*F*_{a} ≤ 0.15', True), ('不放大，一條直線就好', False)]
    for k, (s, b) in enumerate(txt):
        o += T(lx + 16, 120 + k * 32, s, 15 if b else 14, WARN if b else INK, 'start', 'bold' if b else None)
    o += T(450, 446, '兩軸都已正規化：ASD 用容許應力、LRFD 用設計強度；兩者大約差 1.5 倍（第 7 章）', 14, MUT, 'middle')
    return svg(W_, H, o, 'ASD 與 LRFD 互制')


def fig9_2():
    a, b = ex2003(), ex2019()
    faFa03 = a['fa'] / Fa_asd(EX2003['L'] / EX2003['ry'], EX2003['Fy'], EX2003['E'])
    st03 = faFa03 + a['Cm'] * a['fbx'] * a['ampx'] / 1.65 + a['Cm'] * a['fby'] * a['ampy'] / 1.875
    sr03 = a['fa'] / 1.5 + a['fbx'] / 1.65 + a['fby'] / 1.875
    W_, H = 900, 360
    o = T(450, 30, '兩題 ASD：誰控制？', 16, INK, 'middle', 'bold')
    groups = [('SS-2003-4', [('穩定式', st03), ('強度式', sr03)]),
              ('SS-2019-3', [('BC 段穩定式', b['stab']), ('BC 段強度式', b['strg']), ('AB 段純彎', b['AB'])])]
    x0, sc = 230, 420 / 1.2
    y = 64
    for g, items in groups:
        o += T(30, y + 20, g, 15, INK, 'start', 'bold')
        mx = max(v for _, v in items)
        for lab, v in items:
            col = COMP if v > 1 else (KEY if v == mx else STEEL)
            o += T(x0 - 10, y + 22, lab, 14.5, INK, 'end')
            o += R(x0, y, v * sc, 30, col, None, 0, 4, op=0.9)
            o += T(x0 + v * sc + 8, y + 22, f'{v:.3f}' + ('　N.G.' if v > 1 else ('　← 控制' if v == mx else '')), 15, col, 'start', 'bold')
            y += 42
        y += 14
    o += L(x0 + sc, 56, x0 + sc, y - 8, COMP, 1.6, '6 4')
    o += T(x0 + sc + 4, 52, '1.0', 14, COMP, 'start', 'bold')
    return svg(W_, H, o, 'ASD 誰控制')


ALL = {'fig9_1': fig9_1, 'fig9_2': fig9_2}

# -*- coding: utf-8 -*-
"""第 9 章：殘留應力與切線模數。"""
from plot import *  # noqa
from calcs import Ie_ratio, yielded_frac, tm_curve, f_avg, SS2024, ss2024_curve, Fcr_lrfd
import math

TENS = '#c62828'   # 殘留拉應力（紅）
CMPS = '#1565c0'   # 殘留壓應力（藍）


def fig9_1():
    W, H = 900, 420
    o = T(220, 28, '(a) 冷卻順序', 16, INK, 'middle', 'bold')
    cx, cy = 220, 200
    bf, d, tf, tw = 260, 240, 22, 14
    sec = [(-bf / 2, -d / 2), (bf / 2, -d / 2), (bf / 2, -d / 2 + tf), (tw / 2, -d / 2 + tf), (tw / 2, d / 2 - tf), (bf / 2, d / 2 - tf),
           (bf / 2, d / 2), (-bf / 2, d / 2), (-bf / 2, d / 2 - tf), (-tw / 2, d / 2 - tf), (-tw / 2, -d / 2 + tf), (-bf / 2, -d / 2 + tf)]
    o += P([(cx + x, cy + y) for x, y in sec], INK, 1.6, fill=STEEL2, close=True)
    for sx in (-1, 1):
        for sy in (-1, 1):
            o += R(cx + sx * bf / 2 - (40 if sx > 0 else 0), cy + sy * d / 2 - (tf if sy > 0 else 0), 40, tf, CMPS, None, 0, op=0.75)
    for sy in (-1, 1):
        o += R(cx - 22, cy + sy * d / 2 - (tf if sy > 0 else 0), 44, tf, TENS, None, 0, op=0.75)
    o += R(cx - tw / 2, cy - d / 2 + tf, tw, d - 2 * tf, TENS, None, 0, op=0.45)
    o += T(cx + bf / 2 + 6, cy - d / 2 - 8, '翼板端：先冷、先定型', 14, CMPS, 'end', 'bold')
    o += T(cx, cy - d / 2 - 30, '翼腹交界：最後才冷，想縮卻被拉住', 14, TENS, 'middle', 'bold')
    o += T(cx, cy + d / 2 + 34, '翼板端部：殘留壓應力（藍）', 14.5, CMPS, 'middle', 'bold')
    o += T(cx, cy + d / 2 + 58, '翼腹交界與腹板：殘留拉應力（紅）', 14.5, TENS, 'middle', 'bold')
    o += L(450, 20, 450, 405, GRID, 1.5)
    # (b) 翼板上的殘留應力分布（線性，±0.3Fy）
    o += T(675, 28, '(b) 翼板上的殘留應力（常用假設）', 16, INK, 'middle', 'bold')
    x0, x1, y0 = 500, 850, 150
    sc = 220
    o += R(x0, y0 - 8, x1 - x0, 16, STEEL2, INK, 1.2)
    o += L(x0, y0 + 110, x1, y0 + 110, MUT, 1.2)
    xm = (x0 + x1) / 2
    pts = [(x0, y0 + 110 + 0.3 * sc), (xm, y0 + 110 - 0.3 * sc), (x1, y0 + 110 + 0.3 * sc)]
    o += P([(x0, y0 + 110)] + pts + [(x1, y0 + 110)], None, fill='#eef3fb', close=True)
    o += P(pts, INK, 2.6)
    o += T(x0 + 4, y0 + 110 + 0.3 * sc + 22, '−0.3*F*_{y}（壓）', 14.5, CMPS, 'start', 'bold')
    o += T(xm, y0 + 110 - 0.3 * sc - 10, '+0.3*F*_{y}（拉）', 14.5, TENS, 'middle', 'bold')
    o += T(675, 380, '自我平衡：合力為零，不改變靜力平衡', 14.5, INK, 'middle')
    o += T(675, 402, '但決定了「誰先降伏」', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '殘留應力的來源')


def fig9_2():
    W, H = 900, 330
    o = ''
    for i, f_ in enumerate((0.70, 0.85, 1.00)):
        cx = 150 + i * 300
        bf, d, tf, tw = 220, 170, 18, 12
        cy = 130
        u = yielded_frac(f_)
        o += T(cx, 30, f'平均壓應力 ≈ {f_avg(f_):.2f}*F*_{{y}}', 16, INK, 'middle', 'bold')
        for sy in (-1, 1):
            yy = cy + sy * d / 2 - (tf if sy > 0 else 0)
            o += R(cx - bf / 2, yy, bf, tf, STEEL3, INK, 1.2)
            w = u * bf / 2
            if w > 0:
                o += R(cx - bf / 2, yy, w, tf, INK, None, 0) + R(cx + bf / 2 - w, yy, w, tf, INK, None, 0)
        o += R(cx - tw / 2, cy - d / 2 + tf, tw, d - 2 * tf, STEEL3, INK, 1.2)
        ry, rx = Ie_ratio(f_, 'y'), Ie_ratio(f_, 'x')
        o += T(cx, 260, f'弱軸 *I*_{{e}}/*I*_{{y}} ≈ {ry:.2f}', 15, COMP, 'middle', 'bold')
        o += T(cx, 286, f'強軸 *I*_{{e}}/*I*_{{x}} ≈ {rx:.2f}', 15, AC, 'middle', 'bold')
    o += T(450, 318, '黑色＝已降伏（切線模數 0，不再提供勁度）。弱軸 ∝ 寬度³，掉得最快（翼板端殘留壓 0.3*F*_{y} 的假設）', 14, MUT, 'middle')
    return svg(W, H, o, '逐步降伏')


def fig9_3():
    W, H = 900, 430
    pl = Plot(90, 50, 600, 310, 0, 2.0, 0, 1.1)
    o = pl.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 0.25, 0.5, 0.7, 1.0], 'λ_{c}', '*F*_{cr} / *F*_{y}')
    o += pl.curve(lambda l: min(1.0, 1 / l ** 2) if l > 0 else 1, 0.01, 2.0, MUT, 2.2, dash='6 4')
    o += T(pl.X(1.55), pl.Y(1 / 1.55 ** 2) - 12, '理想：min(1, 1/λ²)', 14, MUT, 'start')
    for ax, c, lab in (('y', COMP, '切線模數（弱軸）'), ('x', AC, '切線模數（強軸）')):
        pts = [(l, fv) for l, fv in tm_curve(ax) if l <= 2.0]
        o += P([pl.pt(l, fv) for l, fv in pts], c, 3.2)
    o += T(pl.X(0.58), pl.Y(0.58), '弱軸', 15, COMP, 'start', 'bold')
    o += T(pl.X(0.9), pl.Y(0.86), '強軸', 15, AC, 'start', 'bold')
    o += pl.curve(lambda l: Fcr_lrfd(l, 1.0), 0.01, 2.0, KEY, 2.4, dash='3 3')
    o += T(pl.X(0.05), pl.Y(0.38), '規範 0.658^{λ²}（紫點線）', 14, KEY, 'start', 'bold')
    o += pl.hline(0.7, 0, 2.0, WARN, 1.2, '4 4')
    o += T(pl.X(2.0), pl.Y(0.7) - 6, '比例限 0.7*F*_{y}', 14, WARN, 'end', 'bold')
    o += R(710, 90, 180, 150, '#fff', KEY, 1.4, 8)
    for i, s in enumerate(('每個 *f* 都問：', '*f* = (*I*_{e}/*I*)(*f*) / λ²', '反解 λ = √((*I*_{e}/*I*)/*f*)', '逐點畫出曲線', '（本圖由程式算）')):
        o += T(800, 114 + i * 25, s, 14, KEY if i == 1 else INK, 'middle', 'bold' if i == 1 else None)
    o += T(450, 418, '殘留應力只傷中段：λ 很小時整個斷面最後都會降伏（終點仍是 *F*_{y}）；λ 很大時應力不到比例限就挫屈', 14, MUT, 'middle')
    return svg(W, H, o, '切線模數柱曲線')


def fig9_4():
    W, H = 900, 440
    pl = Plot(90, 50, 560, 320, 0, 2.2, 0, 1.1)
    o = pl.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 0.25, 0.5, 0.75, 1.0], 'λ', '*F*_{cr} / *F*_{y}')
    o += pl.curve(lambda l: min(1.0, 1 / l ** 2) if l > 0 else 1, 0.01, 2.2, MUT, 2.2, dash='6 4')
    o += pl.curve(ss2024_curve, 0.001, 2.2, AC, 4, n=600)
    S = SS2024
    for lab, l, v in (('A', S['l1'], 1.0), ('B', S['l2'], 0.5), ('C', S['l3'], 0.5)):
        o += pl.dot(l, v, KEY, 6)
        o += T(pl.X(l) + 6, pl.Y(v) - 10 if lab != 'B' else pl.Y(v) + 24, f'{lab}({l:.3f}, {v:.3f})', 14, KEY, 'start', 'bold')
    o += T(pl.X(0.42), pl.Y(0.70), '0.485/λ²', 15, AC, 'start', 'bold')
    o += T(pl.X(1.2), pl.Y(0.5) - 12, '平台 0.5', 15, AC, 'middle', 'bold')
    o += T(pl.X(1.7), pl.Y(1 / 1.7 ** 2) - 10, '1/λ²', 15, AC, 'start', 'bold')
    o += P([pl.pt(S['l2'], 0.5), pl.pt(S['l3'], S['IeIx'] / 2), pl.pt(S['l3'], 0.5)], COMP, 2, dash='2 4')
    o += T(pl.X(S['l3']) + 6, pl.Y(S['IeIx'] / 2) + 5, '錯解：跳躍（柱變長反而變強，不可能）', 14, COMP, 'start')
    o += R(660, 60, 230, 200, '#fff', KEY, 1.4, 8)
    lines = ['SS-2024-1（強軸）', '外側 4 塊殘留壓 0.5*F*_{y}', '→ *f* = 0.5*F*_{y} 時整塊降伏', '→ *I*_{e}/*I*_{x} = 0.485', '非彈性分支只在 *f* ≥ 0.5 成立',
             '彈性分支只在 *f* ≤ 0.5 成立', '中間兩者皆不成立', '→ 強度鎖在 0.5（平台）']
    for i, s in enumerate(lines):
        o += T(672, 84 + i * 23, s, 14, KEY if i in (0, 7) else INK, 'start', 'bold' if i in (0, 7) else None)
    return svg(W, H, o, 'SS-2024-1')


ALL = {'fig9_1': fig9_1, 'fig9_2': fig9_2, 'fig9_3': fig9_3, 'fig9_4': fig9_4}

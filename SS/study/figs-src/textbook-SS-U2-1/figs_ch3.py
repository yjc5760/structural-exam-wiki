# -*- coding: utf-8 -*-
"""第 3 章：H 型 Z 的兩個力偶、實心圓／圓管、形狀因子排行與圓管 f–d/D 曲線。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import _section


def fig3_1():
    """H 型：翼板力偶 + 腹板力偶（以 SS-2006-3 依比例）。"""
    s = S06
    W, H = 900, 450
    sc = 6.0
    ytop = 50
    o, ybot, cx = _section(s, 210, ytop, sc)
    ym = (ytop + ybot) / 2
    o += L(cx - 110, ym, cx + 110, ym, KEY, 2.4)
    o += T(cx - 116, ym + 5, 'PNA', 15, KEY, 'end', 'bold')
    o += dim(cx + 120, ytop + 2.0 * sc / 2, cx + 120, ybot - 2.0 * sc / 2, '*d* − *t*_{f}', AC, 0, 15, -1)
    o += dim(cx - 130, ytop + 2 * sc, cx - 130, ym, '*h*_{w}/2', MUT, 0, 14, 1)
    o += T(cx, ytop - 14, '*b*_{f} × *t*_{f}', 15, INK, 'middle')
    o += T(cx + 10, ym + 70, '*t*_{w}', 15, INK, 'start')
    # 右：兩個力偶
    bx = 450
    o += R(bx, 40, 430, 170, KEY2, KEY, 1.4, 10)
    o += T(bx + 215, 68, '① 翼板力偶', 16, KEY, 'middle', 'bold')
    o += T(bx + 215, 100, '力 = *F*_{y}*b*_{f}*t*_{f}，力臂 = *d* − *t*_{f}', 15, INK, 'middle')
    o += T(bx + 215, 130, '→ *Z*_{翼} = *b*_{f}*t*_{f}(*d* − *t*_{f})', 16, INK, 'middle', 'bold')
    o += T(bx + 215, 160, f'2006-3：30×2×58 = {30 * 2 * 58:,.0f}', 15, MUT, 'middle')
    o += T(bx + 215, 190, f'（占 {30 * 2 * 58 / s.Z * 100:.0f}%）', 14, MUT, 'middle')
    o += R(bx, 230, 430, 170, AC2, AC, 1.4, 10)
    o += T(bx + 215, 258, '② 腹板力偶（像一個矩形）', 16, AC, 'middle', 'bold')
    o += T(bx + 215, 290, '力 = *F*_{y}*t*_{w}*h*_{w}/2，力臂 = *h*_{w}/2', 15, INK, 'middle')
    o += T(bx + 215, 320, '→ *Z*_{腹} = *t*_{w}*h*_{w}^{2}/4', 16, INK, 'middle', 'bold')
    hw = 56
    o += T(bx + 215, 350, f'2006-3：1.2×56²/4 = {1.2 * hw * hw / 4:,.1f}', 15, MUT, 'middle')
    o += T(bx + 215, 380, f'（占 {1.2 * hw * hw / 4 / s.Z * 100:.0f}%）', 14, MUT, 'middle')
    o += T(450 + 215, 432, f'*Z*_{{x}} = {30 * 2 * 58:,.0f} + {1.2 * hw * hw / 4:,.1f} = {s.Z:,.1f} cm^{{3}}', 16, INK, 'middle', 'bold')
    return svg(W, H, o, 'H 型 Z 由翼板力偶與腹板力偶組成')


def fig3_2():
    W, H = 900, 360
    o = ''
    # 實心圓
    cx, cy, Rr = 170, 180, 120
    o += f'<path d="M{cx - Rr},{cy} A{Rr},{Rr} 0 0 1 {cx + Rr},{cy} Z" fill="{COMP2}" stroke="{COMP}" stroke-width="2"/>'
    o += f'<path d="M{cx - Rr},{cy} A{Rr},{Rr} 0 0 0 {cx + Rr},{cy} Z" fill="{TEN2}" stroke="{TEN}" stroke-width="2"/>'
    o += L(cx - Rr - 20, cy, cx + Rr + 20, cy, KEY, 2.2)
    yc = 4 * Rr / (3 * math.pi)
    o += C(cx, cy - yc, 5, COMP, None) + C(cx, cy + yc, 5, TEN, None)
    o += dim(cx + 30, cy - yc, cx + 30, cy, '4*R*/3π', INK, 0, 15, -1)
    o += T(cx, 34, '實心圓：兩個半圓各自一個合力', 16, INK, 'middle', 'bold')
    o += T(cx, 330, '*Z* = (π*R*^{2}/2)·(2·4*R*/3π) = 4*R*^{3}/3 = *D*^{3}/6', 15, INK, 'middle', 'bold')
    # 圓管 = 外 − 內
    x0 = 470
    o += C(x0 + 60, 180, 62, STEEL2, INK, 1.6)
    o += T(x0 + 60, 270, '外圓 *D*', 15, INK, 'middle')
    o += T(x0 + 140, 190, '−', 30, INK, 'middle', 'bold')
    o += C(x0 + 210, 180, 37, STEEL2, INK, 1.6)
    o += T(x0 + 210, 270, '內圓 *d* = 0.6*D*', 15, INK, 'middle')
    o += T(x0 + 275, 190, '=', 30, INK, 'middle', 'bold')
    o += C(x0 + 350, 180, 62, STEEL3, INK, 1.6) + C(x0 + 350, 180, 37, '#fff', INK, 1.4)
    o += L(x0 + 294, 180, x0 + 418, 180, KEY, 2)
    o += T(x0 + 350, 270, '圓管', 15, INK, 'middle')
    o += T(x0 + 215, 34, '圓管：PNA 都在圓心 → 可以直接相減', 16, INK, 'middle', 'bold')
    o += T(x0 + 215, 330, '*Z* = (*D*^{3} − *d*^{3})/6　但 *S* ≠ *S*_{外} − *S*_{內}', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '實心圓與圓管的塑性模數')


SHAPES = [
    ('理想 I（面積全在兩翼）', 1.0, AC),
    (f'H 型 2006-3', S06.f, AC),
    (f'H 型 2009-3', S09.f, AC),
    (f'BH 2021-3', S21.Z / S21_TABLE_S, AC),
    ('極薄圓管 4/π', 4 / math.pi, WARN),
    ('非對稱 H 2020-2', S20.f, KEY),
    ('非對稱 I 2023-3', S23.f, KEY),
    ('矩形', RECT.f, TEN),
    ('圓管 *d* = 0.6*D*（2013-1）', TUBE06[3], WARN),
    ('實心圓 16/3π', F_CIRCLE, TEN),
    ('階梯 2010-1', S10.f, KEY),
    ('T 型 2005-4', S05.f, KEY),
]


def fig3_3():
    W = 900
    rows = sorted(SHAPES, key=lambda r: r[1])
    H = 60 + len(rows) * 34 + 50
    x0, bw = 300, 470
    pl = Plot(x0, 40, bw, len(rows) * 34, 1.0, 1.85, 0, 1)
    o = ''
    for t in (1.0, 1.2, 1.4, 1.6, 1.8):
        o += L(pl.X(t), 36, pl.X(t), 44 + len(rows) * 34, GRID, 1)
        o += T(pl.X(t), 62 + len(rows) * 34, f'{t:.1f}', 14, MUT, 'middle')
    for i, (nm, fv, c) in enumerate(rows):
        y = 44 + i * 34
        o += T(x0 - 12, y + 19, nm, 14, INK, 'end')
        o += R(pl.X(1.0), y + 4, max(2, pl.X(fv) - pl.X(1.0)), 22, c, None, 0, 4)
        o += T(pl.X(fv) + 8, y + 20, f'{fv:.3f}', 14, c, 'start', 'bold')
    o += T(x0 + bw / 2, 24, '形狀因子 *f* = *Z*/*S*：面積越靠近中性軸，*f* 越大', 16, INK, 'middle', 'bold')
    o += T(x0 + bw / 2, H - 8, '藍＝雙對稱 H、紫＝歷屆非對稱斷面、綠＝實心、橘＝圓管', 14, MUT, 'middle')
    return svg(W, int(H), o, '各斷面形狀因子排行')


def fig3_4():
    W, H = 900, 380
    pl = Plot(90, 40, 540, 270, 0, 1, 1.2, 1.75)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [1.2, 1.3, 1.4, 1.5, 1.6, 1.7], '*d*/*D*', '*f*', size=14,
                yfmt=lambda v: f'{v:.1f}')
    o += pl.curve(lambda r: tube(min(r, 0.9999))[3], 0, 0.999, WARN, 3.2)
    o += pl.hline(F_CIRCLE, c=TEN, w=1.4)
    o += pl.hline(4 / math.pi, c=AC, w=1.4)
    o += pl.dot(0.6, TUBE06[3], KEY, 6)
    o += T(pl.X(0.6) + 12, pl.Y(TUBE06[3]) - 10, f'2013-1：*d* = 0.6*D* → *f* = {TUBE06[3]:.3f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.02), pl.Y(F_CIRCLE) - 10, f'實心圓 {F_CIRCLE:.3f}', 14, TEN, 'start', 'bold')
    o += T(pl.X(0.98), pl.Y(4 / math.pi) - 10, f'極薄管 4/π = {4 / math.pi:.3f}', 14, AC, 'end', 'bold')
    o += R(670, 90, 220, 150, KEY2, KEY, 1.4, 10)
    for i, s in enumerate(['圓管的 *f* 一定介於', '1.273 與 1.698 之間', '算出 1.8 或 1.1', '→ 一定算錯']):
        o += T(780, 122 + i * 30, s, 15, KEY if i < 2 else INK, 'middle', 'bold' if i < 2 else None)
    return svg(W, H, o, '圓管形狀因子隨內外徑比變化')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}

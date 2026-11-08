# -*- coding: utf-8 -*-
"""第 4 章：M–φ 理想化與塑性鉸、塑性區長度、鉸的候選位置、固端-簡支的鉸形成順序。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch2 import _mphi


def fig4_1():
    W, H = 900, 400
    s = S20
    pl = Plot(80, 50, 460, 280, 0, 8, 0, 1.45)
    o = pl.axes([0, 1, 2, 4, 6, 8], [0, 0.5, 1.0, s.f], 'φ/φ_{y}', '*M*/*M*_{y}', size=14, yfmt=lambda v: f'{v:.2f}' if v not in (0, 0.5, 1.0) else f'{v:g}')
    pts = _mphi(s)
    o += P([pl.pt(k, m) for k, m, _ in pts if k <= 8], KEY, 3)
    o += P([pl.pt(0, 0), pl.pt(s.f, s.f), pl.pt(8, s.f)], COMP, 2.6, dash='8 5')
    o += T(pl.X(7.9), pl.Y(s.f) - 12, '理想化：先斜後平', 15, COMP, 'end', 'bold')
    o += T(pl.X(7.9), pl.Y(s.f) + 26, '實際（SS-2020-2 纖維積分）', 14, KEY, 'end')
    o += T(pl.X(4.6), pl.Y(0.55), '平的這一段 = 塑性鉸：', 15, COMP, 'middle', 'bold')
    o += T(pl.X(4.6), pl.Y(0.55) + 24, '*M* 不再增加，轉角一直長', 15, COMP, 'middle')
    # 右：普通鉸 vs 塑性鉸
    bx = 600
    for i, (t, m, c) in enumerate((('普通鉸', '*M* = 0', AC), ('塑性鉸', '*M* = *M*_{p}', COMP))):
        y = 70 + i * 160
        o += R(bx, y, 280, 130, '#fff', c, 2, 12)
        o += T(bx + 140, y + 28, t, 16, c, 'middle', 'bold')
        o += L(bx + 30, y + 78, bx + 128, y + 66, INK, 5) + L(bx + 152, y + 66, bx + 250, y + 78, INK, 5)
        o += C(bx + 140, y + 64, 10, '#fff', c, 2.6)
        if i == 1:
            o += curve_arrow([(bx + 104, y + 46), (bx + 116, y + 38), (bx + 126, y + 46)], COMP, 1.8, 8)
            o += curve_arrow([(bx + 176, y + 46), (bx + 164, y + 38), (bx + 154, y + 46)], COMP, 1.8, 8)
        o += T(bx + 140, y + 112, m + ('，可自由轉' if i == 0 else '，在 *M*_{p} 下轉'), 15, INK, 'middle')
    return svg(W, H, o, '塑性鉸的定義：M–φ 理想化')


def fig4_2():
    W, H = 900, 330
    o = ''
    for i, (nm, fv, c) in enumerate((('矩形 *f* = 1.5', RECT.f, TEN), (f'H 型 *f* = {S06.f:.2f}', S06.f, AC))):
        x0 = 40 + i * 440
        bw = 380
        y0 = 70
        o += T(x0 + bw / 2, 34, f'簡支梁跨中集中載重：{nm}', 16, INK, 'middle', 'bold')
        o += L(x0, y0, x0 + bw, y0, INK, 4)
        o += pin(x0, y0 + 2) + pin(x0 + bw, y0 + 2)
        o += A(x0 + bw / 2, y0 - 40, x0 + bw / 2, y0 - 4, WARN, 2.4, 11)
        # 彎矩圖（三角形，頂點 = Mp）
        mb, mh = y0 + 50, 150
        o += P([(x0, mb), (x0 + bw / 2, mb + mh), (x0 + bw, mb)], c, 2.4, close=True, fill='none')
        zone = plastic_zone_point(fv)
        ymy = mb + mh / fv
        xa, xb = x0 + bw / 2 * (1 - zone), x0 + bw / 2 * (1 + zone)
        o += P([(xa, ymy), (x0 + bw / 2, mb + mh), (xb, ymy)], None, fill=COMP2, close=True)
        o += L(x0, ymy, x0 + bw, ymy, AC, 1.4, '5 4')
        o += T(x0 + bw + 6, ymy - 4 if i else ymy + 5, '*M*_{y}', 14, AC, 'start')
        o += L(x0, mb + mh, x0 + bw, mb + mh, KEY, 1.4, '5 4')
        o += T(x0 + bw + 6, mb + mh + 14 if i else mb + mh + 5, '*M*_{p}', 14, KEY, 'start')
        o += dim(xa, mb + mh + 24, xb, mb + mh + 24, f'塑性區 {zone:.3f}*L*', COMP, 0, 15, 1, weight='bold')
    return svg(W, H, o, '塑性區長度：矩形與 H 型')


def _beam_icon(x, y, w, kind):
    o = L(x, y, x + w, y, INK, 4)
    hinges = []
    if kind == 'pc':      # 左固定、右簡支、集中
        o += f'<rect x="{x - 10}" y="{y - 26}" width="10" height="52" fill="{STEEL3}" stroke="{INK}"/>'
        o += pin(x + w, y + 2)
        o += A(x + w * 0.4, y - 40, x + w * 0.4, y - 4, WARN, 2.2, 10)
        hinges = [x + 8, x + w * 0.4]
    elif kind == 'cont':  # 兩跨連續
        o += pin(x, y + 2) + pin(x + w / 2, y + 2) + pin(x + w, y + 2)
        for i in range(12):
            xx = x + 8 + i * (w - 16) / 11
            o += A(xx, y - 30, xx, y - 4, WARN, 1.4, 7)
        hinges = [x + w / 2, x + w * 0.21, x + w * 0.79]
    elif kind == 'step':  # 變斷面
        o = L(x, y, x + w * 0.55, y, INK, 7) + L(x + w * 0.55, y, x + w, y, INK, 3.4)
        o += pin(x, y + 4) + pin(x + w, y + 2)
        o += A(x + w * 0.35, y - 40, x + w * 0.35, y - 5, WARN, 2.2, 10)
        hinges = [x + w * 0.55]
    elif kind == 'frame':
        hh = 70
        o = L(x, y + 10, x, y - hh, INK, 4) + L(x, y - hh, x + w, y - hh, INK, 4) + L(x + w, y - hh, x + w, y + 10, INK, 4)
        o += hatch_ground(x - 16, y + 10, 32) + hatch_ground(x + w - 16, y + 10, 32)
        o += A(x - 44, y - hh, x - 6, y - hh, WARN, 2.2, 10)
        hinges = [(x + 10, y - hh + 8), (x + w - 10, y - hh + 8), (x + 1, y + 2), (x + w - 1, y + 2)]
    for h in hinges:
        hx, hy = (h if isinstance(h, tuple) else (h, y))
        o += C(hx, hy, 8, '#fff', COMP, 2.6)
    return o


def fig4_3():
    W, H = 900, 300
    items = [('pc', '① 固定端 ＋ 集中載重點'), ('cont', '② 內支承 ＋ 均佈跨內極值'), ('step', '③ 斷面變小處'), ('frame', '④ 梁柱節點、柱腳')]
    o = ''
    for i, (k, t) in enumerate(items):
        x0 = 30 + i * 222
        o += _beam_icon(x0 + 14, 170, 160, k)
        o += T(x0 + 94, 250, t, 15, INK, 'middle', 'bold')
    o += T(450, 40, '紅圈 = 鉸的候選位置：彎矩圖的「尖點、端點、極值點」，或 *M*_{p} 突然變小的地方', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, '塑性鉸的常見位置')


def fig4_4():
    W, H = 900, 420
    pl = Plot(90, 50, 560, 300, 0, 1, -1.2, 1.2)
    o = pl.axes([0, 0.25, X_PROP, 0.5, 0.75, 1.0], [-1, -0.5, 0, 0.5, 1], '*x*/*L*', '*M*/*M*_{p}', size=14,
                xfmt=lambda v: f'{v:.3f}' if abs(v - X_PROP) < 1e-6 else f'{v:g}')
    o += pl.hline(1, c=KEY, w=1.4) + pl.hline(-1, c=KEY, w=1.4)
    o += pl.hline(0, c=INK, w=1, dash=None)
    w1 = W_FIRST_HINGE
    o += pl.curve(lambda x: 3 * w1 / 8 * x - w1 * x * x / 2, 0, 1, AC, 2.8)
    wc = COEF_PC_U
    o += pl.curve(lambda x: (wc / 2 - 1) * x - wc * x * x / 2, 0, 1, COMP, 3.2)
    o += pl.dot(1, -1, AC, 6) + pl.dot(X_PROP, 1, COMP, 6) + pl.dot(1, -1, COMP, 4)
    o += T(pl.X(0.03), pl.Y(-0.3), '① 藍線 *w* = 8*M*_{p}/*L*^{2}：固端先到 −*M*_{p}', 14, AC, 'start', 'bold')
    o += T(pl.X(0.03), pl.Y(-0.3) + 22, '　（跨內最大只有 0.56*M*_{p}）', 14, AC, 'start')
    o += T(pl.X(X_PROP), pl.Y(1) - 12, f'② 紅線 *w* = {wc:.2f}*M*_{{p}}/*L*^{{2}}：跨內也到 *M*_{{p}} → 崩塌', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.02), pl.Y(-0.9), '左端：簡支（*x* = 0）', 14, MUT, 'start')
    o += T(pl.X(0.98), pl.Y(-1.12), '右端：固定', 14, MUT, 'end')
    o += R(690, 110, 200, 180, KEY2, KEY, 1.4, 10)
    for i, s_ in enumerate(['一次靜不定', '第 1 個鉸：變靜定', '第 2 個鉸：變機構', f'中間儲備 {RESERVE:.3f} 倍']):
        o += T(790, 144 + i * 36, s_, 15, KEY if i in (0, 3) else INK, 'middle', 'bold' if i in (0, 3) else None)
    return svg(W, H, o, '固端-簡支梁均佈載重下塑性鉸的形成順序')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}

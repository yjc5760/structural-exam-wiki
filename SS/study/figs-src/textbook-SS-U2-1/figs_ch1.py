# -*- coding: utf-8 -*-
"""第 1 章：σ–ε 兩段線、應力由三角形長成矩形、ENA 與 M_y、平行軸定理的貢獻。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig1_1():
    """理想彈—完全塑性 vs 實際軟鋼（示意）。橫軸以 εy 為單位。"""
    W, H = 900, 400
    pl = Plot(90, 50, 560, 280, 0, 16, 0, 1.4)
    o = pl.axes([0, 1, 4, 8, 12, 16], [0, 0.5, 1.0], 'ε/ε_{y}', 'σ/*F*_{y}', size=14)
    # 實際（示意）：彈性 → 平台到 10εy → 硬化
    def real(e):
        if e <= 1:
            return e
        if e <= 10:
            return 1.0
        return min(1.0 + 0.30 * (1 - math.exp(-(e - 10) / 4)), 1.4)
    o += pl.curve(real, 0, 16, STEEL, 2.6, '7 5')
    o += P([pl.pt(0, 0), pl.pt(1, 1), pl.pt(16, 1)], TEN, 3.6)
    o += pl.dot(1, 1, KEY, 6)
    o += T(pl.X(1) + 10, pl.Y(1) - 14, '降伏點 (ε_{y}, *F*_{y})', 15, KEY, 'start', 'bold')
    o += T(pl.X(5.5), pl.Y(1) + 26, '降伏平台：應變一直長，應力不再增加', 15, TEN, 'middle', 'bold')
    o += T(pl.X(14.6), pl.Y(1.25) - 12, '實際：應變硬化', 14, MUT, 'middle')
    o += T(pl.X(14.6), pl.Y(1.25) + 8, '（示意）', 14, MUT, 'middle')
    o += A(pl.X(10), pl.Y(0.55), pl.X(10), pl.Y(0.97), MUT, 1.4, 8)
    o += T(pl.X(10), pl.Y(0.55) + 20, '約 10ε_{y}', 14, MUT, 'middle')
    # 右側說明
    bx = 690
    o += R(bx, 70, 200, 210, KEY2, KEY, 1.4, 10)
    o += T(bx + 100, 98, '只用綠色兩段線', 16, KEY, 'middle', 'bold')
    for i, s in enumerate(['① 斜線：σ = *E*ε', '② 平線：σ = *F*_{y}', '   （拉、壓都一樣）', '硬化部分不算', '→ 偏保守']):
        o += T(bx + 14, 130 + i * 28, s, 15, INK, 'start')
    o += T(bx + 100, 312, f'ε_{{y}} = *F*_{{y}}/*E* = {2.5 / E:.5f}', 14, MUT, 'middle')
    o += T(bx + 100, 334, '（*F*_{y} = 2.5 時）', 14, MUT, 'middle')
    return svg(W, H, o, '鋼的兩段線應力應變關係')


def _stage(x0, top, hh, k, title, mval):
    """矩形斷面在外緣應變 k·εy 時的應變與應力分布。x0：面板左緣。"""
    o = ''
    cx = x0 + 18                  # 斷面（側視）
    o += R(cx, top, 22, hh, STEEL3, INK, 1.2)
    mid = top + hh / 2
    o += L(cx - 6, mid, x0 + 196, mid, AC, 1.4, '5 4')
    # 應力分布：σ(y) = Fy·clamp(k·y/c)
    sx = x0 + 110; sc = 70          # 應力軸位置、Fy 對應 70 px
    o += L(sx, top - 6, sx, top + hh + 6, INK, 1.4)
    n = 80
    ptsC, ptsT = [(sx, mid)], [(sx, mid)]
    for i in range(n + 1):
        u = i / n                      # 0 = 中性軸, 1 = 外緣
        s = max(-1, min(1, k * u))
        ptsC.append((sx - s * sc, mid - u * hh / 2))
        ptsT.append((sx + s * sc, mid + u * hh / 2))
    ptsC.append((sx, top)); ptsT.append((sx, top + hh))
    o += P(ptsC, COMP, 2, COMP2, close=True)
    o += P(ptsT, TEN, 2, TEN2, close=True)
    o += L(sx - sc, top - 6, sx - sc, top + hh + 6, MUT, 1, '3 3')
    o += L(sx + sc, top - 6, sx + sc, top + hh + 6, MUT, 1, '3 3')
    o += T(sx - sc, top + hh + 24, '−*F*_{y}', 14, MUT, 'middle')
    o += T(sx + sc, top + hh + 24, '+*F*_{y}', 14, MUT, 'middle')
    o += T(x0 + 105, top - 40, title, 15, INK, 'middle', 'bold')
    o += T(x0 + 105, top - 18, f'外緣 ε = {k:g}ε_{{y}}' if k < 50 else '外緣 ε → ∞', 14, MUT, 'middle')
    o += R(x0 + 30, top + hh + 38, 150, 30, KEY2 if k >= 50 else AC2, None, 0, 8)
    o += T(x0 + 105, top + hh + 59, mval, 15, KEY if k >= 50 else AC, 'middle', 'bold')
    return o


def fig1_2():
    W, H = 900, 400
    top, hh = 80, 220
    o = ''
    ks = [(0.5, '① 彈性'), (1, '② 剛好降伏'), (3, '③ 部分塑化'), (1000, '④ 全塑化')]
    for i, (k, t) in enumerate(ks):
        if k >= 50:
            mv = f'*M* → {RECT.f:g}*M*_{{y}} = *M*_{{p}}'
        else:
            m = RECT.moment_at_curvature(k * RECT.phi_y())[0] / RECT.My
            mv = '*M* = *M*_{y}' if k == 1 else f'*M* = {m:.3f}*M*_{{y}}'
        o += _stage(10 + i * 222, top, hh, k, t, mv)
    return svg(W, H, o, '矩形斷面應力分布由三角形長成矩形')


def _section(s, x0, ytop, sc, fill=STEEL3):
    """依比例畫斷面（rects y 由底量）。回傳 svg、底緣 y、中心 x。"""
    o = ''
    cx = x0
    ybot = ytop + s.H * sc
    for nm, b, y0, y1 in s.rects:
        o += R(cx - b * sc / 2, ybot - y1 * sc, b * sc, (y1 - y0) * sc, fill, INK, 1.2)
    return o, ybot, cx


def fig1_3():
    s = S20
    W, H = 900, 470
    sc = 6.0
    ytop = 50
    o, ybot, cx = _section(s, 200, ytop, sc)
    ye = ybot - s.ybar * sc
    o += L(cx - 130, ye, cx + 130, ye, AC, 2.2, '8 5')
    o += T(cx - 136, ye + 5, 'ENA', 16, AC, 'end', 'bold')
    o += dim(cx + 140, ytop, cx + 140, ye, f'*c*_{{top}} = {s.c_top:.2f}', AC, 0, 15, -1)
    o += dim(cx + 140, ye, cx + 140, ybot, f'*c*_{{bot}} = {s.c_bot:.2f}', AC, 0, 15, -1)
    o += T(cx, ytop - 14, '上翼板 30×2.5', 14, MUT, 'middle')
    o += T(cx, ybot + 24, '下翼板 20×2.5', 14, MUT, 'middle')
    o += T(cx + 8, ytop + 140, '腹板 1.5×55', 14, MUT, 'start')
    # 應力圖（M = My）：底緣 +Fy（拉）、頂緣 −Fy·c_top/c_bot
    sx = 560; scs = 110
    o += L(sx, ytop - 10, sx, ybot + 10, INK, 1.4)
    o += L(sx - 140, ye, sx + 150, ye, AC, 1.4, '8 5')
    stop = s.c_top / s.c_bot
    o += P([(sx, ye), (sx - stop * scs, ytop), (sx, ytop)], COMP, 2.2, COMP2, close=True)
    o += P([(sx, ye), (sx + scs, ybot), (sx, ybot)], TEN, 2.2, TEN2, close=True)
    o += L(sx + scs, ytop - 10, sx + scs, ybot + 10, MUT, 1, '3 3')
    o += T(sx + scs + 6, ybot - 6, '*F*_{y}', 15, TEN, 'start', 'bold')
    o += T(sx + scs + 6, ybot + 16, '← 先到', 15, TEN, 'start', 'bold')
    o += T(sx - stop * scs - 6, ytop + 18, f'{stop:.3f}*F*_{{y}}', 15, COMP, 'end', 'bold')
    o += T(sx - stop * scs - 6, ytop + 40, '還沒到', 14, COMP, 'end')
    o += T(sx, ytop - 22, '*M* = *M*_{y} 時的應力', 15, INK, 'middle', 'bold')
    o += R(700, 60, 190, 120, AC2, AC, 1.4, 10)
    o += T(795, 86, '離 ENA 較遠的', 15, AC, 'middle', 'bold')
    o += T(795, 110, '那一側先降伏', 15, AC, 'middle', 'bold')
    o += T(795, 138, '*S*_{min} = *I*/*c*_{max}', 15, INK, 'middle')
    o += T(795, 164, f'= {s.I:,.0f}/{s.c_bot:.2f}', 14, INK, 'middle')
    return svg(W, H, o, 'SS-2020-2 斷面的 ENA 與降伏彎矩時的應力')


def fig1_4():
    s = S20
    W, H = 900, 330
    x0, bw = 190, 560
    mx = max(p['Iown'] + p['Ad2'] for p in s.parts_I)
    o = T(x0 + bw / 2, 30, f'*I*_{{x}} = {s.I:,.0f} cm^{{4}} 的組成（SS-2020-2）', 17, INK, 'middle', 'bold')
    order = [s.parts_I[2], s.parts_I[1], s.parts_I[0]]
    for i, p in enumerate(order):
        y = 60 + i * 72
        a = p['Ad2'] / mx * bw; b = p['Iown'] / mx * bw
        o += T(x0 - 14, y + 30, p['nm'], 16, INK, 'end', 'bold')
        o += R(x0, y + 8, a, 36, AC, None, 0, 4)
        o += R(x0 + a, y + 8, max(b, 1.5), 36, KEY, None, 0, 4)
        tot = p['Ad2'] + p['Iown']
        lx = x0 + a + b + 10
        txt = f'*Ad*^{{2}} {p["Ad2"]:,.0f} + 自身 {p["Iown"]:,.0f}'
        if lx + 300 > W:
            o += T(x0 + 10, y + 32, txt, 14, '#fff', 'start', 'bold')
        else:
            o += T(lx, y + 32, txt, 14, INK, 'start')
        o += T(x0 + 10, y + 64, f'占 {tot / s.I * 100:.1f}%', 14, MUT, 'start')
    o += R(x0, 286, 18, 18, AC, None) + T(x0 + 26, 301, '*Ad*^{2}（離軸遠）', 14, INK)
    o += R(x0 + 200, 286, 18, 18, KEY, None) + T(x0 + 226, 301, '*bh*^{3}/12（自身）', 14, INK)
    return svg(W, H, o, 'SS-2020-2 慣性矩的組成')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}

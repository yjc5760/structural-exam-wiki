# -*- coding: utf-8 -*-
"""第 11 章：弱軸應力塊與 1.5FySy 上限、雙軸彎曲互制。"""
from plot import *  # noqa
import calcs

WK = calcs.ex_weak()
D = calcs.example()


def fig11_1():
    W, H = 900, 430
    o = ''
    # 弱軸彎曲：彎曲軸＝腹板軸（垂直）；畫兩片翼板（俯視為矩形）＋腹板
    cx, cy = 170, 200
    sc = 7.0
    bf, tf, d = 20, 2.5, 70
    hh = d * 2.2
    o += T(cx, 36, 'H700 弱軸彎曲（中性軸＝腹板）', 16, INK, 'middle', 'bold')
    o += R(cx - bf / 2 * sc, cy - hh / 2, bf * sc, tf * sc, STEEL3, INK, 1.4)
    o += R(cx - bf / 2 * sc, cy + hh / 2 - tf * sc, bf * sc, tf * sc, STEEL3, INK, 1.4)
    o += R(cx - 0.6 * sc, cy - hh / 2 + tf * sc, 1.2 * sc, hh - 2 * tf * sc, STEEL3, INK, 1.2)
    o += L(cx, cy - hh / 2 - 20, cx, cy + hh / 2 + 20, AC, 1.6, '6 4')
    o += T(cx + 8, cy + hh / 2 + 34, '中性軸', 14, AC, 'start')
    o += T(cx, cy + hh / 2 + 56, '翼板＝兩塊「直立的矩形」', 15, KEY, 'middle', 'bold')
    # 應力圖（沿翼板寬度）
    for k, (title, mode, c) in enumerate((('彈性：三角形', 'e', AC), ('塑性：矩形', 'p', TEN))):
        ox = 420 + k * 240
        y0 = cy - 60
        o += T(ox + 70, 36, title, 16, c, 'middle', 'bold')
        w = bf / 2 * sc
        o += L(ox + 70, y0 - 40, ox + 70, y0 + 160, INK, 1.2)
        o += L(ox + 70 - w, y0 + 60, ox + 70 + w, y0 + 60, MUT, 1.2)
        if mode == 'e':
            o += P([(ox + 70, y0 + 60), (ox + 70 - w, y0 + 60), (ox + 70 - w, y0 - 10)], COMP, 1.6, COMPM, close=True)
            o += P([(ox + 70, y0 + 60), (ox + 70 + w, y0 + 60), (ox + 70 + w, y0 + 130)], TEN, 1.6, TENM, close=True)
        else:
            o += R(ox + 70 - w, y0 - 10, w, 70, COMPM, COMP, 1.6)
            o += R(ox + 70, y0 + 60, w, 70, TENM, TEN, 1.6)
        o += T(ox + 70 + bf / 2 * sc + 6, y0 + 65, '*x*', 15, MUT, 'start')
    o += box(430, 320, 450, 90, f'*Z*_{{y}}/*S*_{{y}} = {WK["Zy"]:.1f}/{WK["Sy"]:.1f} = {WK["fy"]:.3f}　＞ 1.5',
             [f'取 *M*_{{ny}} = min(*F*_{{y}}*Z*_{{y}}, 1.5*F*_{{y}}*S*_{{y}}) = {WK["Mny"]:.0f} tf·cm'], KEY2, KEY, 16, 15)
    return svg(W, H, o, '弱軸彎曲')


def fig11_2():
    W, H = 900, 400
    pl = Plot(100, 40, 300, 300, 0, 1.2, 0, 1.2)
    o = pl.axes([0, 0.5, 1.0], [0, 0.5, 1.0], '*M*_{ux}/φ*M*_{nx}', '', size=14)
    o += T(pl.X(0), pl.Y(1.2) - 22, '*M*_{uy}/φ*M*_{ny}', 15, INK, 'middle')
    o += P([pl.pt(0, 1), pl.pt(1, 0), pl.pt(0, 0)], None, fill=TEN2, close=True)
    o += L(pl.X(0), pl.Y(1), pl.X(1), pl.Y(0), TEN, 2.8)
    x, y = 400 / 945.8, 50 / 171.1
    o += pl.dot(x, y, KEY, 7)
    o += T(pl.X(x) + 10, pl.Y(y) - 8, f'SS-2014-3：{x:.3f}+{y:.3f}={x + y:.3f}', 14, KEY, 'start', 'bold')
    o += T(pl.X(0.15), pl.Y(0.15), '安全區', 15, TEN, 'start', 'bold')
    # 強弱軸長條
    bx = Plot(560, 60, 280, 260, 0, 2, 0, 160)
    o += bx.axes([], [0, 40, 80, 120, 160], '', 'φ*M*_{n}（tf·m）', size=14)
    vals = [(D['phiMp'] / 100, '強軸 φ*M*_{p}', COMP), (0.9 * WK['Mny'] / 100, '弱軸 φ*M*_{ny}', TEN)]
    for i, (v, lab, c) in enumerate(vals):
        xx = 0.25 + i
        o += R(bx.X(xx), bx.Y(v), bx.X(xx + 0.5) - bx.X(xx), bx.Y(0) - bx.Y(v), c, None, 0, 4, op=0.85)
        o += T(bx.X(xx + 0.25), bx.Y(v) - 8, f'{v:.1f}', 15, c, 'middle', 'bold')
        o += T(bx.X(xx + 0.25), bx.Y(0) + 22, lab, 14, INK, 'middle', 'bold')
    o += T(700, 380, f'H700×200：弱軸只有強軸的 1/{WK["strong_weak"]:.1f}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '雙軸彎曲互制')


ALL = {'fig11_1': fig11_1, 'fig11_2': fig11_2}

# -*- coding: utf-8 -*-
"""第 1 章：保險絲鏈、韌性三層次。"""
from figs_common import *  # noqa
from calcs import p2022_4
import math

D22 = p2022_4()


def _link(cx, cy, w, h, col, fill, lab):
    o = R(cx - w / 2, cy - h / 2, w, h, fill, col, 3, h / 2)
    o += R(cx - w / 2 + 14, cy - h / 2 + 12, w - 28, h - 24, '#fff', col, 1.4, (h - 24) / 2)
    o += T(cx, cy + h / 2 + 22, lab, 14, col, 'middle', 'bold')
    return o


def fig1_1():
    W, H = 900, 400
    o = T(450, 24, '一串保險絲：讓延性的梁端先降伏，其他都要比它強', 16, INK, 'middle', 'bold')
    # 左：鏈條（直式）
    cx = 150
    labs = [('柱（壓、彎）', COMP, COMP2), ('接頭剪力', COMP, COMP2), ('梁端撓曲', TEN, TEN2), ('梁剪力', COMP, COMP2), ('搭接、錨定', COMP, COMP2)]
    o += A(cx, 52, cx, 70, INK, 2, 9)
    for i, (lab, col, fill) in enumerate(labs):
        cy = 92 + i * 58
        o += _link(cx, cy, 70, 44, col, fill, '')
        o += T(cx + 50, cy + 5, lab, 15, col, 'start', 'bold')
    o += A(cx, 92 + 4 * 58 + 24, cx, 92 + 4 * 58 + 42, INK, 2, 9)
    o += T(cx + 50, 92 + 2 * 58 + 26, '← 保險絲（最弱、延性）', 14, TEN, 'start', 'bold')
    o += T(cx, 384, '綠＝延性；紅＝脆性', 14, MUT, 'middle')
    # 右：力–位移
    pl = Plot(470, 70, 370, 260, 0, 10, 0, 1.3)
    o += pl.axes([], [], 'Δ', '*V*', grid=False, size=14)
    o += P([pl.pt(0, 0), pl.pt(1.0, 1.15), pl.pt(1.25, 0.25)], COMP, 3)
    o += T(pl.X(1.3) + 6, pl.Y(0.35), '脆性：一壞就掉', 15, COMP, 'start', 'bold')
    o += P([pl.pt(0, 0), pl.pt(1.0, 1.0), pl.pt(8.5, 1.08), pl.pt(9.3, 0.8)], TEN, 3)
    o += T(pl.X(5.2), pl.Y(1.08) - 14, '延性：降伏後繼續變形、消能', 15, TEN, 'middle', 'bold')
    o += P([pl.pt(1.0, 0), pl.pt(1.0, 1.0)], MUT, 1.2, dash='4 3')
    o += T(pl.X(1.0), pl.Y(0) + 22, 'Δ_{y}', 14, MUT, 'middle')
    o += P([pl.pt(8.5, 0), pl.pt(8.5, 1.08)], MUT, 1.2, dash='4 3')
    o += T(pl.X(8.5), pl.Y(0) + 22, 'Δ_{u}', 14, MUT, 'middle')
    o += T(pl.X(5.2), pl.Y(0.65), 'μ_{Δ} = Δ_{u}/Δ_{y}', 16, AC, 'middle', 'bold')
    return svg(W, H, o, '保險絲鏈')


def fig1_2():
    W, H = 900, 430
    o = T(450, 24, '懸臂柱：曲率 × 長度 = 轉角，轉角 × 力臂 = 位移', 16, INK, 'middle', 'bold')
    Lc, Lp = D22['L'], D22['Lp']
    sc = 92
    ytop, ybot = 70, 70 + Lc * sc
    # 柱
    x0 = 90
    o += R(x0 - 18, ytop, 36, Lc * sc, STEEL2, INK, 1.4)
    o += fixed_wall(x0, ybot, 90)
    o += A(x0 - 70, ytop + 6, x0 - 24, ytop + 6, AC, 2.6, 10)
    o += T(x0 - 72, ytop - 4, '*V*', 15, AC, 'end', 'bold')
    o += vdim(x0 + 36, ytop, ybot, f'*L* = {Lc:.1f} m', INK, 1, 15)
    o += T(x0, ybot + 40, '柱', 15, INK, 'middle', 'bold')
    # 彎矩圖
    x1 = 260
    o += T(x1 + 40, 56, '彎矩', 15, INK, 'middle', 'bold')
    o += L(x1, ytop, x1, ybot, MUT, 1.2)
    o += P([(x1, ytop), (x1 + 100, ybot), (x1, ybot)], COMP, 2, fill=COMP2, close=True)
    o += T(x1 + 104, ybot - 6, '*M*', 15, COMP, 'start', 'bold')
    # 曲率圖
    x2 = 450
    o += T(x2 + 60, 56, '曲率', 15, INK, 'middle', 'bold')
    o += L(x2, ytop, x2, ybot, MUT, 1.2)
    kx = 60 / D22['phiy']
    o += P([(x2, ytop), (x2 + D22['phiy'] * kx, ybot), (x2, ybot)], AC, 2, fill=AC2, close=True)
    yp = ybot - Lp * sc
    o += R(x2 + D22['phiy'] * kx * (1 - Lp / Lc), yp, (D22['phid'] - D22['phiy']) * kx, Lp * sc, KEY2, KEY, 2)
    o += T(x2 + D22['phiy'] * kx + 6, ybot + 22, 'φ_{y}', 14, AC, 'middle', 'bold')
    o += T(x2 + D22['phid'] * kx, ybot + 22, 'φ_{d}', 14, KEY, 'middle', 'bold')
    o += vdim(x2 + D22['phid'] * kx + 14, yp, ybot, f'*L*_{{p}} = {Lp:.3f} m', KEY, 1, 14)
    o += T(x2 + 40, ytop + 80, '彈性三角形', 14, AC, 'start')
    o += T(x2 + (D22['phiy'] * (1 - Lp / Lc) + (D22['phid'] - D22['phiy']) / 2) * kx, yp + Lp * sc / 2 + 5, '塑性', 14, KEY, 'middle', 'bold')
    # 右：結果框
    o += box(745, 80, 145, 280, 'RC-2022-4', [f"φ_{{y}} = {D22['phiy']:.3f}", f"φ_{{d}} = {D22['phid']:.4f}", f"δ_{{y}} = {D22['dy']*100:.3f} cm", f"δ_{{d}} = {D22['dd']*100:.3f} cm", f"μ_{{φ}} = {D22['mu_phi']:.2f}", f"μ_{{θ}} = μ_{{Δ}} = {D22['mu_d']:.2f}", '塑性只在 *L*_{p}', '→ μ_{Δ} < μ_{φ}'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '韌性三層次')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}

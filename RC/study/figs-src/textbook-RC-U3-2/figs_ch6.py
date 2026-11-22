# -*- coding: utf-8 -*-
"""第 6 章：版剪力筋配置平面、剛性樁帽樁力。"""
from figs_common import *  # noqa
from calcs import p2020_3, p2021_3
import math

P20 = p2020_3()
P21 = p2021_3()


def fig6_1():
    W, H = 900, 420
    o = T(450, 24, '柱周剪力筋：同一周線上數肢數', 16, INK, 'middle', 'bold')
    sc = 1.3
    cx, cy = 260, 220
    c, d = P20['c'], P20['d']
    o += R(cx - 170, cy - 170, 340, 340, STEEL2, INK, 1.2)
    a = (c + d) * sc
    o += R(cx - a / 2, cy - a / 2, a, a, COMP2, COMP, 2.6)
    o += R(cx - c * sc / 2, cy - c * sc / 2, c * sc, c * sc, STEEL3, INK, 1.6)
    # 四條剪力筋帶
    for ang in range(4):
        for k in range(1, 5):
            r = c * sc / 2 + k * 5 * sc * 2.4
            for off in (-c * sc / 2 + 10, c * sc / 2 - 10):
                if ang == 0:
                    x, y = cx + r, cy + off
                elif ang == 1:
                    x, y = cx - r, cy + off
                elif ang == 2:
                    x, y = cx + off, cy + r
                else:
                    x, y = cx + off, cy - r
                o += C(x, y, 3.6, TEN, '#fff', 0.8)
    o += T(cx, cy + a / 2 + 24, f"*b*_{{o}} = {P20['bo']:.0f} cm", 15, COMP, 'middle', 'bold')
    o += T(cx, cy + 8, '柱', 15, INK, 'middle', 'bold')
    o += T(cx + 175, cy - 150, '±X、±Y 四條帶', 14, TEN, 'start', 'bold')
    o += T(cx + 175, cy - 130, '每條雙肢 D13', 14, TEN, 'start', 'bold')
    o += box(560, 70, 320, 300, 'RC-2020-3', [f"λ_{{s}} = {P20['lam_s']:.3f}（樓版要乘）", f"*V*_{{u}} = {P20['Vu']:.2f} tf", f"無筋 φ*V*_{{c}} = {P20['phiVc']:.2f}（不足）", f"有筋 *V*_{{c}} = 0.53λ_{{s}}… = {P20['Vcw']:.2f}", f"*V*_{{s}} = {P20['Vs']:.2f} tf", f"*A*_{{v}} = 4×2×1.267 = {P20['Av']:.2f} cm²", f"*s* = {P20['s']:.2f} → 5 cm", f"上限 φ1.59√*f*′_{{c}}*b*_{{o}}*d* = {P20['phiVnmax']:.2f}"], KEY2, KEY, 15, 14)
    return svg(W, H, o, '版剪力筋')


def fig6_2():
    W, H = 900, 475
    o = T(450, 24, '剛性樁帽：只會下沉＋轉動，樁力隨 *x* 直線變化', 16, INK, 'middle', 'bold')
    e = P21['emax']
    # 左：立面
    x0, y0, sc = 60, 150, 1.25
    Bc = 260
    ang = -0.035
    o += R(x0, y0, Bc * sc, 55, STEEL2, INK, 1.6)
    xc = x0 + Bc * sc / 2
    o += R(xc - 25 * sc, y0 - 50, 50 * sc, 50, STEEL3, INK, 1.4)
    o += A(xc + e * sc, y0 - 90, xc + e * sc, y0 - 52, AC, 2.8, 10)
    o += T(xc + e * sc + 8, y0 - 70, f"*P*_{{u}} = {P21['Pu']:.0f} tf", 15, AC, 'start', 'bold')
    o += L(xc, y0 - 96, xc, y0 + 60, MUT, 1, '4 3')
    o += hdim(xc, xc + e * sc, y0 - 104, f'*e*_{{x}} = {e:.0f}', AC, -1, 14)
    forces = []
    for xi in (-90, 90):
        Pi = P21['Pu'] / 4 + P21['k_e'] * e * (1 if xi > 0 else -1)
        forces.append((xi, Pi))
        xx = xc + xi * sc
        o += R(xx - 15 * sc / 2, y0 + 55, 15 * sc, 110, STEEL3, INK, 1.2)
        hgt = Pi * 2.6
        o += A(xx, y0 + 175 + hgt, xx, y0 + 175, KEY, 2.6, 10)
        o += T(xx + 10, y0 + 200, f'{Pi:.0f} tf ×2', 15, KEY, 'start', 'bold')
    o += L(xc - 90 * sc, y0 + 175 + forces[0][1] * 2.6, xc + 90 * sc, y0 + 175 + forces[1][1] * 2.6, KEY, 1.4, '5 3')
    o += T(xc, y0 + 314, f"*P*_{{i}} = 25 ± *e*_{{x}}/3.6；壓 ≤ 40 → *e*_{{x}} ≤ {P21['e_comp']:.0f} cm", 15, INK, 'middle', 'bold')
    # 右：平面
    px, py, s2 = 560, 80, 1.15
    o += R(px, py, Bc * s2, Bc * s2, STEEL2, INK, 1.6)
    pcx, pcy = px + Bc * s2 / 2, py + Bc * s2 / 2
    a = (P21['c'] + P21['d']) * s2
    o += R(pcx - a / 2, pcy - a / 2, a, a, 'none', COMP, 2.2)
    o += R(pcx - 25 * s2, pcy - 25 * s2, 50 * s2, 50 * s2, STEEL3, INK, 1.2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            o += C(pcx + sx * 90 * s2, pcy + sy * 90 * s2, 15 * s2, '#fff', INK, 1.4)
    # 角隅樁臨界周長（右下）
    qx, qy = pcx + 90 * s2, pcy + 90 * s2
    rc = P21['r_crit'] * s2
    pts = []
    for i in range(31):
        t = math.radians(180 + 90 * i / 30)
        pts.append((qx + rc * math.cos(t), qy + rc * math.sin(t)))
    o += P([(qx - rc, py + Bc * s2)] + pts + [(px + Bc * s2, qy - rc)], KEY, 2.4)
    o += T(pcx, py + Bc * s2 + 30, f"柱周 *b*_{{o}} = {P21['bo_col']:.0f}（紅）", 14, COMP, 'middle', 'bold')
    o += T(pcx, py + Bc * s2 + 52, f"角隅樁 *b*_{{o}} = {P21['bo_corner']:.1f}（紫）", 14, KEY, 'middle', 'bold')
    o += T(pcx, py + Bc * s2 + 74, f"φ*V*_{{c}} = {P21['phiVc_pile']:.2f} ≥ 40 tf", 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '剛性樁帽')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}

# -*- coding: utf-8 -*-
"""第 7 章：剪力牆覆沒與剪力兩份；橫膈版鋼筋相加。"""
from figs_common import *  # noqa
from calcs import p2003_4, p2019_3, sq

W03, D19 = p2003_4(), p2019_3()


def fig7_1():
    W, H = 900, 440
    o = T(450, 24, 'RC-2003-4：覆沒軸力與剪力強度', 16, INK, 'middle', 'bold')
    x0, yb, s = 60, 370, 0.36
    lw, hw = 930, 800
    # 牆
    o += R(x0, yb - hw * s, lw * s, hw * s, STEEL2, INK, 1.4)
    o += R(x0, yb - hw * s, 30 * s, hw * s, STEEL3, INK, 1.2)
    o += R(x0 + (lw - 30) * s, yb - hw * s, 30 * s, hw * s, STEEL3, INK, 1.2)
    o += hatch_ground(x0 - 10, yb, lw * s + 20)
    # 地震力（向左）
    o += A(x0 + lw * s + 70, yb - hw * s, x0 + lw * s + 4, yb - hw * s, COMP, 2.6, 11)
    o += T(x0 + lw * s + 74, yb - hw * s + 5, '45 tf', 15, COMP, 'start', 'bold')
    o += A(x0 + lw * s + 70, yb - 450 * s, x0 + lw * s + 4, yb - 450 * s, COMP, 2.6, 11)
    o += T(x0 + lw * s + 74, yb - 450 * s + 5, '30 tf', 15, COMP, 'start', 'bold')
    o += T(x0 + lw * s / 2, yb - hw * s / 2, f"*M*_{{u}} = {W03['Mu_wall']:.0f} tf·m", 15, KEY, 'middle', 'bold')
    o += T(x0 + lw * s / 2, yb - hw * s / 2 + 26, f"÷ 9.0 m = ±{W03['F_ot']:.1f} tf", 15, KEY, 'middle', 'bold')
    # 端部軸力
    o += A(x0 + 5, yb + 8, x0 + 5, yb + 40, AC, 2.4, 10)
    o += T(x0 - 6, yb + 60, f"壓 {W03['BE_max']:.1f}", 14, AC, 'start', 'bold')
    o += A(x0 + lw * s - 5, yb + 8, x0 + lw * s - 5, yb + 30, AC, 2.0, 9)
    o += T(x0 + lw * s + 6, yb + 60, f"0.9*D* + *E*：壓 {W03['BE_min']:.2f}", 14, AC, 'end', 'bold')
    # 右：剪力兩份
    gx, gy, k = 520, 110, 0.9
    vc = W03['alpha_c'] * sq(W03['fc']) * W03['Acv'] / 1000
    vs = W03['rho_t'] * W03['fy'] * W03['Acv'] / 1000
    o += T(gx, gy - 20, f"*V*_{{n}} = *A*_{{cv}}(*α*_{{c}}√*f*'_{{c}} + *ρ*_{{t}}*f*_{{y}})", 15, INK, 'start', 'bold')
    o += R(gx, gy, vc * k, 40, AC, None, 0, op=0.8)
    o += R(gx + vc * k, gy, vs * k, 40, TEN, None, 0, op=0.8)
    o += T(gx + vc * k / 2, gy + 26, f'混凝土 {vc:.1f}', 14, '#fff', 'middle', 'bold')
    o += T(gx + vc * k + vs * k / 2, gy + 26, f'鋼筋 {vs:.1f}', 14, '#fff', 'middle', 'bold')
    o += T(gx, gy + 70, f"*V*_{{n}} = {W03['Vn']:.1f} tf，*φV*_{{n}} = {W03['phiVn']:.1f} tf", 15, KEY, 'start', 'bold')
    o += L(gx + W03['Vu'] * k, gy - 6, gx + W03['Vu'] * k, gy + 46, COMP, 2.2, '5 4')
    o += T(gx + W03['Vu'] * k, gy + 104, f"*V*_{{u}} = {W03['Vu']:.0f}", 15, COMP, 'middle', 'bold')
    o += T(gx, gy + 150, '門檻（tf）：', 15, INK, 'start', 'bold')
    o += T(gx, gy + 178, f"0.27√*f*'_{{c}}*A*_{{cv}} = {W03['rmin_trigger']:.1f} → *ρ* ≥ 0.0025", 14, INK, 'start')
    o += T(gx, gy + 204, f"0.53√*f*'_{{c}}*A*_{{cv}} = {W03['single']:.1f} → 超過才要雙層", 14, INK, 'start')
    o += T(gx, gy + 230, f"邊界 *f*_{{c}} = {W03['fc_edge']:.1f} ＜ 0.2*f*'_{{c}} = {W03['fc_lim']:.0f}", 14, INK, 'start')
    return svg(W, H, o, '剪力牆')


def fig7_2():
    W, H = 900, 380
    o = T(450, 24, 'RC-2019-3：剪力斷面 = 厚 × 長；鋼筋 = 撓曲 + 抗剪', 16, INK, 'middle', 'bold')
    x0, y0, s = 80, 80, 0.5
    o += R(x0, y0, 500 * s, 500 * s, STEEL2, INK, 1.4)
    o += R(x0, y0 + 250 * s - 6, 500 * s, 12, KEY, None, 0, op=0.5)
    o += A(x0 + 60, y0 + 60, x0 + 190, y0 + 60, COMP, 2.6, 11)
    o += T(x0 + 60, y0 + 46, f"*V*_{{u}} = {D19['Vu']:.0f} tf（面內）", 15, COMP, 'start', 'bold')
    o += T(x0 + 125, y0 + 250 * s + 34, '剪力斷面（平行於力）', 15, KEY, 'middle', 'bold')
    o += T(x0 + 125, y0 + 250 * s + 58, f"18 × 500 = {D19['Acv']:.0f} cm²", 14, KEY, 'middle')
    o += hdim(x0, x0 + 500 * s, y0 + 500 * s + 18, '500 cm', INK, 1, 15)
    # 右：相加
    gx, gy, k = 540, 110, 1500
    o += T(gx, gy - 20, '每 cm 版寬，上下雙層合計（cm²/cm）', 15, INK, 'start', 'bold')
    o += R(gx, gy, D19['As_flex'] * k, 34, AC, None, 0, op=0.8)
    o += R(gx + D19['As_flex'] * k, gy, D19['As_shear'] * k, 34, TEN, None, 0, op=0.8)
    o += T(gx + D19['As_flex'] * k / 2, gy + 23, f"撓曲 {D19['As_flex']:.4f}", 14, '#fff', 'middle', 'bold')
    o += T(gx + D19['As_flex'] * k + D19['As_shear'] * k / 2, gy + 23, f"抗剪 {D19['As_shear']:.4f}", 14, '#fff', 'middle', 'bold')
    o += T(gx, gy + 64, f"合計 {D19['As_tot']:.4f} → *s* = 2×1.27/{D19['As_tot']:.4f} = {D19['s_req']:.1f}", 15, KEY, 'start', 'bold')
    o += T(gx, gy + 92, f"採 #4 雙層 @{D19['s_use']:.0f}：*φV*_{{n}} = {D19['phiVn']:.1f} tf", 15, TEN, 'start', 'bold')
    o += T(gx, gy + 132, '舊解取兩者較小（@25）：抗剪筋被吃掉', 14, MUT, 'start')
    return svg(W, H, o, '橫膈版')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}

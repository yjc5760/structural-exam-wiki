"""lecture-SD-U3-1.html 的全部 SVG 圖（座標全部由 calcs.py 的數值算出）。
用法：python gen_figs.py ../../../study/lecture-SD-U3-1.html"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common')); sys.path.insert(0, HERE)
from figkit import *  # noqa
import calcs as K

BLUE, RED, GRN, ORG, PUR, GRY, TEAL = '#1565C0', '#C62828', '#2E7D32', '#EF6C00', '#6A1B9A', '#78909C', '#00838F'

def hatch_ground(cv, x0, x1, y):
    px_line(cv, x0, y, x1, y, C['member'], 2)
    for x in np.arange(x0 + 4, x1, 8): px_line(cv, x, y, x - 7, y + 8, C['member'], 1.1)

def fig_overview():
    """延性 vs 脆性：力–位移（以 Vy、Δy 正規化）"""
    cv = new(900, 350)
    for k, (x0, title, col, pts, area, note) in enumerate((
        (70, '延性破壞：梁端撓曲塑鉸（准許）', GRN, [(0, 0), (1, 1), (K.mu_duct, 1)], K.E_duct, f'μ = {K.mu_duct:g}，能量 ≈ {K.E_duct:.1f}（以 V_yΔ_y 計）'),
        (500, '脆性破壞：剪力、柱、接頭（不准先發生）', RED, [(0, 0), (0.8, 0.8), (0.9, 0.0)], K.E_brit, f'無預警掉落，能量 ≈ {K.E_brit:.2f}'))):
        p = Plot(cv, x0, 74, 330, 178, (0, 7), (0, 1.3))
        p.frame([0, 1, 2, 3, 4, 5, 6, 7], [0, 0.5, 1.0], 'Δ / Δ_y', 'V / V_y', yfmt='{:.1f}')
        px_polygon(cv, [p.P(x, y) for x, y in pts] + [p.P(pts[-1][0], 0)], col, 'none', 0, 0.18)
        p.curve([q[0] for q in pts], [q[1] for q in pts], col, 3)
        T(cv, x0 + 165, 30, title, 14, col, 'middle', '700')
        T(cv, x0 + 165, 310, note, 12.5, C['text'])
    T(cv, 450, 336, '同樣的強度，延性破壞吸收的能量多十倍以上而且看得見；耐震設計就是保證先發生左邊這種', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_capacity_shear():
    """SD-2013-2：兩個側移方向的剪力線、容量剪力包絡與 φVn"""
    cv = new(900, 360)
    p = Plot(cv, 90, 50, 640, 240, (0, K.ln), (-5, 40))
    p.frame([0, 1.2, 2, 3, 4, 5.2, 6.4], [0, 10, 20, 30, 40], '距 A 柱面 x（m）', 'V（tf）', xfmt='{:g}')
    xs = np.linspace(0, K.ln, 100)
    V1 = K.Veq1 + K.wu * (K.ln / 2 - xs)       # 側移方向 1：A 端剪力大
    V2 = K.Veq2 - K.wu * (K.ln / 2 - xs)       # 側移方向 2：B 端剪力大
    p.curve(xs, V1, ORG, 2.2, '6 4'); p.curve(xs, V2, BLUE, 2.2, '6 4')
    p.curve(xs, np.maximum(V1, V2), RED, 3)
    cap = [(0, K.phiVs_hinge), (1.2, K.phiVs_hinge), (1.2, K.phiVn_out), (K.ln - 1.2, K.phiVn_out), (K.ln - 1.2, K.phiVs_hinge), (K.ln, K.phiVs_hinge)]
    p.curve([c[0] for c in cap], [c[1] for c in cap], GRN, 2.6)
    px_line(cv, p.X(0), p.Y(K.Vu_analysis), p.X(K.ln), p.Y(K.Vu_analysis), GRY, 1.4, '3 3')
    T(cv, p.X(3.2), p.Y(K.Vu_analysis) + 14, f'若用分析彎矩推：{K.Vu_analysis:.2f} tf（低估 {100*(1-K.Vu_analysis/K.Ve):.0f}%）', 11.5, GRY)
    p.dot(K.ln, K.Ve, 5, RED); T(cv, p.X(K.ln) + 10, p.Y(K.Ve), f'V_e = {K.Ve:.2f}', 12.5, RED, 'start', '700')
    p.dot(0, K.Veq1 + K.Vg, 5, RED); T(cv, p.X(0) + 8, p.Y(K.Veq1 + K.Vg) - 12, f'{K.Veq1 + K.Vg:.2f}', 12, RED, 'start', '700')
    T(cv, p.X(0.6), p.Y(K.phiVs_hinge) - 10, f'塑鉸區 2h：V_c = 0、D13@12 → φV_n = {K.phiVs_hinge:.2f}', 11.5, GRN, 'start')
    T(cv, p.X(3.2), p.Y(K.phiVn_out) + 16, f'2h 外：D13@25（計 V_c）→ φV_n = {K.phiVn_out:.2f}', 11.5, GRN)
    lx = 745
    for i, (col, dash, lab) in enumerate(((ORG, '6 4', '側移方向 1'), (BLUE, '6 4', '側移方向 2'), (RED, None, '包絡＝設計剪力'), (GRN, None, '箍筋設計強度'))):
        px_line(cv, lx, 140 + 22*i, lx + 26, 140 + 22*i, col, 2.6, dash); T(cv, lx + 32, 140 + 22*i, lab, 11.5, C['text'], 'start')
    T(cv, lx, 250, f'M_pr：A⁻ {K.MprAm:.2f}', 11, C['muted'], 'start')
    T(cv, lx, 266, f'A⁺ {K.MprAp:.2f}、B⁻ {K.MprBm:.2f}', 11, C['muted'], 'start')
    T(cv, lx, 282, f'（tf·m，實配、1.25f_y）', 11, C['muted'], 'start')
    T(cv, lx, 306, f'w_u ℓ_n/2 = {K.Vg:.2f} tf', 11, C['muted'], 'start')
    return cv.svg()

def fig_spiral():
    cv = new(900, 330)
    cx, cy, s = 200, 170, 2.6                    # 1 cm = 2.6 px
    cv.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{K.D/2*s:.1f}" fill="#ECEFF1" stroke="{C["member"]}" stroke-width="2"/>')
    cv.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{K.Dc/2*s:.1f}" fill="rgba(46,125,50,0.10)" stroke="{GRN}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    cv.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{K.dsp/2*s:.1f}" fill="none" stroke="{RED}" stroke-width="{1.27*s:.1f}" opacity="0.85"/>')
    rb = (K.dsp / 2 - 1.27 / 2 - 2.54 / 2) * s
    for i in range(9):
        a = 2 * math.pi * i / 9 + math.pi / 2
        cv.parts.append(f'<circle cx="{cx + rb*math.cos(a):.1f}" cy="{cy - rb*math.sin(a):.1f}" r="{2.54/2*s:.1f}" fill="{C["member"]}"/>')
    px_line(cv, cx - K.D/2*s, cy + K.D/2*s + 18, cx + K.D/2*s, cy + K.D/2*s + 18, C['dim'], 1.2)
    T(cv, cx, cy + K.D/2*s + 32, f'D = {K.D:g} cm（保護層 {K.cover:g} cm → 核心 D_c = {K.Dc:g} cm）', 12, C['muted'])
    T(cv, cx, 28, '9-D25、D13 螺箍筋 @7.5 cm（比例 1 cm = 2.6 px）', 12.5, C['text'], 'middle', '700')
    T(cv, cx, 50, '綠虛線＝核心（量到螺箍筋外緣）；紅＝螺箍筋中心線', 11.5, C['muted'])
    p = Plot(cv, 480, 60, 360, 190, (0, 0.016), (0, 4))
    for v in (0, 0.004, 0.008, 0.012, 0.016):
        X = p.X(v); px_line(cv, X, 60, X, 250, '#E6EBF1', 1); T(cv, X, 266, f'{v*100:.1f}%', 11.5, C['muted'])
    rows = [('實配 @7.5', K.rho_act, GRN), ('規範 0.45(A_g/A_c−1)f′_c/f_y', K.rho_req, RED), ('耐震下限 0.12f′_c/f_y', K.rho_min_seis, GRY), ('若改 @8.0', K.rho_s8, ORG)]
    for i, (lab, v, col) in enumerate(rows):
        yc = 60 + 190 * (i + 0.5) / 4
        px_rect(cv, p.X(0), yc - 12, p.X(v) - p.X(0), 24, col, 'none', 0, 3)
        T(cv, p.X(0) + 6, yc - 22, lab, 11.5, C['text'], 'start')
        inside = v < K.rho_req
        T(cv, p.X(v) - 6 if inside else p.X(v) + 6, yc, f'{v*100:.3f}%', 12, '#fff' if inside else col, 'end' if inside else 'start', '700')
    px_line(cv, p.X(K.rho_req), 55, p.X(K.rho_req), 255, RED, 1.2, '4 3')
    T(cv, 660, 300, f'實配 / 規範 = {K.rho_act/K.rho_req:.3f}：只多 1%；螺距放大到 8 cm 就不合格', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_beam_detail():
    """耐震梁的 2h 區、第一支箍筋、搭接禁區與梁寬上限（以 SD-2013-2 尺寸、1 cm = 1 px）"""
    cv = new(900, 400)
    s = 0.95; X0 = 60; Y0 = 70; c = 60 * s; hb = 60 * s; span = 700 * s
    xL, xR = X0 + c, X0 + c + 640 * s * 1.0
    # 立面：左右柱與梁
    for xc in (X0, xR):
        px_rect(cv, xc, Y0 - 30, c, hb + 120, '#ECEFF1', C['member'], 1.6, 0)
    px_rect(cv, xL, Y0, xR - xL, hb, '#FAFAFA', C['member'], 1.6, 0)
    T(cv, (xL + xR) / 2, Y0 - 16, f'淨跨 ℓ_n = {K.ln*100:.0f} cm、梁深 h = 60 cm、d = 53 cm（立面，1 cm ≈ 0.95 px）', 12, C['muted'])
    zone = 2 * 60 * s
    for xa, sg in ((xL, 1), (xR, -1)):
        x2 = xa + sg * zone
        px_rect(cv, min(xa, x2), Y0, zone, hb, 'rgba(198,40,40,0.10)', RED, 1.2, 0, '4 3')
        xs_ = [xa + sg * 5 * s] + [xa + sg * (5 + 12 * i) * s for i in range(1, 10) if (5 + 12 * i) <= 120]
        for x in xs_: px_line(cv, x, Y0 + 4, x, Y0 + hb - 4, RED, 1.6)
        T(cv, (xa + x2) / 2, Y0 + hb + 16, '2h = 120 cm：閉合箍筋 s ≤ min(d/4, 6d_b, 15 cm)', 11, RED)
        T(cv, (xa + x2) / 2, Y0 + hb + 32, '搭接禁區', 11, RED, 'middle', '700')
    for x in np.arange(xL + zone + 25 * s, xR - zone, 25 * s): px_line(cv, x, Y0 + 4, x, Y0 + hb - 4, GRY, 1.2)
    T(cv, (xL + xR) / 2, Y0 + hb + 16, '2h 外：可計 V_c，s ≤ d/2', 11.5, GRY)
    px_arrow(cv, xL + 30, Y0 - 44, xL + 5*s + 1, Y0 + 2, ORG, 1.6, 7)
    T(cv, xL + 34, Y0 - 50, '第一支閉合箍距柱面 ≤ 5 cm', 11.5, ORG, 'start', '700')
    # 平面：梁寬上限
    py = 300; bc = 60 * 0.9; bb = 150 * 0.9
    cxp = 450
    px_rect(cv, cxp - bc/2, py - bc/2, bc, bc, '#ECEFF1', C['member'], 1.6, 0)
    px_rect(cv, cxp - bb/2, py - bc/2 - 40, bb, 40, 'rgba(21,101,192,0.12)', BLUE, 1.4, 0, '5 3')
    px_rect(cv, cxp - 20*0.9, py - bc/2 - 40, 40*0.9, 40, 'rgba(21,101,192,0.35)', BLUE, 1.4, 0)
    T(cv, cxp, py + bc/2 + 16, '柱 c₁ = c₂ = 60 cm（平面）', 11.5, C['muted'])
    T(cv, cxp + bb/2 + 10, py - bc/2 - 20, 'b_w 上限 = c₂ + 2·min(c₂, 0.75c₁) = 150 cm', 12, BLUE, 'start', '700')
    T(cv, cxp + bb/2 + 10, py - bc/2 - 2, '本例 b_w = 40 cm ≪ 150 cm', 11.5, C['muted'], 'start')
    T(cv, cxp - bb/2 - 10, py - bc/2 - 20, '超出柱寬的部分每側 ≤ 45 cm', 11.5, BLUE, 'end')
    T(cv, cxp - bb/2 - 10, py - bc/2 - 2, '（梁筋要能錨進柱、傳力給柱）', 11.5, C['muted'], 'end')
    return cv.svg()

def fig_shortcol():
    """SD-2017-3：牆把柱箍短 → 勁度 ∝ 1/h³ → 剪力集中"""
    cv = new(900, 380)
    lpx = 200; X0 = 80; gap = 110; yb = 70; yg = yb + lpx
    xs = [X0 + i * gap for i in range(4)]
    px_rect(cv, xs[0] - 20, yb - 22, xs[3] - xs[0] + 40, 22, '#90A4AE', C['member'], 1.4, 0)
    T(cv, (xs[0] + xs[3]) / 2, yb - 11, '剛性梁', 12, '#fff', 'middle', '700')
    hatch_ground(cv, xs[0] - 40, xs[3] + 40, yg)
    walls = [(xs[0], xs[1], 0.5), (xs[1], xs[2], 0.25)]
    for a, b_, hh in walls:
        px_rect(cv, a + 5, yg - hh * lpx, b_ - a - 10, hh * lpx, 'rgba(120,144,156,0.35)', GRY, 1.2, 0)
        T(cv, (a + b_) / 2, yg - hh * lpx / 2, f'剛性牆 {"ℓ/2" if hh == 0.5 else "ℓ/4"}', 11, C['text'])
    for i, (x, hf, sh) in enumerate(zip(xs, K.h, K.share)):
        hpx = float(hf) * lpx
        px_line(cv, x, yg, x, yg - lpx, C['member2'], 6)
        px_line(cv, x, yb, x, yb + hpx, RED if i < 2 else C['member'], 6)
        T(cv, x, yg + 24, f'柱 {i+1}', 12.5, C['text'], 'middle', '700')
        T(cv, x + 8, yb + hpx / 2, f'h = {hf}ℓ'.replace('1ℓ', 'ℓ'), 11, RED if i < 2 else C['muted'], 'start')
    T(cv, (xs[0] + xs[3]) / 2, yg + 46, '紅＝可變形段（剛性梁底到牆頂）；兩端固定 → k = 12EI/h³', 11.5, C['muted'])
    px_arrow(cv, xs[0] - 62, yb - 11, xs[0] - 22, yb - 11, RED, 2.6, 10); T(cv, xs[0] - 60, yb - 28, 'V', 14, RED, 'start', '700', True)
    p = Plot(cv, 560, 60, 290, 200, (0, 0.5), (0, 4))
    for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
        X = p.X(v); px_line(cv, X, 60, X, 260, '#E6EBF1', 1); T(cv, X, 276, f'{v:.1f}', 11.5, C['muted'])
    for i, sh in enumerate(K.share):
        yc = 60 + 200 * (i + 0.5) / 4; v = float(sh)
        px_rect(cv, p.X(0), yc - 13, p.X(v) - p.X(0), 26, RED if i < 2 else C['member2'], 'none', 0, 3)
        T(cv, 552, yc, f'柱 {i+1}', 12, C['text'], 'end')
        T(cv, p.X(v) + 6, yc, f'{sh.numerator}/{sh.denominator} = {v:.3f}', 12, C['text'], 'start', '700')
    T(cv, 705, 300, '各柱剪力 / V', 12.5, C['text'], 'middle', '700')
    T(cv, 450, 362, f'柱 1、2 的可變形段只有 ℓ/2 → 勁度是柱 4 的 8 倍，兩根就吃掉 {float(2*K.share[0])*100:.1f}% 的剪力', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_cantilever():
    """SD-2015-4：懸臂梁法——柱軸力 ∝ 到形心距離、彎矩圖"""
    cv = new(900, 400)
    s = 34; X0 = 120; yt = 110; yg = yt + K.H * s
    xs = [X0 + x * s for x in K.xs]
    px_line(cv, xs[0], yt, xs[2], yt, C['member'], 4)
    for x in xs: px_line(cv, x, yt, x, yg, C['member'], 4)
    for x in xs: hatch_ground(cv, x - 18, x + 18, yg)
    px_arrow(cv, xs[0] - 70, yt, xs[0] - 6, yt, RED, 2.6, 10); T(cv, xs[0] - 72, yt - 14, f'P = {K.P:g} tf', 12.5, RED, 'start', '700')
    xb = X0 + K.xbar * s
    px_line(cv, xb, yt - 70, xb, yt - 52, PUR, 1.4, '6 4'); px_line(cv, xb, yt + 4, xb, yg + 40, PUR, 1.4, '6 4'); T(cv, xb + 6, yt - 64, f'柱群形心 x̄ = {K.xbar:g} m', 12, PUR, 'start', '700')
    # 彎矩圖（畫在受拉側；反曲點在中點）
    sc = 2.6
    for (xa, xb_, M) in ((xs[0], xs[1], K.Mb12), (xs[1], xs[2], K.Mb23)):
        xm = (xa + xb_) / 2
        px_polygon(cv, [(xa, yt), (xa, yt - M*sc), (xm, yt), (xb_, yt + M*sc), (xb_, yt)], 'rgba(46,125,111,0.25)', C['bmd'], 1.4)
        T(cv, xa + 6, yt - M*sc - 8, f'{M:.2f}', 11.5, C['bmd'], 'start', '700')
    for x, M in zip(xs, K.Mc):
        ym = (yt + yg) / 2
        px_polygon(cv, [(x, yt), (x - M*sc, yt), (x, ym), (x + M*sc, yg), (x, yg)], 'rgba(46,125,111,0.25)', C['bmd'], 1.4)
        T(cv, x + M*sc + 8, yg - 24, f'{M:.2f}', 11.5, C['bmd'], 'start', '700')
    # 柱軸力（柱底反力方向：壓＝向上推）
    for x, Nv in zip(xs, K.N):
        col = BLUE if Nv > 0 else RED
        L_ = 18 + 16 * abs(Nv)
        if Nv > 0: px_arrow(cv, x + 26, yg + 60, x + 26, yg + 60 - L_, col, 2.4, 8)
        else: px_arrow(cv, x + 26, yg + 60 - L_, x + 26, yg + 60, col, 2.4, 8)
        T(cv, x + 34, yg + 50, f'{"壓" if Nv > 0 else "拉"} {abs(Nv):.3f}', 11.5, col, 'start', '700')
    for i, (a, b_, L_) in enumerate(((xs[0], xs[1], 7), (xs[1], xs[2], 10))):
        T(cv, (a + b_) / 2, yt - 50 if i == 0 else yt - 52, f'{L_} m', 12, C['muted'])
    T(cv, xs[2] + 50, (yt + yg) / 2, f'h = {K.H:g} m', 12, C['muted'], 'start')
    T(cv, 450, 386, '彎矩單位 tf·m，反曲點都在桿件中點；柱底箭頭為地面給柱的反力：左、中柱受拉，右柱受壓', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_collapse():
    """SD-2010-4：(a) 左柱底鉸 (b) 兩柱底固定——塑鉸位置與推覆曲線"""
    cv = new(900, 360)
    for k, (x0, lab, pinL) in enumerate(((60, '(a) 左柱底鉸、右柱底固定', True), (260, '(b) 兩柱底固定', False))):
        L_ = 120; yt, yg = 100, 220; w_ = 110; dx = 26
        T(cv, x0 + w_/2, 52, lab, 12.5, C['text'], 'middle', '700')
        px_line(cv, x0, yt, x0 + w_, yt, C['ghost'], 3)
        px_line(cv, x0 + dx, yt, x0 + w_ + dx, yt, C['member'], 6)
        for xc, pinned in ((x0, pinL), (x0 + w_, False)):
            px_line(cv, xc + dx, yt, xc, yg, C['member'], 3)
            hatch_ground(cv, xc - 14, xc + 14, yg + (8 if pinned else 0))
            if pinned:
                px_polygon(cv, [(xc, yg), (xc - 7, yg + 8), (xc + 7, yg + 8)], '#fff', C['member'], 1.4)
            hinges = [(xc + dx, yt)] + ([] if pinned else [(xc, yg)])
            for hx, hy in hinges:
                cv.parts.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="5.5" fill="{RED}" stroke="#fff" stroke-width="1.5"/>')
        n = 3 if pinL else 4
        T(cv, x0 + w_/2 + 13, yg + 34, f'{n} 個塑鉸 → V = {n}M_p/L', 12, RED, 'middle', '700')
        T(cv, x0 + w_/2 + 13, yg + 54, f'k = {15 if pinL else 24}EI/L³', 12, C['muted'])
    p = Plot(cv, 520, 50, 330, 220, (0, 0.6), (0, 4.6))
    p.frame([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0, 1, 2, 3, 4], 'Δ（M_pL²/EI）', 'V（M_p/L）', xfmt='{:.1f}')
    p.curve([q[0] for q in K.push_a], [q[1] for q in K.push_a], ORG, 3)
    p.curve([q[0] for q in K.push_b], [q[1] for q in K.push_b], BLUE, 3)
    p.dot(K.d1_a, K.V1_a, 4.5, ORG); T(cv, p.X(K.d1_a) + 6, p.Y(K.V1_a) + 14, '右柱兩端先降伏', 11, ORG, 'start')
    p.dot(K.d2_a, K.V2_a, 4.5, ORG); T(cv, p.X(K.d2_a) + 6, p.Y(K.V2_a) + 14, '左柱頂降伏 → 機構 3M_p/L', 11, ORG, 'start')
    p.dot(K.d1_b, K.V1_b, 4.5, BLUE); T(cv, p.X(K.d1_b) + 6, p.Y(K.V1_b) - 12, '四鉸同時 → 4M_p/L', 11, BLUE, 'start')
    T(cv, 450, 330, f'頻率比 ω_a/ω_b = √(15/24) = {K.w_ratio:.3f}；崩塌側力比 V_a/V_b = 3/4 → (b) 勁度與強度都較高', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_pushover():
    cv = new(900, 340)
    T(cv, 450, 24, '3 層算例（等質量、層高 3 m、V = 600 kN、T = 2.5 s）的五種側推力分布', 13.5, C['text'], 'middle', '700')
    cols = [GRY, BLUE, ORG, RED, GRN]
    W = 170
    for j, ((nm, F), col) in enumerate(zip(K.DIST, cols)):
        x0 = 20 + j * W; yb = 290
        px_line(cv, x0 + 40, yb, x0 + 40, yb - 3 * 70, C['member'], 3)
        hatch_ground(cv, x0 + 25, x0 + 55, yb)
        for i in range(3):
            y = yb - (i + 1) * 70
            Lp = F[i] * 0.28
            px_arrow(cv, x0 + 42, y, x0 + 42 + Lp, y, col, 2.6, 8)
            T(cv, x0 + 46 + Lp, y - 11, f'{F[i]:.1f}', 11, col, 'start', '700')
            cv.parts.append(f'<circle cx="{x0+40}" cy="{y}" r="4" fill="{C["member"]}"/>')
        T(cv, x0 + 70, yb + 24, nm, 12.5, col, 'middle', '700')
    T(cv, 450, 330, '箭頭長度與力成正比（kN）。越往右，頂層越大：指數與經驗式反映長週期的高振態，SRSS 是由層剪力組合後差分得到的單一分布', 11.5, C['muted'])
    return cv.svg()

def fig_flow():
    cv = new(900, 560)
    BX = 260
    box(cv, BX, 36, 300, 44, ['讀題：計算題還是論述題？'], '#ECEFF1', '#546E7A', bold_first=True)
    diamond(cv, BX, 116, 220, 64, ['有側力、要分柱剪力？'])
    edge(cv, [(BX, 58), (BX, 84)])
    box(cv, 690, 116, 300, 58, ['先找每根柱的「可變形段」h', 'k ∝ 1/h³ 分配（§5）→ 短柱檢查'], '#E3F2FD', '#1565C0')
    edge(cv, [(BX + 110, 116), (540, 116)], '是', (BX + 122, 104))
    diamond(cv, BX, 210, 220, 64, ['多跨構架求彎矩？'])
    edge(cv, [(BX, 148), (BX, 178)], '否', (BX + 8, 164))
    box(cv, 690, 210, 300, 58, ['懸臂梁法：形心 → N ∝ A·d', '→ 梁剪力 → 端彎矩（§6）'], '#E3F2FD', '#1565C0')
    edge(cv, [(BX + 110, 210), (540, 210)], '是', (BX + 122, 198))
    diamond(cv, BX, 304, 220, 64, ['問崩塌／塑鉸？'])
    edge(cv, [(BX, 242), (BX, 272)], '否', (BX + 8, 258))
    box(cv, 690, 304, 300, 58, ['數塑鉸：V = ΣM_p / L', '推覆曲線依降伏順序（§7）'], '#E3F2FD', '#1565C0')
    edge(cv, [(BX + 110, 304), (540, 304)], '是', (BX + 122, 292))
    diamond(cv, BX, 398, 220, 64, ['RC 梁柱配筋？'])
    edge(cv, [(BX, 336), (BX, 366)], '否', (BX + 8, 352))
    box(cv, 690, 398, 300, 58, ['實配筋 → M_pr(1.25f_y) → V_e', '→ V_c = 0？→ 箍筋 s（§2、§4）'], '#E3F2FD', '#1565C0')
    edge(cv, [(BX + 110, 398), (540, 398)], '是', (BX + 122, 386))
    box(cv, BX, 492, 300, 58, ['論述題：先排破壞模式', '延性准許、脆性擋住 → 條文＋理由'], '#F3E5F5', '#6A1B9A')
    edge(cv, [(BX, 430), (BX, 463)], '否', (BX + 8, 446))
    box(cv, 690, 506, 300, 50, ['收尾：剪力和＝V？軸力和＝0？', '條文寫現行版本（111／112 年）'], '#FFF8E1', '#F9A825')
    edge(cv, [(840, 116), (870, 116), (870, 506), (840, 506)])
    for y in (210, 304, 398):
        px_line(cv, 840, y, 870, y, C['member'], 1.6)
    edge(cv, [(410, 492), (540, 506)])
    return cv.svg()

FIGS = dict(f0=fig_overview, f1=fig_capacity_shear, f2=fig_spiral, f3=fig_beam_detail, f4=fig_shortcol,
            f5=fig_cantilever, f6=fig_collapse, f7=fig_pushover, f8=fig_flow)

if __name__ == '__main__':
    html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', '..', 'study', 'lecture-SD-U3-1.html')
    embed(html, {k: f() for k, f in FIGS.items()})

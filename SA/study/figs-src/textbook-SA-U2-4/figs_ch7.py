# -*- coding: utf-8 -*-
"""第 7 章：特殊元素（旋轉彈簧、彈簧支承、半剛接、格床扭轉）。數值取自 calcs。"""
from figs_common import *  # noqa
from calcs import semirigid_2019, sp, L_, EI


def _rot_spring(x, y, r=16, c=TEN):
    """零長度旋轉彈簧（螺旋）。"""
    pts = []
    for k in range(120):
        a = k / 119 * 4 * math.pi
        rr = 4 + (r - 4) * k / 119
        pts.append((x + rr * math.cos(a), y - rr * math.sin(a)))
    return P(pts, c, 2)


def fig7_1():
    W, H = 900, 380
    o = T(225, 34, '(a) 旋轉彈簧元素：兩個轉角、一支彈簧', 16, INK, 'middle', 'bold')
    cx, cy = 225, 170
    o += L(cx - 170, cy, cx - 6, cy, INK, 5) + L(cx + 6, cy, cx + 170, cy, INK, 5)
    o += _rot_spring(cx, cy, 20)
    o += arc_arrow(cx - 60, cy, 24, -40, 200, AC, 2.4, 10) + T(cx - 60, cy - 36, 'θ_{i}', 16, AC, 'middle', 'bold')
    o += arc_arrow(cx + 60, cy, 24, -40, 200, AC, 2.4, 10) + T(cx + 60, cy - 36, 'θ_{j}', 16, AC, 'middle', 'bold')
    o += T(cx, cy + 46, '*M* ＝ *k*_{θ}(θ_{i} − θ_{j})', 17, TEN, 'middle', 'bold')
    o += mat_grid(cx - 70, 248, [['+*k*_{θ}', '−*k*_{θ}'], ['−*k*_{θ}', '+*k*_{θ}']], 70, 38, size=16)
    o += T(cx, 350, '*k*_{θ}→∞：剛接（θ_{i}＝θ_{j}）　*k*_{θ}→0：鉸接', 14, MUT, 'middle')
    o += L(450, 20, 450, 360, GRID, 1.2)
    o += T(675, 34, '(b) 彈簧支承：一端接地的彈簧', 16, INK, 'middle', 'bold')
    bx, by = 560, 140
    o += L(bx, by, bx + 230, by, INK, 5) + node(bx + 115, by, 7)
    sx = bx + 115
    pts = [(sx, by + 8), (sx, by + 18)]
    for k in range(8):
        pts.append((sx + (12 if k % 2 == 0 else -12), by + 22 + k * 8))
    pts += [(sx, by + 90), (sx, by + 100)]
    o += P(pts, TEN, 2.2) + hatch_ground(sx - 26, by + 100, 52)
    o += T(sx + 22, by + 60, '*k*_{s}', 17, TEN, 'start', 'bold')
    o += A(sx - 40, by - 10, sx - 40, by - 54, AC, 2.4, 10) + T(sx - 48, by - 50, '*v*', 16, AC, 'end', 'bold')
    o += R(560, 270, 230, 70, KEY2, KEY, 1.6, 9)
    o += T(675, 298, '只在 *K*_{vv} 加 *k*_{s}', 16, KEY, 'middle', 'bold')
    o += T(675, 324, '（另一端是地，沒有自由度）', 14, MUT, 'middle')
    return svg(W, H, o, '旋轉彈簧元素與彈簧支承')


def fig7_2():
    W, H = 900, 430
    N = {'A': (0, 0), 'B': (0, 1), 'C': (1, 0), 'D': (1, 1), 'E': (2, 1)}
    X0, Y0, sc = 100, 330, 160
    S = lambda p: (X0 + p[0] * sc, Y0 - p[1] * sc)
    o = ''
    bx, by = S(N['B'])
    o += L(*S(N['A']), bx, by, INK, 5) + L(bx + 14, by, *S(N['D']), INK, 5)
    o += L(*S(N['C']), *S(N['D']), INK, 5) + L(*S(N['D']), *S(N['E']), INK, 5)
    o += _rot_spring(bx + 7, by, 13)
    o += fixed_wall(*S(N['A']), 50) + pin(*S(N['C']))
    ex, ey = S(N['E'])
    o += C(ex, ey + 9, 8, '#fff', INK, 1.8) + hatch_ground(ex - 18, ey + 17, 36)
    for nm, (dx, dy) in {'A': (-26, 4), 'B': (-22, -12), 'C': (-26, 4), 'D': (-8, -14), 'E': (10, -14)}.items():
        x, y = S(N[nm]); o += T(x + dx, y + dy, nm, 16, INK, 'middle', 'bold')
    # 元素編號
    for t, p in (('①', (0, 0.3)), ('②', (1, 0.3)), ('③', (0.1, 1.3)), ('④', (0.5, 0.86)), ('⑤', (1.5, 0.86))):
        x, y = S(p); o += T(x + (14 if t in '①②' else 0), y, t, 17, KEY, 'start' if t in '①②' else 'middle', 'bold')
    # 載重
    for p, lab in (((0, 0.5), '*P*'), ((1, 0.5), '*Q*')):
        x, y = S(p); o += A(x - 56, y, x - 6, y, COMP, 2.6, 10) + T(x - 60, y + 6, lab, 16, COMP, 'end', 'bold')
    dx_, dy_ = S(N['D'])
    for k in range(7):
        xx = dx_ + 12 + k * (sc - 24) / 6
        o += A(xx, dy_ - 40, xx, dy_ - 6, COMP, 1.6, 8)
    o += L(dx_ + 12, dy_ - 40, ex - 12, dy_ - 40, COMP, 1.6) + T((dx_ + ex) / 2, dy_ - 50, '*w*', 16, COMP, 'middle', 'bold')
    o += A(ex + 6, ey, ex + 54, ey, COMP, 2.6, 10) + T(ex + 58, ey + 6, '*R*', 16, COMP, 'start', 'bold')
    # 自由度
    o += A(ex + 6, ey + 46, ex + 60, ey + 46, AC, 2.4, 10) + T(ex + 64, ey + 52, '*d*_{1}', 15, AC, 'start', 'bold')
    o += arc_arrow(bx - 4, by, 26, 120, 250, AC, 2.4, 10) + T(bx - 34, by + 28, '*d*_{2}', 15, AC, 'end', 'bold')
    o += arc_arrow(bx + 18, by, 26, -60, 60, AC, 2.4, 10) + T(bx + 46, by + 32, '*d*_{3}', 15, AC, 'start', 'bold')
    o += arc_arrow(dx_, dy_, 26, 200, 330, AC, 2.4, 10) + T(dx_ - 28, dy_ + 34, '*d*_{4}', 15, AC, 'end', 'bold')
    o += T(250, 30, 'SA-2019-4：③ 旋轉彈簧 *k*_{θ}＝10*EI*/*L*', 16, INK, 'middle', 'bold')
    # [K] 格子
    sr = semirigid_2019()
    K = sr['K']
    lab = []
    for i in range(4):
        row = []
        for j in range(4):
            v = sp.simplify(K[i, j] * L_**3 / EI)
            c = sp.Poly(v, L_).coeffs()[0] if v != 0 else 0
            pw = sp.degree(v, L_) if v != 0 else 0
            row.append('0' if v == 0 else (f'{c}'.replace('-', '−') + ('' if pw == 0 else ('*L*' if pw == 1 else '*L*^{2}'))))
        lab.append(row)
    col = [[KEY2, AC2, None, '#e0f2f1'], [AC2, KEY2, TEN2, None], [None, TEN2, KEY2, WARN2], ['#e0f2f1', None, WARN2, KEY2]]
    o += mat_grid(560, 110, lab, 80, 44, hdr=('*d*_{1}', '*d*_{2}', '*d*_{3}', '*d*_{4}'), rowhdr=('*d*_{1}', '*d*_{2}', '*d*_{3}', '*d*_{4}'), colors=col, size=15)
    o += T(720, 70, '[*K*]（× *EI*/*L*^{3}）', 16, INK, 'middle', 'bold')
    o += T(720, 316, '藍＝柱 ①、青＝柱 ②、綠＝彈簧 ③、橘＝梁 ④', 14, MUT, 'middle')
    o += T(720, 340, '紫色對角＝多個元素相加：15＝12＋3、14＝4＋10、', 14, MUT, 'middle')
    o += T(720, 362, '14＝10＋4、10＝3＋4＋3（柱②、梁④、梁⑤）', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2019-4 半剛接構架')


def fig7_3():
    W, H = 900, 380
    X0, Y0, sc = 200, 170, 150
    S = lambda p: (X0 + p[0] * sc, Y0 - p[1] * sc)
    o = ''
    ax, ay = S((-1, 0)); bx, by = S((0, 0)); cx, cy = S((0, -1)); dx_, dy_ = S((1, 0))
    G = 56
    o += L(ax, ay, bx, by, INK, 5) + L(bx, by, cx, cy, INK, 5) + L(bx + G, by, dx_, dy_, INK, 5)
    o += vwall(ax, ay, 56) + fixed_wall(cx, cy, 50) + vwall(dx_, dy_, 56, left=False)
    o += _rot_spring(bx + G / 2, by - 2, 12)
    o += node(bx, by, 6) + node(bx + G, by, 6)
    o += T(bx - 6, by + 30, 'B1', 15, INK, 'end', 'bold') + T(bx + G + 6, by + 30, 'B2', 15, INK, 'start', 'bold')
    o += T(ax - 14, ay - 30, 'A', 16, INK, 'middle', 'bold') + T(cx + 26, cy + 4, 'C', 16, INK, 'middle', 'bold') + T(dx_ + 16, dy_ - 30, 'D', 16, INK, 'middle', 'bold')
    for k in range(6):
        xx = ax + 8 + k * (sc - 50) / 5
        o += A(xx, ay - 40, xx, ay - 6, COMP, 1.6, 8)
    o += L(ax + 8, ay - 40, bx - 42, ay - 40, COMP, 1.6) + T((ax + bx) / 2 - 20, ay - 50, '*w*（AB 全長）', 15, COMP, 'middle', 'bold')
    mx = (bx + G + dx_) / 2
    o += A(mx, by - 60, mx, by - 6, COMP, 2.6, 10) + T(mx + 8, by - 50, '*P*', 16, COMP, 'start', 'bold')
    o += arc_arrow(bx, by, 22, 160, 20, AC, 2.4, 10) + T(bx, by - 34, '*r*_{1}', 15, AC, 'middle', 'bold')
    o += A(bx + G, by + 14, bx + G, by + 60, AC, 2.4, 10) + T(bx + G + 10, by + 66, '*r*_{2}（向下）', 15, AC, 'start', 'bold')
    o += arc_arrow(bx + G, by, 22, 160, 20, AC, 2.4, 10) + T(bx + G, by - 34, '*r*_{3}', 15, AC, 'middle', 'bold')
    o += T(450, 30, 'SA-2015-4：B 拆成兩個節點；轉角以順時針為正', 16, INK, 'middle', 'bold')
    o += R(560, 190, 320, 160, '#fff', WARN, 2, 12)
    o += T(720, 220, '線性彈簧 *k*_{s} 去哪了？', 16, WARN, 'middle', 'bold')
    o += T(580, 254, '忽略軸向變形 → AB 不伸縮 → *u*_{B1}＝0', 14, INK, 'start')
    o += T(580, 282, 'BD 不伸縮、D 固定 → *u*_{B2}＝0', 14, INK, 'start')
    o += T(580, 310, '彈簧兩端都不動 → 不變形、不出力', 14, INK, 'start')
    o += T(720, 338, '→ 不進 [*K*]，也沒有自由度', 15, WARN, 'middle', 'bold')
    return svg(W, H, o, 'SA-2015-4 彈簧接頭')


def fig7_4():
    W, H = 900, 420
    X0, Y0, sc = 120, 340, 240
    S = lambda p: (X0 + p[0] * sc, Y0 - p[1] * sc)
    d_, a_, b_, c_ = S((0, 0)), S((1, 0)), S((1, 1)), S((0, 1))
    o = L(*a_, *b_, INK, 6) + L(*b_, *c_, INK, 6) + L(*c_, *d_, INK, 6)
    o += L(*d_, *a_, GRID, 1.4, '5 4')
    for p in (a_, d_):
        o += R(p[0] - 9, p[1] - 9, 18, 18, STEEL3, INK, 1.6)
    for nm, p, dxy in (('a', a_, (18, 22)), ('b', b_, (20, -12)), ('c', c_, (-20, -12)), ('d', d_, (-18, 22))):
        o += T(p[0] + dxy[0], p[1] + dxy[1], nm, 17, INK, 'middle', 'bold')
    # 均布（平面圖用 ⊗ 表示向下）
    for k in range(6):
        x = c_[0] + 20 + k * (sc - 40) / 5
        o += C(x, c_[1] - 22, 7, '#fff', COMP, 1.6) + L(x - 5, c_[1] - 27, x + 5, c_[1] - 17, COMP, 1.4) + L(x - 5, c_[1] - 17, x + 5, c_[1] - 27, COMP, 1.4)
    o += T((b_[0] + c_[0]) / 2, c_[1] - 40, 'ω（向下，−*z*）', 15, COMP, 'middle', 'bold')
    # 轉角向量（雙箭頭）
    bx, by = b_
    o += A(bx - 24, by + 44, bx - 24, by + 124, AC, 2.6, 11) + A(bx - 24, by + 44, bx - 24, by + 110, AC, 2.6, 11)
    o += T(bx - 34, by + 118, 'φ：繞 ab 軸', 15, AC, 'end', 'bold')
    o += A(bx - 40, by + 24, bx - 120, by + 24, KEY, 2.6, 11) + A(bx - 40, by + 24, bx - 106, by + 24, KEY, 2.6, 11)
    o += T(bx - 130, by + 30, 'ψ：繞 bc 軸', 15, KEY, 'end', 'bold')
    o += T(X0 + sc / 2, 30, 'SA-2025-4 格床（平面圖，雙箭頭＝右手定則轉角向量）', 16, INK, 'middle', 'bold')
    # 右側表
    x0 = 470
    o += R(x0, 64, 410, 270, '#fff', TEAL, 2, 12)
    o += T(x0 + 205, 94, '🌱 S4 的轉角版：投影到桿軸', 16, TEAL, 'middle', 'bold')
    hdr = ('', 'ab 桿', 'bc 桿')
    rows = [('φ（沿 ab）', '扭轉 *GJ*/*L*', '彎曲'), ('ψ（沿 bc）', '彎曲', '扭轉 *GJ*/*L*'), ('*w*_{b}（垂直）', '彎曲（剪力）', '彎曲（剪力）')]
    for j, h in enumerate(hdr):
        o += T(x0 + 70 + j * 130, 132, h, 15, MUT, 'middle', 'bold')
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            o += T(x0 + 70 + j * 130, 170 + i * 40, v, 15, [AC, KEY, TEN][i] if j == 0 else INK, 'middle', 'bold')
    o += T(x0 + 205, 296, '轉角向量沿桿軸 → 扭；垂直桿軸 → 彎', 15, TEAL, 'middle', 'bold')
    o += T(x0 + 205, 322, '實心圓桿 *J* ＝ π*d*^{4}/32 ＝ 2*I*', 15, INK, 'middle', 'bold')
    o += T(450, 400, '對稱於 bc 中垂線 → φ_{c}＝−φ_{b}、ψ_{c}＝ψ_{b}、*w*_{c}＝*w*_{b}：6 個未知數只剩 3 個', 15, MUT, 'middle')
    return svg(W, H, o, '格床：彎與扭互換')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4}

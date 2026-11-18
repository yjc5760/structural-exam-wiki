# -*- coding: utf-8 -*-
"""第 4 章：斜桿與座標轉換。幾何由 c、s 與 calcs.truss_2013() 的數值算出。"""
from figs_common import *  # noqa
from calcs import truss_2013

CS = (0.8, 0.6)   # 示意用斜桿（3-4-5）


def _bar(ix, iy, Lp, c, s):
    jx, jy = ix + Lp * c, iy - Lp * s
    return jx, jy, L(ix, iy, jx, jy, TEN, 7) + node(ix, iy, 7) + node(jx, jy, 7)


def fig4_1():
    W, H = 900, 400
    c, s = CS
    ix, iy, Lp = 90, 330, 330
    jx, jy, o = _bar(ix, iy, Lp, c, s)
    o += T(ix - 6, iy + 30, '*i*（鎖住）', 15, INK, 'middle', 'bold')
    o += T(jx - 30, jy + 34, '*j*', 16, INK, 'middle', 'bold')
    # 軸線延長
    o += L(jx, jy, jx + 150 * c, jy - 150 * s, TEN, 1.4, '6 4')
    u, v = 120, 40           # 像素
    px, py = jx + u, jy - v
    o += A(jx, jy, px, jy, AC, 2.6, 11) + T(jx + u / 2, jy + 24, '*u*', 17, AC, 'middle', 'bold')
    o += A(px, jy, px, py, AC, 2.6, 11) + T(px + 14, jy - v / 2 + 6, '*v*', 17, AC, 'start', 'bold')
    o += A(jx, jy, px, py, KEY, 2.2, 10, dash='5 4')
    o += C(px, py, 6, KEY, '#fff', 1.6)
    e = u * c + v * s
    fx, fy = jx + e * c, jy - e * s
    o += L(px, py, fx, fy, MUT, 1.4, '3 3')
    # 兩段：u·c（藍）與 v·s（綠）沿軸
    ax, ay = jx + u * c * c, jy - u * c * s
    nx, ny = -s, -c   # 垂直於桿、往左上（畫面座標）
    off = 26
    o += L(jx + nx * off, jy + ny * off, ax + nx * off, ay + ny * off, AC, 5)
    o += L(ax + nx * off, ay + ny * off, fx + nx * off, fy + ny * off, TEN, 5)
    o += T((jx + ax) / 2 + nx * (off + 22) - 6, (jy + ay) / 2 + ny * (off + 22), '*c*·*u*', 16, AC, 'middle', 'bold')
    o += T((ax + fx) / 2 + nx * (off + 22) + 4, (ay + fy) / 2 + ny * (off + 22), '*s*·*v*', 16, TEN, 'middle', 'bold')
    o += T(ix + 120, iy - 30, 'θ', 17, INK, 'middle', 'bold', italic=True)
    o += f'<path d="M{f(ix + 80)},{f(iy)} A80,80 0 0 0 {f(ix + 80 * c)},{f(iy - 80 * s)}" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    o += L(ix, iy, ix + 130, iy, INK, 1.2, '4 3')
    o += R(560, 60, 320, 210, '#fff', TEAL, 2, 12)
    o += T(720, 92, '🌱 種子 S4：桿子只看得見', 16, TEAL, 'middle', 'bold')
    o += T(720, 118, '沿著自己的那一段', 16, TEAL, 'middle', 'bold')
    o += T(720, 168, '伸長 *e* ＝ *c*·*u* ＋ *s*·*v*', 19, KEY, 'middle', 'bold')
    o += T(720, 204, '*c* ＝ cos θ、*s* ＝ sin θ', 15, INK, 'middle')
    o += T(720, 236, '垂直桿軸的位移 → 伸長 0', 15, MUT, 'middle')
    o += T(720, 316, f'示意：*c*＝{c}、*s*＝{s}、*u*:*v*＝3:1', 14, MUT, 'middle')
    return svg(W, H, o, '斜桿伸長量＝位移投影')


def fig4_2():
    W, H = 900, 380
    c, s = CS
    ix, iy, Lp = 150, 280, 270
    jx, jy, o = _bar(ix, iy, Lp, c, s)
    o += T(ix - 4, iy + 30, '*i*', 16, INK, 'middle', 'bold') + T(jx + 4, jy + 34, '*j*', 16, INK, 'middle', 'bold')
    Fp = 110
    o += A(jx, jy, jx + Fp * c, jy - Fp * s, COMP, 3.2, 13)
    o += T(jx + Fp * c + 8, jy - Fp * s - 8, '*N*', 17, COMP, 'start', 'bold')
    o += A(jx, jy, jx + Fp * c, jy, COMP, 1.8, 10, dash='5 4') + T(jx + Fp * c + 8, jy + 6, '*N c*', 15, COMP, 'start', 'bold')
    o += A(jx + Fp * c, jy, jx + Fp * c, jy - Fp * s, COMP, 1.8, 10, dash='5 4')
    o += T(jx + Fp * c + 8, jy - Fp * s / 2 + 18, '*N s*', 15, COMP, 'start', 'bold')
    o += A(ix, iy, ix - 80 * c, iy + 80 * s, COMP, 3.2, 13)
    o += T(ix - 80 * c - 10, iy + 80 * s + 4, '−*N*', 16, COMP, 'end', 'bold')
    o += T(250, 40, '要讓桿伸長 *e*，*j* 端得往外拉 *N*＝*k e*；*i* 端反向', 15, INK, 'middle', 'bold')
    # 右：三步推出 c²、cs、s²
    x0 = 520
    steps = [('① 推 *u*_{j}＝1', '伸長 *e*＝*c*（S4）', AC),
             ('② 拉力', '*N*＝*k*·*c*（S2）', TEN),
             ('③ 投影回 *x*、*y*', '*N c*＝*k c*^{2}、*N s*＝*k cs*', COMP)]
    for i, (a, b, cc) in enumerate(steps):
        y = 64 + i * 78
        o += R(x0, y, 360, 62, '#fff', cc, 1.8, 10)
        o += T(x0 + 16, y + 26, a, 15, cc, 'start', 'bold')
        o += T(x0 + 16, y + 50, b, 16, INK, 'start', 'bold')
    o += R(x0, 304, 360, 56, KEY2, KEY, 1.8, 10)
    o += T(x0 + 180, 338, '[*k*]_{jj} ＝ *k*·[*c*^{2}  *cs* ; *cs*  *s*^{2}]', 17, KEY, 'middle', 'bold')
    return svg(W, H, o, '伸長→軸力→投影：c²、cs、s²')


def _mini(x0, ang, title, mat):
    o = T(x0 + 140, 34, title, 16, INK, 'middle', 'bold')
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    cx, cy = x0 + 85, 160
    Lp = 66
    o += L(cx - Lp * c, cy + Lp * s, cx + Lp * c, cy - Lp * s, TEN, 7)
    o += node(cx + Lp * c, cy - Lp * s, 6) + node(cx - Lp * c, cy + Lp * s, 6)
    o += mat_grid(x0 + 175, 120, mat, 50, 38, size=16)
    return o


def fig4_3():
    W, H = 900, 300
    o = ''
    o += _mini(0, 0, '水平桿 θ＝0°', [['1', '0'], ['0', '0']])
    o += _mini(300, 90, '垂直桿 θ＝90°', [['0', '0'], ['0', '1']])
    o += _mini(600, 45, '45° 桿', [['½', '½'], ['½', '½']])
    for x in (300, 600):
        o += L(x, 20, x, 280, GRID, 1.2)
    o += T(450, 280, '[*c*^{2} *cs* ; *cs* *s*^{2}]（×*EA*/*L*）：水平桿只擋水平、垂直桿只擋垂直、45° 桿推 *x* 也會頂 *y*', 14, MUT, 'middle')
    return svg(W, H, o, '三個方向的檢查')


def fig4_4():
    W, H = 900, 440
    t = truss_2013()
    N = {'A': (0, 0), 'B': (14, 0), 'C': (0, 6), 'D': (6, 6)}
    X0, Y0, sc = 110, 340, 36
    S = lambda p: (X0 + p[0] * sc, Y0 - p[1] * sc)
    o = ''
    names = {'AB': ('A', 'B'), 'AD': ('A', 'D'), 'CD': ('C', 'D'), 'BD': ('B', 'D')}
    for nm, (i, j) in names.items():
        Nf = t['N'][nm]
        wdt = 3 + 6 * abs(Nf) / 150
        o += L(*S(N[i]), *S(N[j]), COMP if Nf > 0 else AC, wdt)
        mx, my = (S(N[i])[0] + S(N[j])[0]) / 2, (S(N[i])[1] + S(N[j])[1]) / 2
        offs = {'AB': (0, 26, 'middle'), 'AD': (-16, -6, 'end'), 'CD': (-20, -14, 'middle'), 'BD': (44, -8, 'start')}[nm]
        o += T(mx + offs[0], my + offs[1], f'{nm} {Nf:+.2f}', 15, COMP if Nf > 0 else AC, offs[2], 'bold')
    o += pin(*S(N['A'])) + pin(*S(N['C']))
    bx, by = S(N['B'])
    o += C(bx, by + 8, 7, '#fff', INK, 1.8) + hatch_ground(bx - 18, by + 15, 36)
    for nm, (dx, dy) in {'A': (-22, -6), 'B': (20, -14), 'C': (-22, -6), 'D': (0, -22)}.items():
        x, y = S(N[nm]); o += T(x + dx, y + dy, nm, 17, INK, 'middle', 'bold')
    dx_, dy_ = S(N['D'])
    o += A(dx_ + 10, dy_ - 40, dx_ + 60, dy_ - 40, KEY, 2.4, 10) + T(dx_ + 66, dy_ - 34, '*d*_{2}', 15, KEY, 'start', 'bold')
    o += A(dx_ - 26, dy_ - 10, dx_ - 26, dy_ - 60, KEY, 2.4, 10) + T(dx_ - 30, dy_ - 66, '*d*_{3}', 15, KEY, 'end', 'bold')
    o += A(bx + 14, by - 30, bx + 64, by - 30, KEY, 2.4, 10) + T(bx + 40, by - 40, '*d*_{1}', 15, KEY, 'middle', 'bold')
    yy = Y0 + 58
    for a, b, t_ in ((0, 6, '6 m'), (6, 14, '8 m')):
        o += dim(S((a, 0))[0], yy, S((b, 0))[0], yy, '', MUT)
        o += T((S((a, 0))[0] + S((b, 0))[0]) / 2, yy + 22, t_, 14, MUT, 'middle')
    xx = X0 - 60
    o += dim(xx, Y0, xx, S((0, 6))[1], '', MUT)
    o += T(xx - 8, (Y0 + S((0, 6))[1]) / 2 + 5, '6 m', 14, MUT, 'end')
    o += T(450, 30, 'SA-2013-4 桿力（kN，拉＋；紅＝拉、線寬∝內力）', 16, INK, 'middle', 'bold')
    P = t['P']
    o += R(640, 60, 240, 100, KEY2, KEY, 1.6, 10)
    o += T(760, 88, '{*P*} ＝ [*K*]{*d*}', 16, KEY, 'middle', 'bold')
    o += T(760, 116, f'＝ ({P[0]:.2f}, {P[1]:.2f}, {P[2]:.2f})', 15, INK, 'middle', 'bold')
    o += T(760, 144, '≈ (80, 100, 150) kN', 15, INK, 'middle', 'bold')
    return svg(W, H, o, 'SA-2013-4 桁架')


def fig4_5():
    W, H = 900, 320
    c, s = CS
    ix, iy, Lp = 100, 285, 240
    jx, jy = ix + Lp * c, iy - Lp * s
    o = L(ix, iy, jx, jy, INK, 6) + node(ix, iy, 6) + node(jx, jy, 6)
    o += L(ix, iy, ix + 150, iy, MUT, 1.4) + head(ix + 150, iy, 0, MUT, 9) + T(ix + 158, iy + 6, '*X*', 16, MUT, 'start', 'bold')
    o += L(ix, iy, ix, iy - 150, MUT, 1.4) + head(ix, iy - 150, -math.pi / 2, MUT, 9) + T(ix - 8, iy - 156, '*Y*', 16, MUT, 'end', 'bold')
    o += A(jx, jy, jx + 90 * c, jy - 90 * s, AC, 2.6, 11) + T(jx + 96 * c + 6, jy - 96 * s, "*x*'（桿軸）", 15, AC, 'start', 'bold')
    o += A(jx, jy, jx - 90 * s, jy - 90 * c, TEN, 2.6, 11) + T(jx - 96 * s - 4, jy - 96 * c - 8, "*y*'（垂直桿軸）", 15, TEN, 'end', 'bold')
    o += arc_arrow(jx, jy, 22, -40, 220, COMP, 2.2, 9) + T(jx + 26, jy + 30, 'θ 不必轉', 15, COMP, 'start', 'bold')
    o += R(560, 50, 320, 220, '#fff', KEY, 2, 12)
    o += T(720, 82, '每個節點的 [*t*]', 16, KEY, 'middle', 'bold')
    o += mat_grid(632, 104, [['*c*', '*s*', '0'], ['−*s*', '*c*', '0'], ['0', '0', '1']], 60, 38, size=16)
    o += T(720, 246, "(*u*', *v*', θ) ＝ [*t*] (*u*, *v*, θ)", 15, INK, 'middle', 'bold')
    return svg(W, H, o, '剛架元素的座標轉換')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4, 'fig4_5': fig4_5}

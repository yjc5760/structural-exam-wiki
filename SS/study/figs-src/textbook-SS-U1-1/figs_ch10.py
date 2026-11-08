# -*- coding: utf-8 -*-
"""第 10 章 柱強度曲線 的全部向量圖（所有曲線由公式逐點計算）。"""
import math
from plot import *  # noqa
from calcs import E, sq, Cc_of, Fcr_lrfd, Fa_asd, FS_of, example

FY = 2.52
SQ = sq(FY)              # 28.45
S1 = math.pi * SQ        # Fe = Fy 時的 KL/r = 89.4
CC = Cc_of(FY)           # 126.4
S15 = 1.5 * math.pi * SQ  # 134.1
PUR = '#7b1fa2'; PUR2 = '#f3e5f5'


def fe(s):
    return math.pi ** 2 * E / s ** 2 if s > 0 else 99


# ---------------------------------------------------------------- 10-1
def fig10_1():
    W, H = 820, 470
    p = Plot(90, 60, 600, 330, 0, 250, 0, 4.0)
    o = p.axes([0, 50, 100, 150, 200, 250], [0, 1, 2, 2.52, 3, 4], 'KL/r', '應力（tf/cm²）',
               yfmt=lambda t: '2.52' if t == 2.52 else f(t))
    # 兩個區域
    o += p.area(lambda s: 4.0, lambda s: 0, 0, S1, AC2, 0.55)
    o += p.area(lambda s: 4.0, lambda s: 0, S1, 250, COMP2, 0.6)
    # Fy 線與 Euler
    o += p.hline(FY, 0, 250, TEN, 2.2, '7 5')
    o += p.curve(fe, 40, 250, AC, 2.4, '7 5')
    # 取小者（包絡線）
    o += p.curve(lambda s: min(FY, fe(s)), 0.5, 250, PUR, 5)
    o += p.dot(S1, FY, PUR, 6)
    o += p.vline(S1, 0, FY, PUR, 1.3)
    o += T(p.X(S1), p.Y(0) + 40, f'{S1:.1f}', 14, PUR, 'middle', 'bold')
    o += T(p.X(S1) + 10, p.Y(FY) - 14, '兩線交點：F_{e} = F_{y}', 14, PUR, 'start', 'bold')
    o += T(p.X(2), p.Y(FY) - 10, '材料上限 F_{y}（橫線）', 14, TEN, 'start', 'bold')
    o += T(p.X(52), p.Y(3.75), '幾何上限 F_{e}=π²E/(KL/r)²', 14, AC, 'start', 'bold')
    o += T(p.X(30), p.Y(0.9), 'F_{e} > F_{y}', 15, AC, 'middle', 'bold')
    o += T(p.X(30), p.Y(0.9) + 22, '材料先輸', 14, AC, 'middle')
    o += T(p.X(30), p.Y(0.9) + 42, '（壓降伏）', 13, MUT, 'middle')
    o += T(p.X(190), p.Y(1.25), 'F_{e} < F_{y}', 15, COMP, 'middle', 'bold')
    o += T(p.X(190), p.Y(1.25) + 22, '幾何先輸', 14, COMP, 'middle')
    o += T(p.X(190), p.Y(1.25) + 42, '（彎出去＝挫屈）', 13, MUT, 'middle')
    o += T(p.X(250) + 4, p.Y(0.35), '紫粗線＝', 13, PUR, 'start', 'bold')
    o += T(p.X(250) + 4, p.Y(0.35) + 18, '兩者取小', 13, PUR, 'start', 'bold')
    # 右側柱子小圖
    bx = 735
    o += T(bx + 30, 90, '粗短柱', 14, AC, 'middle', 'bold')
    o += R(bx + 18, 110, 24, 70, STEEL2, INK, 1.5) + A(bx + 30, 92 + 4, bx + 30, 108, INK, 1.8)
    o += T(bx + 30, 200, '壓扁', 13, MUT, 'middle')
    o += T(bx + 30, 250, '細長柱', 14, COMP, 'middle', 'bold')
    pts = [(bx + 30 + 16 * math.sin(math.pi * t / 100), 270 + 1.3 * t) for t in range(0, 101, 5)]
    o += L(bx + 30, 270, bx + 30, 400, MUT, 1, '4 3') + P(pts, COMP, 4)
    o += T(bx + 30, 425, '彎出去', 13, MUT, 'middle')
    return svg(W, H, o, '材料上限與幾何上限兩線取小')


# ---------------------------------------------------------------- 10-2
def fig10_2():
    W, H = 820, 480
    p = Plot(90, 85, 610, 320, 0, 3.0, 0, 1.6)
    o = p.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.5, 1, 1.5], 'λ_{c}', 'F/F_{y}')
    # 上方第二軸 KL/r（A36）
    ytop = p.y0 - 8
    o += L(p.X(0), ytop, p.X(3), ytop, MUT, 1)
    for s in (50, 89.4, 134.1, 200, 250):
        lc = s / S1
        if lc <= 3:
            o += L(p.X(lc), ytop - 5, p.X(lc), ytop, MUT, 1)
            o += T(p.X(lc), ytop - 10, f(s) if s not in (89.4, 134.1) else f'{s:.1f}', 12.5,
                   PUR if s in (89.4, 134.1) else MUT, 'middle', 'bold' if s in (89.4, 134.1) else None)
    o += T(p.X(3) + 10, ytop + 4, 'A36 的 KL/r', 13, MUT, 'start')
    o += p.area(lambda x: 1.6, lambda x: 0, 0, 1, AC2, 0.55)
    o += p.area(lambda x: 1.6, lambda x: 0, 1, 3, COMP2, 0.6)
    o += p.hline(1, 0, 3, TEN, 2.2, '7 5')
    o += p.curve(lambda x: 1 / x ** 2, 0.62, 3, AC, 2.4, '7 5')
    o += p.curve(lambda x: min(1, 1 / x ** 2), 0.01, 3, PUR, 5)
    o += p.dot(1, 1, PUR, 6) + p.vline(1, 0, 1, PUR, 1.3)
    o += T(p.X(1) + 10, p.Y(1) - 14, '交點永遠在 λ_{c} = 1', 15, PUR, 'start', 'bold')
    o += T(p.X(0.05), p.Y(1) - 10, '材料：F_{y}/F_{y} = 1', 14, TEN, 'start', 'bold')
    o += T(p.X(0.68), p.Y(1.5), '幾何：F_{e}/F_{y} = 1/λ_{c}²', 14, AC, 'start', 'bold')
    o += T(p.X(0.5), p.Y(0.35), 'λ_{c} < 1', 15, AC, 'middle', 'bold')
    o += T(p.X(0.5), p.Y(0.35) + 22, '材料先輸', 14, AC, 'middle')
    o += T(p.X(2.2), p.Y(0.55), 'λ_{c} > 1', 15, COMP, 'middle', 'bold')
    o += T(p.X(2.2), p.Y(0.55) + 22, '幾何先輸', 14, COMP, 'middle')
    o += R(560, 410 + 22, 250, 36, KEY2, KEY, 1.4, 8)
    o += T(685, 410 + 46, '縱軸 ÷F_{y}、橫軸換成 λ_{c}', 14, KEY, 'middle', 'bold')
    o += T(90, 410 + 46, '同一張圖適用所有鋼種（A36、A572 ⋯）', 14, INK, 'start')
    return svg(W, H, o, '無因次化後的柱強度圖')


# ---------------------------------------------------------------- 10-3
def fig10_3():
    W, H = 860, 470
    o = ''
    # 左：初始彎曲柱
    cx, top, bot = 120, 70, 390
    Lp = bot - top
    d0, d1 = 14, 34
    o += L(cx, top, cx, bot, MUT, 1, '4 3')
    o += P([(cx + d0 * math.sin(math.pi * (y - top) / Lp), y) for y in range(top, bot + 1, 4)], STEEL, 2, dash='6 4')
    o += P([(cx + d1 * math.sin(math.pi * (y - top) / Lp), y) for y in range(top, bot + 1, 4)], COMP, 4)
    o += A(cx, top - 50, cx, top - 3, COMP, 3, 13) + T(cx + 10, top - 30, '*P*', 18, COMP, 'start', 'bold')
    o += A(cx, bot + 50, cx, bot + 3, COMP, 3, 13) + T(cx + 10, bot + 38, '*P*', 18, COMP, 'start', 'bold')
    ym = (top + bot) / 2
    o += dim(cx, ym, cx + d0, ym, '', STEEL, 0)
    o += T(cx - 6, ym + 24, 'δ_{0}', 15, STEEL, 'end', 'bold')
    o += dim(cx, ym - 26, cx + d1, ym - 26, '', COMP, 0)
    o += T(cx + d1 + 6, ym - 22, 'δ_{0}+δ', 15, COMP, 'start', 'bold')
    o += T(cx, 460, '虛線＝出廠時就微彎', 13, MUT, 'middle')
    # 中：上半段自由體圖
    fx, ftop, fbot = 330, 100, 260
    o += T(fx + 10, 34, '切開中點看上半段', 14, INK, 'middle', 'bold')
    o += P([(fx + d1 * math.sin(math.pi * (y - ftop) / (2 * (fbot - ftop))), y) for y in range(ftop, fbot + 1, 4)], COMP, 4)
    o += A(fx, ftop - 46, fx, ftop - 3, COMP, 3, 13) + T(fx - 10, ftop - 26, '*P*', 17, COMP, 'end', 'bold')
    o += A(fx + d1, fbot + 50, fx + d1, fbot + 3, COMP, 3, 13) + T(fx + d1 + 10, fbot + 40, '*P*', 17, COMP, 'start', 'bold')
    o += dim(fx, fbot + 62, fx + d1, fbot + 62, '', INK, 0)
    o += T(fx + d1 / 2, fbot + 84, '力臂 δ_{0}+δ', 14, INK, 'middle')
    # 力矩箭頭
    import math as m
    arc = [(fx + d1 + 32 * m.cos(t), fbot - 6 + 32 * m.sin(t)) for t in [m.radians(a) for a in range(200, 470, 10)]]
    o += curve_arrow(arc, WARN, 2.6, 11)
    o += T(fx + d1 + 44, fbot - 46, '推歪力矩', 14, WARN, 'start', 'bold')
    o += T(fx + d1 + 44, fbot - 26, '*M* = *P*(δ_{0}+δ)', 14, WARN, 'start')
    o += T(fx + 12, 400, '一加 *P* 就有彎矩', 13.5, INK, 'middle')
    o += T(fx + 12, 422, '→ 彎矩又讓 δ 變大', 13.5, INK, 'middle')
    o += T(fx + 12, 444, '→ 沒有「突然分岔」', 13.5, INK, 'middle')
    # 右：放大曲線
    p = Plot(540, 70, 270, 300, 0, 12, 0, 1.1)
    o += p.axes([0, 4, 8, 12], [0, 0.5, 0.877, 1.0], 'δ/δ_{0}', '*P*/*P*_{e}', size=12.5,
                yfmt=lambda t: '0.877' if t == 0.877 else f(t))
    o += p.vline(0.0001, 0, 1.0, MUT, 0) + L(p.X(0), p.Y(1), p.X(12), p.Y(1), AC, 2, '7 5')
    o += T(p.X(12), p.Y(1) - 8, '理想直柱：在 *P*_{e} 突然分岔', 12.5, AC, 'end')
    o += p.curve(lambda r: 1 - 1 / r if r >= 1 else 0, 1, 12, COMP, 3.4)
    o += p.hline(0.877, 0, 1 / (1 - 0.877), PUR, 1.4)
    o += p.dot(1 / (1 - 0.877), 0.877, PUR, 5)
    o += T(p.X(8.6), p.Y(0.877) + 20, 'δ 已放大 8 倍', 12.5, PUR, 'start', 'bold')
    o += T(p.X(3.2), p.Y(0.42), 'δ = δ_{0}/(1−*P*/*P*_{e})', 13.5, COMP, 'start', 'bold')
    o += T(675, 430, '真實柱：還沒到 *P*_{e} 就彎得很厲害', 13.5, COMP, 'middle', 'bold')
    return svg(W, H, o, '初始彎曲的放大效應')


# ---------------------------------------------------------------- 10-4
def fig10_4():
    W, H = 860, 330
    o = ''
    panels = [(0.0, '① 只有殘留應力', '翼板端部已帶 0.5*F*_{y} 壓應力'),
              (0.5, '② 外加 *f* = 0.5*F*_{y}', '端部剛好到 *F*_{y} → 比例限'),
              (0.75, '③ 外加 *f* = 0.75*F*_{y}', '端部已降伏（黑），只剩中間彈性')]
    pw, gap = 250, 30
    for i, (fa, t1, t2) in enumerate(panels):
        x0 = 30 + i * (pw + gap)
        base, sc = 230, 110   # y of zero; px per Fy
        o += T(x0 + pw / 2, 34, t1, 15, INK, 'middle', 'bold')
        # 翼板
        o += R(x0, 250, pw, 14, STEEL3, INK, 1.2)
        o += T(x0 + pw / 2, 290, '翼板寬度', 12.5, MUT, 'middle')
        # 應力分布：壓為上
        n = 60
        pts = []
        yld = []
        for k in range(n + 1):
            u = k / n
            r = 0.5 * (abs(2 * u - 1) * 2 - 1)      # 端部 +0.5（壓）、中央 −0.5（拉）
            tot = min(1.0, fa + r)
            pts.append((x0 + u * pw, base - tot * sc))
            yld.append(fa + r >= 1.0 - 1e-9)
        poly = [(x0, base)] + pts + [(x0 + pw, base)]
        o += P(poly, None, fill=COMP2 if fa > 0 else WARN2, close=True)
        o += P(pts, COMP if fa > 0 else WARN, 2.6)
        # 已降伏段塗黑
        for k in range(n):
            if yld[k] and yld[k + 1]:
                o += R(x0 + k / n * pw, 250, pw / n + 0.5, 14, INK, None)
        o += L(x0 - 6, base, x0 + pw + 6, base, INK, 1.2)
        o += L(x0 - 6, base - sc, x0 + pw + 6, base - sc, TEN, 1.6, '6 4')
        o += T(x0 + pw + 4, base - sc - 6, '*F*_{y}', 13, TEN, 'end', 'bold')
        o += T(x0 - 4, base + 16, '0', 12, MUT, 'end')
        o += T(x0 + pw / 2, 318, t2, 13, COMP if i else WARN, 'middle', 'bold')
    o += T(30, 58, '壓應力畫在上方', 12, MUT, 'start')
    return svg(W, H, o, '殘留應力讓翼板端部提早降伏')


# ---------------------------------------------------------------- 10-5
def fig10_5():
    W, H = 840, 470
    p = Plot(90, 60, 620, 340, 0, 3.0, 0, 1.15)
    o = p.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.39, 0.658, 0.877, 1.0], 'λ_{c}', '*F*_{cr}/*F*_{y}',
               yfmt=lambda t: {0.39: '0.390', 0.658: '0.658', 0.877: '0.877'}.get(t, f(t)))
    ideal = lambda x: min(1, 1 / x ** 2) if x > 0 else 1
    des = lambda x: 0.658 ** (x * x) if x <= 1.5 else 0.877 / x ** 2
    o += p.area(ideal, des, 0.001, 3, PUR2, 0.9)
    o += p.curve(ideal, 0.001, 3, AC, 2.2, '7 5')
    o += p.curve(lambda x: 0.658 ** (x * x), 0, 1.5, COMP, 4)
    o += p.curve(lambda x: 0.877 / x ** 2, 1.5, 3, COMP, 4)
    o += p.curve(lambda x: 0.877 / x ** 2, 1.0, 1.5, COMP, 1.5, '3 4')
    o += p.dot(1.5, 0.877 / 2.25, COMP, 6)
    o += p.vline(1.5, 0, 0.39, COMP, 1.2)
    o += T(p.X(1.5) - 12, p.Y(0.39) + 30, '接點 (1.5, 0.390)', 14, COMP, 'end', 'bold')
    # λ=1 落差
    o += A(p.X(1.0), p.Y(1.0) + 3, p.X(1.0), p.Y(0.658) - 4, PUR, 2, 9, both=True)
    o += T(p.X(1.0) + 8, p.Y(0.83), '差最多：1 → 0.658', 13.5, PUR, 'start', 'bold')
    o += T(p.X(1.0) + 8, p.Y(0.83) + 18, '（殘留應力＋初始彎曲）', 12.5, PUR, 'start')
    o += T(p.X(0.04), p.Y(1.0) - 10, 'λ_{c}→0：0.658⁰ = 1，回到 *F*_{y}', 13.5, COMP, 'start', 'bold')
    o += T(p.X(1.95), p.Y(0.66), '彈性段 = 0.877 × 理想', 13.5, COMP, 'start', 'bold')
    o += T(p.X(1.95), p.Y(0.66) + 20, '（只剩初始彎曲打折）', 12.5, COMP, 'start')
    o += T(p.X(1.95), p.Y(0.66) + 44, '藍虛線＝理想（取小）', 12.5, AC, 'start')
    o += T(p.X(0.2), p.Y(0.15), '非彈性段 0.658^{λc²}', 14, COMP, 'start', 'bold')
    o += T(p.X(1.62), p.Y(0.06), '彈性段 0.877/λ_{c}²', 14, COMP, 'start', 'bold')
    o += T(420, 455, '紫色區＝真實柱比理想柱少掉的強度', 13.5, PUR, 'middle', 'bold')
    return svg(W, H, o, 'LRFD 柱強度曲線')


# ---------------------------------------------------------------- 10-6
def fig10_6():
    W, H = 840, 400
    p = Plot(90, 50, 380, 300, 1.1, 1.9, 0.2, 0.6)
    o = p.axes([1.2, 1.5, 1.8], [0.3, 0.39, 0.5], 'λ_{c}', '*F*_{cr}/*F*_{y}',
               yfmt=lambda t: '0.390' if t == 0.39 else f(t))
    o += p.curve(lambda x: 0.658 ** (x * x), 1.1, 1.5, COMP, 4)
    o += p.curve(lambda x: 0.658 ** (x * x), 1.5, 1.9, COMP, 1.5, '3 4')
    o += p.curve(lambda x: 0.877 / x ** 2, 1.5, 1.9, AC, 4)
    o += p.curve(lambda x: 0.877 / x ** 2, 1.1, 1.5, AC, 1.5, '3 4')
    o += p.dot(1.5, 0.39, PUR, 7)
    o += T(p.X(1.12), p.Y(0.36), '左邊：*a*^{λc²}（*a* 未知）', 14, COMP, 'start', 'bold')
    o += T(p.X(1.53), p.Y(0.47), '右邊：0.877/λ_{c}²', 14, AC, 'start', 'bold')
    o += T(p.X(1.5) + 12, p.Y(0.39) + 22, '兩邊必須接上', 14, PUR, 'start', 'bold')
    # 右邊：三步推算
    bx = 520
    steps = [('① 右邊在 1.5 的值', '0.877 ÷ 1.5² = 0.877 ÷ 2.25 = 0.390'),
             ('② 左邊要相等', '*a*^{2.25} = 0.390'),
             ('③ 開 2.25 次方', '*a* = 0.390^{1/2.25} = 0.658 ✔')]
    for i, (t, s) in enumerate(steps):
        y = 60 + i * 100
        o += R(bx, y, 300, 76, KEY2 if i == 2 else '#fff', KEY, 1.5, 9)
        o += T(bx + 14, y + 28, t, 15, KEY, 'start', 'bold')
        o += T(bx + 14, y + 56, s, 14.5, INK, 'start')
        if i < 2:
            o += A(bx + 150, y + 78, bx + 150, y + 98, KEY, 2, 9)
    o += T(bx + 150, 375, '計算機：0.39 ^ (1÷2.25)', 13, MUT, 'middle')
    return svg(W, H, o, '由連續條件反推 0.658')


# ---------------------------------------------------------------- 10-7
def fig10_7():
    W, H = 840, 450
    p = Plot(90, 60, 620, 320, 0, 250, 0, 3.0)
    o = p.axes([0, 50, 100, 150, 200, 250], [0, 1.26, 2.52], 'KL/r', '應力（tf/cm²）',
               yfmt=lambda t: {1.26: '1.26', 2.52: '2.52'}.get(t, f(t)))
    o += p.area(lambda s: 3.0, lambda s: 0, 0, CC, WARN2, 0.8)
    o += p.area(lambda s: 3.0, lambda s: 0, CC, 250, AC2, 0.7)
    o += p.hline(FY, 0, 250, TEN, 2, '7 5')
    o += p.hline(FY / 2, 0, 250, WARN, 2.2, '7 5')
    o += p.curve(fe, 55, 250, AC, 3)
    o += p.dot(CC, FY / 2, PUR, 7) + p.vline(CC, 0, FY / 2, PUR, 1.5)
    o += T(p.X(CC), p.Y(0) + 40, f'*C*_{{c}} = {CC:.1f}', 15, PUR, 'middle', 'bold')
    o += p.dot(S1, FY, MUT, 4)
    o += T(p.X(3), p.Y(FY) - 10, '*F*_{y}', 14, TEN, 'start', 'bold')
    o += T(p.X(3), p.Y(FY / 2) - 10, '比例限 *F*_{y}/2（殘留應力 0.5*F*_{y} 吃掉一半）', 14, WARN, 'start', 'bold')
    o += T(p.X(150), p.Y(2.3), 'Euler：*F*_{e} = π²*E*/(*KL*/*r*)²', 14, AC, 'start', 'bold')
    o += T(p.X(CC / 2), p.Y(0.55), '*KL*/*r* < *C*_{c}', 15, WARN, 'middle', 'bold')
    o += T(p.X(CC / 2), p.Y(0.55) + 22, '挫屈前已部分降伏 → 非彈性', 14, WARN, 'middle')
    o += T(p.X(195), p.Y(0.15), '*KL*/*r* > *C*_{c}', 15, AC, 'middle', 'bold')
    o += T(p.X(195), p.Y(0.15) + 22, '全斷面彈性 → Euler', 14, AC, 'middle')
    o += T(p.X(CC) + 12, p.Y(FY / 2) + 24, 'Euler 碰到 *F*_{y}/2 的地方', 13.5, PUR, 'start', 'bold')
    return svg(W, H, o, 'Cc 的定義')


# ---------------------------------------------------------------- 10-8
def fig10_8():
    W, H = 840, 450
    p = Plot(90, 60, 620, 320, 0, 250, 0, 3.0)
    o = p.axes([0, 50, 100, 150, 200, 250], [0, 1.26, 2.52], 'KL/r', '應力（tf/cm²）',
               yfmt=lambda t: {1.26: '1.26', 2.52: '2.52'}.get(t, f(t)))
    par = lambda s: FY * (1 - s * s / (2 * CC * CC))
    o += p.curve(fe, 55, CC, AC, 1.6, '6 4')
    o += p.curve(fe, CC, 250, AC, 4)
    o += p.curve(par, 0, CC, WARN, 4.4)
    # 切線
    slope = -FY / CC
    a, b = CC - 45, CC + 45
    o += L(p.X(a), p.Y(FY / 2 + slope * (a - CC)), p.X(b), p.Y(FY / 2 + slope * (b - CC)), PUR, 2, '4 3')
    o += p.dot(0, FY, WARN, 7) + p.dot(CC, FY / 2, PUR, 7)
    o += L(p.X(0), p.Y(FY), p.X(35), p.Y(FY), WARN, 2)
    o += T(p.X(4), p.Y(FY) - 14, '① 起點 (0, *F*_{y})，頂端是平的', 14, WARN, 'start', 'bold')
    o += T(p.X(CC) + 14, p.Y(FY / 2) - 8, '② 在 *C*_{c} 處接上 Euler，而且相切', 14, PUR, 'start', 'bold')
    o += T(p.X(CC) + 14, p.Y(FY / 2) + 12, '（紫虛線＝共同切線，不會折一下）', 12.5, PUR, 'start')
    o += T(p.X(62), p.Y(2.85), '虛線段 Euler 在比例限以上已不成立', 12.5, AC, 'start')
    o += T(p.X(30), p.Y(0.9), '*F*_{cr} = *F*_{y}[1 − (*KL*/*r*)²/(2*C*_{c}²)]', 15, WARN, 'start', 'bold')
    o += T(p.X(30), p.Y(0.9) + 24, '＝ CRC 拋物線', 14, WARN, 'start')
    o += T(p.X(180), p.Y(0.9), 'Euler', 15, AC, 'start', 'bold')
    return svg(W, H, o, 'CRC 拋物線的兩個條件')


# ---------------------------------------------------------------- 10-9
def fig10_9():
    W, H = 840, 400
    p = Plot(90, 50, 600, 280, 0, 1.6, 1.6, 2.0)
    o = p.axes([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5], [1.6, 5 / 3, 1.8, 23 / 12, 2.0],
               '*x* = (*KL*/*r*)/*C*_{c}', '安全係數 FS',
               yfmt=lambda t: {5 / 3: '5/3', 23 / 12: '23/12'}.get(t, f(t)))
    fs = lambda x: 5 / 3 + 3 * x / 8 - x ** 3 / 8 if x <= 1 else 23 / 12
    o += p.area(lambda x: fs(x), lambda x: 1.6, 0, 1, WARN2, 0.7)
    o += p.area(lambda x: fs(x), lambda x: 1.6, 1, 1.6, AC2, 0.7)
    o += p.curve(fs, 0, 1.6, KEY, 4)
    o += p.hline(23 / 12, 0, 1.6, MUT, 1, '4 4') + p.hline(5 / 3, 0, 1.6, MUT, 1, '4 4')
    o += p.dot(0, 5 / 3, KEY, 6) + p.dot(1, 23 / 12, KEY, 6)
    o += L(p.X(0.8), p.Y(23 / 12), p.X(1.2), p.Y(23 / 12), PUR, 3)
    o += T(p.X(0.03), p.Y(5 / 3) - 12, '起點 5/3 ≈ 1.67（和拉力桿件同級）', 14, KEY, 'start', 'bold')
    o += T(p.X(1.0), p.Y(23 / 12) - 16, '終點 23/12 ≈ 1.92，落地要平', 14, PUR, 'middle', 'bold')
    o += T(p.X(0.5), p.Y(1.62), '非彈性：FS 一路加大', 14, WARN, 'middle', 'bold')
    o += T(p.X(1.3), p.Y(1.62), '彈性：固定 23/12', 14, AC, 'middle', 'bold')
    o += T(p.X(0.5), p.Y(1.79) + 34, 'FS = 5/3 + (3*x* − *x*³)/8', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'ASD 安全係數 FS')


# ---------------------------------------------------------------- 10-10
def fig10_10():
    W, H = 860, 420
    o = ''
    p = Plot(70, 60, 330, 280, 0, 2.5, 0, 1.1)
    o += T(235, 28, '(a) 兩條「非彈性」曲線（未除安全係數）', 14.5, INK, 'middle', 'bold')
    o += p.axes([0, 0.5, 1, 1.5, 2, 2.5], [0, 0.5, 1], 'λ_{c}', '*F*_{cr}/*F*_{y}', size=12.5)
    o += p.curve(lambda x: min(1.1, 1 / x ** 2), 0.95, 2.5, MUT, 1.6, '6 4')
    o += p.curve(lambda x: 1 - x * x / 4, 0, math.sqrt(2), WARN, 3.6)
    o += p.curve(lambda x: 0.658 ** (x * x) if x <= 1.5 else 0.877 / x ** 2, 0, 2.5, COMP, 3.6)
    o += p.vline(math.sqrt(2), 0, 0.5, WARN, 1.2) + p.vline(1.5, 0, 0.39, COMP, 1.2)
    o += T(p.X(math.sqrt(2)) - 4, p.Y(0) - 6, '√2', 12.5, WARN, 'end', 'bold')
    o += T(p.X(1.5) + 4, p.Y(0) - 6, '1.5', 12.5, COMP, 'start', 'bold')
    o += T(p.X(0.1), p.Y(0.28), '橘：ASD 拋物線 1−λ²/4', 13, WARN, 'start', 'bold')
    o += T(p.X(0.1), p.Y(0.28) + 18, '紅：LRFD 0.658^{λ²}', 13, COMP, 'start', 'bold')
    o += T(p.X(0.1), p.Y(0.28) + 36, '灰：Euler 1/λ²', 13, MUT, 'start')
    # (b) 比值
    q = Plot(500, 60, 320, 280, 0, 2.5, 1.3, 1.5)
    o += T(660, 28, '(b) LRFD φ_{c}*P*_{n} ÷ ASD *P*_{a}', 14.5, INK, 'middle', 'bold')
    o += q.axes([0, 0.5, 1, 1.5, 2, 2.5], [1.3, 1.35, 1.4, 1.45, 1.5], 'λ_{c}', '', size=12.5)
    rat = lambda lc: 0.85 * Fcr_lrfd(lc, FY) / Fa_asd(lc * S1, FY)
    o += q.area(lambda x: 1.466, lambda x: 1.386, 0, 2.5, KEY2, 0.7)
    o += q.curve(rat, 0.01, 2.5, KEY, 3.6, n=400)
    ex = example()
    o += q.dot(ex['lc'], ex['LR'], COMP, 6)
    o += T(q.X(ex['lc']) + 10, q.Y(ex['LR']) - 10, f"本章範例 {ex['LR']:.2f}", 13, COMP, 'start', 'bold')
    o += T(q.X(1.25), q.Y(1.32), '永遠落在 1.39 ～ 1.47', 14, KEY, 'middle', 'bold')
    o += T(q.X(1.25), q.Y(1.32) + 20, '→ 拿來驗算自己的答案', 13, KEY, 'middle')
    return svg(W, H, o, 'LRFD 與 ASD 的比較')


# ---------------------------------------------------------------- 10-11
def fig10_11():
    W, H = 860, 470
    ex = example()
    o = ''
    top, bot = 70, 410
    Lp = bot - top
    cols = [(150, '強軸 x 平面', 1, 'x'), (420, '弱軸 y 平面', 2, 'y')]
    for cx, title, nw, ax in cols:
        o += T(cx, 34, title, 16, INK, 'middle', 'bold')
        o += L(cx, top, cx, bot, MUT, 1, '4 3')
        amp = 30
        pts = [(cx + amp * math.sin(nw * math.pi * (y - top) / Lp), y) for y in range(top, bot + 1, 3)]
        o += P(pts, COMP, 4)
        o += pin(cx, bot, INK, 9)
        o += P([(cx, top), (cx - 9, top - 13), (cx + 9, top - 13)], INK, 1.5, '#fff', close=True)
        o += hatch_ground(cx - 15, top - 13, 30, INK, down=False)
        if nw == 2:
            ym = (top + bot) / 2
            o += L(cx - 70, ym, cx - 4, ym, AC, 3) + C(cx, ym, 5, AC, '#fff', 1.5)
            o += T(cx - 74, ym - 8, '側撐', 14, AC, 'end', 'bold')
            o += dim(cx + 60, top, cx + 60, ym, '400', INK, 0, 14, side=-1)
            o += dim(cx + 60, ym, cx + 60, bot, '400', INK, 0, 14, side=-1)
        else:
            o += dim(cx + 60, top, cx + 60, bot, '800', INK, 0, 14, side=-1)
    # 右側計算框
    bx = 560
    o += R(bx, 70, 280, 150, AC2, AC, 1.5, 9)
    o += T(bx + 14, 98, '強軸：*KL*/*r*_{x}', 15, AC, 'start', 'bold')
    o += T(bx + 14, 128, f"= 800 / {ex['rx']}", 15, INK, 'start')
    o += T(bx + 14, 158, f"= {ex['slx']:.1f}", 17, COMP, 'start', 'bold')
    o += T(bx + 14, 196, '一個半波，長 800', 13.5, MUT, 'start')
    o += R(bx, 240, 280, 150, '#fff', AC, 1.5, 9)
    o += T(bx + 14, 268, '弱軸：*KL*/*r*_{y}', 15, AC, 'start', 'bold')
    o += T(bx + 14, 298, f"= 400 / {ex['ry']}", 15, INK, 'start')
    o += T(bx + 14, 328, f"= {ex['sly']:.1f}", 17, INK, 'start', 'bold')
    o += T(bx + 14, 366, '側撐把半波切成兩段', 13.5, MUT, 'start')
    o += T(bx + 140, 430, f"取大者：強軸 {ex['slx']:.1f} 控制", 15.5, COMP, 'middle', 'bold')
    return svg(W, H, o, '範例柱兩軸的挫屈形狀')


# ---------------------------------------------------------------- 10-12
def fig10_12():
    W, H = 880, 520
    p = Plot(90, 60, 520, 380, 0, 2.6, 0, 1.15)
    o = p.axes([0, 1, math.sqrt(2), 2, 2.5], [0, 0.39, 0.5, 1.0], 'λ_{c}', '*F*/*F*_{y}',
               xfmt=lambda t: {math.sqrt(2): '√2'}.get(t, f(t)),
               yfmt=lambda t: {0.39: '0.39'}.get(t, f(t)))
    o += p.hline(1, 0, 2.6, TEN, 2.2, '7 5')                                         # ①
    o += p.curve(lambda x: 1 / x ** 2, 0.93, 2.6, AC, 2.2, '7 5')                    # ②
    o += p.curve(lambda x: 0.658 ** (x * x) if x <= 1.5 else 0.877 / x ** 2, 0, 2.6, COMP, 4)  # ③④
    o += p.hline(0.5, 0, math.sqrt(2), WARN, 1.6, '4 3')                              # ⑤
    o += p.curve(lambda x: 1 - x * x / 4, 0, math.sqrt(2), WARN, 3, '9 4')            # ⑥
    o += p.dot(1.5, 0.39, COMP, 6) + p.dot(math.sqrt(2), 0.5, WARN, 6) + p.dot(1, 1, AC, 5)

    def tag(x, y, n, c):
        return C(x, y, 12, c, '#fff', 1.5) + T(x, y + 5, n, 14, '#fff', 'middle', 'bold')
    o += tag(p.X(2.45), p.Y(1) - 16, '1', TEN)
    o += tag(p.X(2.2), p.Y(1 / 2.2 ** 2) - 18, '2', AC)
    o += tag(p.X(1.5) + 22, p.Y(0.39) + 6, '3', COMP)
    o += tag(p.X(0.55), p.Y(0.658 ** 0.3025) - 22, '4', COMP)
    o += tag(p.X(0.25), p.Y(0.5) - 16, '5', WARN)
    o += tag(p.X(1.12), p.Y(1 - 1.12 ** 2 / 4) + 26, '6', WARN)
    # 右側步驟
    bx = 640
    steps = [('1', TEN, '畫 *F*_{y} 水平線（高 1）'),
             ('2', AC, '畫 Euler 1/λ²（λ=1 碰到 1）'),
             ('3', COMP, '1.5 處取 0.877/2.25 = 0.39'),
             ('4', COMP, '反推 0.39^{1/2.25} = 0.658'),
             ('5', WARN, 'ASD：比例限 1/2 → λ=√2'),
             ('6', WARN, '拋物線 1 − λ²/4 接到 (√2, ½)')]
    for i, (n, c, s) in enumerate(steps):
        y = 80 + i * 62
        o += C(bx + 14, y, 13, c, '#fff', 1.5) + T(bx + 14, y + 5, n, 14, '#fff', 'middle', 'bold')
        o += T(bx + 36, y + 5, s, 14, INK, 'start')
    o += R(bx - 6, 440, 240, 52, KEY2, KEY, 1.4, 8)
    o += T(bx + 114, 462, '只要記：0.877、1.5、½', 14.5, KEY, 'middle', 'bold')
    o += T(bx + 114, 483, '其他全部畫得出來', 13.5, KEY, 'middle')
    return svg(W, H, o, '考場上 30 秒重畫柱強度曲線')


ALL = {k: v for k, v in globals().items() if k.startswith('fig10_')}
